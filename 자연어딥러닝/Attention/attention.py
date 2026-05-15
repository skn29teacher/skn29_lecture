"""Bahdanau Attention layer for PyTorch.

BiLSTM 출력과 query를 입력받아 attention score, weight, context vector를 계산한다.
예를 들어 "영화 정말 좋다"에서 query가 "좋다"의 의미를 찾고,
key는 각 단어의 표지판 역할을 하고, value는 실제 단어 정보를 담는다.
"""

from __future__ import annotations

from typing import Optional, Tuple

import torch
import torch.nn as nn


class BahdanauAttention(nn.Module):
    """Bahdanau additive attention.

    역할:
    - Query와 BiLSTM 출력 사이의 관계를 학습한다.
    - 모든 time step에 대해 중요도를 계산한다.
    - softmax 이전 score와 softmax 이후 weight를 모두 반환한다.

    간단한 예:
    - 문장: "영화 정말 좋다"
    - query: 현재 보고 싶은 단어의 의미
    - key: 각 단어가 가진 표지판
    - value: 실제 단어 정보
    - 결과: query와 가장 잘 맞는 단어 쪽 weight가 커진다.

    입력 shape:
    - encoder_outputs: [B, T, Henc]
    - query: [B, Hq] 또는 [B, 1, Hq]
    - lengths: [B]

    출력 shape:
    - context_vector: [B, Henc]
    - attention_weights: [B, T]
    - attention_scores: [B, T]
    """

    def __init__(
        self,
        encoder_hidden_dim: int,
        query_dim: Optional[int] = None,
        attention_dim: int = 128,
        dropout: float = 0.1,
        verbose: bool = False,
    ):
        super().__init__()

        # query_dim이 없으면 encoder output과 같은 차원으로 본다.
        # query는 decoder가 지금 찾고 싶은 정보다.
        if query_dim is None:
            query_dim = encoder_hidden_dim

        self.encoder_hidden_dim = encoder_hidden_dim
        self.query_dim = query_dim
        self.attention_dim = attention_dim
        self.verbose = verbose

        # Bahdanau attention 파라미터.
        # encoder_projection: key/value 쪽 출력(모든 단어)을 attention 공간으로 보낸다.
        # query_projection: 현재 찾고 싶은 query를 같은 공간으로 보낸다.
        # score_projection: 두 정보를 섞은 뒤 최종 score 1개를 만든다.
        self.encoder_projection = nn.Linear(encoder_hidden_dim, attention_dim, bias=False)
        self.query_projection = nn.Linear(query_dim, attention_dim, bias=False)
        self.score_projection = nn.Linear(attention_dim, 1, bias=False)

        self.dropout = nn.Dropout(dropout)

    def _shape_query(self, query: torch.Tensor) -> torch.Tensor:
        """query를 [B, H] 형태로 맞춘다."""
        if query.dim() == 3 and query.size(1) == 1:
            query = query.squeeze(1)
        if query.dim() != 2:
            raise ValueError(f"query는 [batch_size, hidden_dim] 또는 [batch_size, 1, hidden_dim] 이어야 합니다. 현재 shape: {tuple(query.shape)}")
        return query

    def _make_mask(self, lengths: torch.Tensor, max_len: int) -> torch.Tensor:
        """padding 위치를 True로 표시하는 mask를 만든다.

        반환 shape:
        - mask: [B, T]
        - True: padding 위치
        - False: 실제 토큰 위치
        """
        device = lengths.device
        range_tensor = torch.arange(max_len, device=device).unsqueeze(0)  # [1, T]
        mask = range_tensor >= lengths.unsqueeze(1)  # [B, T]
        return mask

    def forward(
        self,
        encoder_outputs: torch.Tensor,
        query: torch.Tensor,
        lengths: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Attention 계산.

        forward 과정:
        1. encoder_outputs와 query의 shape를 확인한다.
        2. query를 [B, H] 형태로 정리한다.
        3. encoder_outputs와 query를 같은 attention 공간으로 projection한다.
        4. time step마다 additive score를 계산한다.
        5. lengths가 있으면 padding 위치를 mask 처리한다.
        6. softmax로 attention weight를 만든다.
        7. weight와 value를 이용해 context vector를 만든다.

        tensor shape:
        - encoder_outputs: [B, T, Henc]
        - query: [B, Hq]
        - enc_proj: [B, T, A]
        - query_proj: [B, 1, A]
        - combined: [B, T, A]
        - attention_scores: [B, T]
        - attention_weights: [B, T]
        - context_vector: [B, Henc]
        """
        if encoder_outputs.dim() != 3:
            raise ValueError(f"encoder_outputs는 [batch_size, seq_len, hidden_dim] 형태여야 합니다. 현재 shape: {tuple(encoder_outputs.shape)}")

        query = self._shape_query(query)

        batch_size, seq_len, hidden_dim = encoder_outputs.shape
        if hidden_dim != self.encoder_hidden_dim:
            raise ValueError(
                f"encoder_outputs의 마지막 차원(hidden_dim)이 초기화 값과 다릅니다. "
                f"expected={self.encoder_hidden_dim}, got={hidden_dim}"
            )

        if query.size(0) != batch_size:
            raise ValueError(
                f"query의 batch_size가 encoder_outputs와 같아야 합니다. "
                f"encoder_outputs batch={batch_size}, query batch={query.size(0)}"
            )

        if self.verbose:
            print("[Attention] encoder_outputs shape:", tuple(encoder_outputs.shape))
            print("[Attention] query shape:", tuple(query.shape))
            if lengths is not None:
                print("[Attention] lengths shape:", tuple(lengths.shape))

        # 1) Linear projection
        # encoder_outputs는 전체 문장이다. 여기에는 각 단어의 key/value 후보가 들어 있다.
        # query는 "지금 무엇을 보고 싶은가"를 나타낸다.
        # 예: "영화 정말 좋다"에서 query가 "좋다" 쪽 의미를 찾는다고 보면 된다.
        # encoder_outputs: [B, T, Henc] -> [B, T, A]
        # query: [B, Hq] -> [B, A] -> [B, 1, A]
        enc_proj = self.encoder_projection(encoder_outputs)
        query_proj = self.query_projection(query).unsqueeze(1)

        if self.verbose:
            print("[Attention] enc_proj shape:", tuple(enc_proj.shape))
            print("[Attention] query_proj shape:", tuple(query_proj.shape))

        # 2) Additive combination
        # query와 각 단어의 key를 더해 "얼마나 잘 맞는지"를 비교할 준비를 한다.
        # value는 아직 그대로 두고, score 계산 직전 상태만 만든다.
        combined = torch.tanh(enc_proj + query_proj)
        combined = self.dropout(combined)

        if self.verbose:
            print("[Attention] combined shape:", tuple(combined.shape))

        # 3) Score 계산
        # 각 time step마다 query와 key가 얼마나 맞는지 숫자로 만든다.
        # 점수가 클수록 그 단어를 더 많이 볼 가능성이 높다.
        attention_scores = self.score_projection(combined).squeeze(-1)

        if self.verbose:
            print("[Attention] raw attention_scores shape:", tuple(attention_scores.shape))
            print("[Attention] raw attention_scores sample:", attention_scores[0].detach().cpu() if attention_scores.numel() > 0 else attention_scores)

        # 4) Mask 적용
        # padding은 실제 단어가 아니므로 score를 무시한다.
        if lengths is not None:
            mask = self._make_mask(lengths=lengths, max_len=seq_len)
            attention_scores = attention_scores.masked_fill(mask, float("-inf"))

            if self.verbose:
                print("[Attention] mask shape:", tuple(mask.shape))
                print("[Attention] masked attention_scores sample:", attention_scores[0].detach().cpu() if attention_scores.numel() > 0 else attention_scores)

        # 5) Softmax로 attention weight 생성
        # score를 weight로 바꾼다. 합은 1이 된다.
        # 예: [좋다, 영화, 정말] 점수가 [1, 3, 2]면 softmax 뒤에는 "영화" 쪽 weight가 커질 수 있다.
        attention_weights = torch.softmax(attention_scores, dim=1)

        if self.verbose:
            print("[Attention] attention_weights shape:", tuple(attention_weights.shape))
            print("[Attention] attention_weights sample:", attention_weights[0].detach().cpu() if attention_weights.numel() > 0 else attention_weights)
            print("[Attention] weights sum per batch:", attention_weights.sum(dim=1).detach().cpu())

        # 6) Context vector 계산
        # value는 encoder_outputs를 그대로 사용한다.
        # attention_weights가 큰 단어의 value가 더 많이 더해진다.
        # 즉, 현재 query와 가장 관련 있는 단어 중심으로 문장 요약 벡터를 만든다.
        context_vector = torch.sum(attention_weights.unsqueeze(-1) * encoder_outputs, dim=1)

        if self.verbose:
            print("[Attention] context_vector shape:", tuple(context_vector.shape))

        return context_vector, attention_weights, attention_scores


class BiLSTMAttentionSentimentClassifier(nn.Module):
    """BiLSTM + Bahdanau Attention 감정분류 모델.

    이 클래스는 attention layer와 BiLSTM 출력의 연결을 보여준다.
    예를 들어 "영화 정말 좋다"에서 마지막 hidden state를 query로 두고,
    나머지 time step의 출력들(key/value 후보)을 보면서 중요한 단어를 고른다.

    입력 shape:
    - input_ids: [B, T]
    - lengths: [B]

    출력 shape:
    - probs: [B, 1]
    - attention_weights: [B, T]
    - attention_scores: [B, T]
    """

    def __init__(
        self,
        vocab_size: int,
        embedding_dim: int = 128,
        hidden_dim: int = 128,
        attention_dim: int = 128,
        dropout: float = 0.3,
        pad_idx: int = 0,
        verbose: bool = False,
    ):
        super().__init__()

        self.verbose = verbose
        self.hidden_dim = hidden_dim

        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=pad_idx)
        self.bilstm = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=hidden_dim,
            num_layers=1,
            batch_first=True,
            bidirectional=True,
        )
        self.attention = BahdanauAttention(
            encoder_hidden_dim=hidden_dim * 2,
            query_dim=hidden_dim * 2,
            attention_dim=attention_dim,
            dropout=dropout,
            verbose=verbose,
        )
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim * 2, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(
        self,
        input_ids: torch.Tensor,
        lengths: torch.Tensor,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """BiLSTM 출력과 Attention을 연결하는 forward.

        처리 순서:
        1. embedding
        2. pack_padded_sequence
        3. BiLSTM
        4. padded sequence 복원
        5. 마지막 hidden state를 query로 사용
        6. Bahdanau Attention 계산
        7. context vector로 감정 예측

        예:
        - 문장: "영화 정말 좋다"
        - query: 마지막 시점의 hidden state
        - key/value: 모든 time step의 BiLSTM 출력
        - 결과: "좋다"와 관련된 위치의 weight가 커진다.
        """
        if input_ids.dim() != 2:
            raise ValueError(f"input_ids는 [batch_size, seq_len] 형태여야 합니다. 현재 shape: {tuple(input_ids.shape)}")
        if lengths.dim() != 1:
            raise ValueError(f"lengths는 [batch_size] 형태여야 합니다. 현재 shape: {tuple(lengths.shape)}")

        if self.verbose:
            print("[Model] input_ids shape:", tuple(input_ids.shape))
            print("[Model] lengths shape:", tuple(lengths.shape))

        embeddings = self.embedding(input_ids)
        if self.verbose:
            print("[Model] embeddings shape:", tuple(embeddings.shape))

        packed_embeddings = nn.utils.rnn.pack_padded_sequence(
            embeddings,
            lengths.cpu(),
            batch_first=True,
            enforce_sorted=False,
        )

        packed_output, (h_n, c_n) = self.bilstm(packed_embeddings)

        if self.verbose:
            print("[Model] h_n shape:", tuple(h_n.shape))
            print("[Model] c_n shape:", tuple(c_n.shape))

        # packed sequence를 다시 펼쳐서 attention이 time step별 출력을 볼 수 있게 한다.
        # 여기의 각 time step은 문장 속 각 단어 위치에 해당한다.
        encoder_outputs, _ = nn.utils.rnn.pad_packed_sequence(
            packed_output,
            batch_first=True,
            total_length=input_ids.size(1),
        )

        if self.verbose:
            print("[Model] encoder_outputs shape:", tuple(encoder_outputs.shape))

        # BiLSTM의 마지막 layer forward/backward hidden state를 query로 사용한다.
        # query는 "지금 문장에서 무엇이 중요한가"를 묻는 질문 역할이다.
        query = torch.cat((h_n[-2], h_n[-1]), dim=1)

        if self.verbose:
            print("[Model] query shape:", tuple(query.shape))

        context_vector, attention_weights, attention_scores = self.attention(
            encoder_outputs=encoder_outputs,
            query=query,
            lengths=lengths,
        )

        if self.verbose:
            print("[Model] context_vector shape:", tuple(context_vector.shape))

        context_vector = self.dropout(context_vector)
        logits = self.fc(context_vector)
        probs = self.sigmoid(logits)

        if self.verbose:
            print("[Model] logits shape:", tuple(logits.shape))
            print("[Model] probs shape:", tuple(probs.shape))

        return probs, attention_weights, attention_scores


def _make_dummy_batch(batch_size: int = 4, seq_len: int = 7, vocab_size: int = 100):
    """더미 입력을 만든다."""
    input_ids = torch.randint(low=2, high=vocab_size, size=(batch_size, seq_len))
    lengths = torch.tensor([seq_len, seq_len - 1, seq_len - 2, seq_len - 3], dtype=torch.long)
    return input_ids, lengths


def main() -> None:
    """실행 함수."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("[device]", device)
    print()

    vocab_size = 500
    model = BiLSTMAttentionSentimentClassifier(
        vocab_size=vocab_size,
        embedding_dim=64,
        hidden_dim=128,
        attention_dim=64,
        dropout=0.3,
        pad_idx=0,
        verbose=True,
    ).to(device)

    input_ids, lengths = _make_dummy_batch(batch_size=4, seq_len=8, vocab_size=vocab_size)
    input_ids = input_ids.to(device)
    lengths = lengths.to(device)

    probs, attention_weights, attention_scores = model(input_ids, lengths)

    print()
    print("[결과] probs shape:", tuple(probs.shape))
    print("[결과] attention_weights shape:", tuple(attention_weights.shape))
    print("[결과] attention_scores shape:", tuple(attention_scores.shape))
    print("[결과] probs:")
    print(probs)
    print("[결과] attention_weights[0]:")
    print(attention_weights[0].detach().cpu())
    print("[결과] attention_scores[0]:")
    print(attention_scores[0].detach().cpu())


if __name__ == "__main__":
    main()
