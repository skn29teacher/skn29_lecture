"""PyTorch 기반 BiLSTM 감정분류 모델.

핵심 구성:

1. Embedding layer
2. BiLSTM
3. Dropout
4. Fully Connected layer
5. Sigmoid 출력

입력은 보통 preprocessing.py에서 만든 padded_ids와 lengths를 사용한다.
GPU가 있으면 자동으로 GPU를 사용하고, 없으면 CPU로 동작한다.
"""

from __future__ import annotations

from typing import Optional, Tuple

import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence


class BiLSTMSentimentClassifier(nn.Module):
    """한국어 영화리뷰 감정분류용 BiLSTM 모델.

    역할:
    - 단어 인덱스 입력을 받아 감정이 긍정인지 부정인지 예측한다.
    - 출력은 sigmoid를 거친 0~1 사이의 확률값이다.

    입력 shape:
    - input_ids: [batch_size, seq_len]
    - lengths: [batch_size]

    출력 shape:
    - probs: [batch_size, 1]
    """

    def __init__(
        self,
        vocab_size: int,
        embedding_dim: int = 128,
        hidden_dim: int = 128,
        num_layers: int = 1,
        dropout: float = 0.3,
        pad_idx: int = 0,
        verbose: bool = False,
    ):
        super().__init__()

        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.dropout_rate = dropout
        self.pad_idx = pad_idx
        self.verbose = verbose

        # 1) Embedding layer
        # 단어 인덱스를 dense vector로 바꾼다.
        self.embedding = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=embedding_dim,
            padding_idx=pad_idx,
        )

        # 2) BiLSTM
        # bidirectional=True 이므로 양방향 정보를 함께 학습한다.
        # dropout은 num_layers가 2 이상일 때만 LSTM 내부에 적용된다.
        lstm_dropout = dropout if num_layers > 1 else 0.0
        self.bilstm = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=lstm_dropout,
        )

        # 3) Dropout
        self.dropout = nn.Dropout(dropout)

        # 4) Fully Connected layer
        # BiLSTM이 양방향이므로 hidden_dim * 2 차원을 사용한다.
        self.fc = nn.Linear(hidden_dim * 2, 1)

        # 5) Sigmoid
        # binary classification이므로 0~1 확률로 변환한다.
        self.sigmoid = nn.Sigmoid()

    def forward(self, input_ids: torch.Tensor, lengths: torch.Tensor) -> torch.Tensor:
        """forward 과정."""
        if input_ids.dim() != 2:
            raise ValueError(f"input_ids는 [batch_size, seq_len] 형태여야 합니다. 현재 shape: {tuple(input_ids.shape)}")

        if lengths.dim() != 1:
            raise ValueError(f"lengths는 [batch_size] 형태여야 합니다. 현재 shape: {tuple(lengths.shape)}")

        if self.verbose:
            print("[forward] input_ids shape:", tuple(input_ids.shape))
            print("[forward] lengths shape:", tuple(lengths.shape))

        # 1) Embedding
        # input_ids의 shape: [B, T]
        # embedding 결과 shape: [B, T, E]
        embeddings = self.embedding(input_ids)

        if self.verbose:
            print("[forward] embeddings shape:", tuple(embeddings.shape))

        # 2) pack_padded_sequence
        # 길이가 다른 문장을 효율적으로 처리하기 위한 단계다.
        # CPU tensor가 필요하므로 lengths는 자동으로 cpu로 옮긴다.
        packed_embeddings = pack_padded_sequence(
            embeddings,
            lengths.cpu(),
            batch_first=True,
            enforce_sorted=False,
        )

        # 3) BiLSTM 통과
        # h_n shape: [num_layers * 2, B, H]
        packed_output, (h_n, c_n) = self.bilstm(packed_embeddings)

        if self.verbose:
            print("[forward] h_n shape:", tuple(h_n.shape))
            print("[forward] c_n shape:", tuple(c_n.shape))

        # 4) 마지막 layer의 forward/backward hidden state를 꺼낸다.
        # BiLSTM이므로 마지막 layer의 forward state와 backward state를 붙인다.
        # h_n[-2] = 마지막 layer의 forward hidden state
        # h_n[-1] = 마지막 layer의 backward hidden state
        forward_hidden = h_n[-2]
        backward_hidden = h_n[-1]
        hidden = torch.cat((forward_hidden, backward_hidden), dim=1)

        if self.verbose:
            print("[forward] forward_hidden shape:", tuple(forward_hidden.shape))
            print("[forward] backward_hidden shape:", tuple(backward_hidden.shape))
            print("[forward] concatenated hidden shape:", tuple(hidden.shape))

        # 5) Dropout
        hidden = self.dropout(hidden)

        # 6) Fully Connected layer
        logits = self.fc(hidden)

        if self.verbose:
            print("[forward] logits shape:", tuple(logits.shape))

        # 7) Sigmoid 출력
        probs = self.sigmoid(logits)

        if self.verbose:
            print("[forward] probs shape:", tuple(probs.shape))

        return probs

    def predict_proba(self, input_ids: torch.Tensor, lengths: torch.Tensor) -> torch.Tensor:
        """예측 확률만 반환하는 편의 함수."""
        self.eval()
        with torch.no_grad():
            return self.forward(input_ids, lengths)

    def predict(self, input_ids: torch.Tensor, lengths: torch.Tensor, threshold: float = 0.5) -> torch.Tensor:
        """이진 분류 예측값을 반환한다.

        반환값:
        - 0 또는 1
        """
        probs = self.predict_proba(input_ids, lengths)
        return (probs >= threshold).long()


def _make_dummy_batch(
    batch_size: int = 4,
    seq_len: int = 8,
    vocab_size: int = 100,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """더미 배치를 만든다."""
    # 랜덤 입력과 길이를 만들어 forward/predict가 정상 동작하는지 확인한다.
    input_ids = torch.randint(low=2, high=vocab_size, size=(batch_size, seq_len))
    lengths = torch.tensor([seq_len, seq_len - 1, seq_len - 2, seq_len - 3], dtype=torch.long)
    return input_ids, lengths


def main() -> None:
    """모델 실행 코드."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("[device]", device)

    vocab_size = 500
    model = BiLSTMSentimentClassifier(
        vocab_size=vocab_size,
        embedding_dim=64,
        hidden_dim=128,
        num_layers=1,
        dropout=0.3,
        pad_idx=0,
        verbose=True,
    ).to(device)

    input_ids, lengths = _make_dummy_batch(batch_size=4, seq_len=10, vocab_size=vocab_size)
    input_ids = input_ids.to(device)
    lengths = lengths.to(device)

    # 입력 shape가 맞는지 먼저 확인한다.
    print("[test] input_ids shape:", tuple(input_ids.shape))
    print("[test] lengths shape:", tuple(lengths.shape))
    print()

    # forward로 확률을 계산하고, predict로 임계값 기준 label을 만든다.
    probs = model(input_ids, lengths)
    preds = model.predict(input_ids, lengths)

    print()
    print("[test] output probabilities:")
    print(probs)
    print("[test] output shape:", tuple(probs.shape))
    print("[test] predicted labels:")
    print(preds)


if __name__ == "__main__":
    main()
