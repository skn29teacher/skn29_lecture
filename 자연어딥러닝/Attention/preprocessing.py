"""한국어 영화 리뷰 감정분류용 전처리 모듈.

구성:

1. pandas로 데이터 읽기 또는 샘플 데이터 만들기
2. 정규표현식으로 문장 클리닝
3. 한국어만 남기기
4. 토큰화
5. 불용어 제거
6. vocab 생성
7. 정수 인코딩
8. padding
9. torch Dataset에서 바로 사용할 수 있는 형태로 변환
10. shape 출력으로 결과 확인

Windows 환경에서도 바로 실행할 수 있도록 경로 처리는 pathlib 기준으로 작성했다.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import pandas as pd
import torch
from torch.utils.data import Dataset


# -----------------------------
# 1. 기본 불용어 목록
# -----------------------------
# 기본 불용어 목록
DEFAULT_STOPWORDS = {
    "이", "그", "저", "것", "수", "등", "들", "좀", "정말", "너무", "그리고",
    "하지만", "또", "더", "가장", "매우", "그냥", "아주", "진짜", "약간",
}


# -----------------------------
# 2. 정제 함수
# -----------------------------
def clean_text(text: str) -> str:
    """문장에서 한국어 감정분류에 불필요한 기호를 지운다.

    역할:
    - 숫자, 영어, 특수문자 제거
    - 여러 공백을 하나로 정리
    - 앞뒤 공백 제거

    입력:
        "I 정말!! 재미있다 :) 123"

    출력:
        "정말 재미있다"
    """
    if not isinstance(text, str):
        text = "" if pd.isna(text) else str(text)

    # 한국어, 공백만 남기고 모두 제거한다.
    text = re.sub(r"[^가-힣\s]", " ", text)

    # 공백이 여러 번 연속된 부분은 하나로 줄인다.
    text = re.sub(r"\s+", " ", text)

    # 앞뒤 공백 제거
    return text.strip()


def keep_korean_only(text: str) -> str:
    """한국어만 남기는 전용 함수.

    역할:
    - clean_text 이후에 남을 수 있는 비한국어 토큰을 제거한다.

    주의:
    - 여기서는 한글 음절(가-힣)과 공백만 남긴다.
    """
    text = re.sub(r"[^가-힣\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -----------------------------
# 3. 토큰화 및 불용어 제거
# -----------------------------
def tokenize(text: str) -> List[str]:
    """공백 기준으로 토큰을 나눈다.

    역할:
    - 가장 단순한 공백 기준 토큰화 방식이다.

    예:
        "영화가 정말 재미있다" -> ["영화가", "정말", "재미있다"]
    """
    text = text.strip()
    if not text:
        return []
    return text.split()


def remove_stopwords(tokens: Sequence[str], stopwords: Optional[Iterable[str]] = None) -> List[str]:
    """불용어를 제거한다.

    역할:
    - 감정 판단에 덜 중요한 단어를 제외한다.
    - 불용어 목록은 기본값을 사용하거나 사용자가 직접 전달할 수 있다.

    입력:
        tokens: 토큰 리스트
        stopwords: 제거할 단어 목록

    출력:
        불용어가 제거된 토큰 리스트
    """
    stopword_set = set(DEFAULT_STOPWORDS if stopwords is None else stopwords)
    return [token for token in tokens if token not in stopword_set and token.strip()]


# -----------------------------
# 4. vocab 생성
# -----------------------------
def build_vocab(
    token_lists: Sequence[Sequence[str]],
    min_freq: int = 1,
    special_tokens: Optional[Sequence[str]] = None,
) -> Dict[str, int]:
    """토큰 목록으로부터 vocab을 생성한다."""
    if special_tokens is None:
        special_tokens = ["<pad>", "<unk>"]

    freq: Dict[str, int] = {}
    for tokens in token_lists:
        for token in tokens:
            freq[token] = freq.get(token, 0) + 1

    vocab: Dict[str, int] = {}
    for token in special_tokens:
        if token not in vocab:
            vocab[token] = len(vocab)

    for token, count in sorted(freq.items(), key=lambda item: (-item[1], item[0])):
        if count >= min_freq and token not in vocab:
            vocab[token] = len(vocab)

    return vocab


def tokens_to_ids(tokens: Sequence[str], vocab: Dict[str, int]) -> List[int]:
    """토큰을 정수 인덱스로 바꾼다."""
    unk_idx = vocab.get("<unk>", 1)
    return [vocab.get(token, unk_idx) for token in tokens]


# -----------------------------
# 5. padding
# -----------------------------
def pad_sequence(ids: Sequence[int], max_len: int, pad_idx: int = 0) -> List[int]:
    """시퀀스 길이를 고정 길이로 맞춘다."""
    ids = list(ids[:max_len])
    if len(ids) < max_len:
        ids.extend([pad_idx] * (max_len - len(ids)))
    return ids


# -----------------------------
# 6. pandas 기반 전체 전처리
# -----------------------------
def preprocess_dataframe(
    df: pd.DataFrame,
    text_col: str = "review",
    label_col: str = "sentiment",
    max_len: int = 50,
    stopwords: Optional[Iterable[str]] = None,
    min_freq: int = 1,
) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """데이터프레임 전체를 전처리한다."""
    required_columns = {text_col, label_col}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"필요한 컬럼이 없습니다: {missing}")

    processed = df.copy()

    # 1) 문자열 정제
    processed["clean_text"] = processed[text_col].astype(str).map(clean_text).map(keep_korean_only)

    # 2) 토큰화
    processed["tokens"] = processed["clean_text"].map(tokenize)

    # 3) 불용어 제거
    processed["tokens"] = processed["tokens"].map(lambda tokens: remove_stopwords(tokens, stopwords=stopwords))

    # 4) vocab 생성
    vocab = build_vocab(processed["tokens"].tolist(), min_freq=min_freq)
    pad_idx = vocab["<pad>"]

    # 5) 정수 인코딩 + padding
    processed["token_ids"] = processed["tokens"].map(lambda tokens: tokens_to_ids(tokens, vocab))
    # 길이가 max_len을 초과하면 truncate 되므로 실제 사용되는 length는 max_len을 넘지 않도록 제한한다.
    # 또한 pack_padded_sequence는 길이가 0인 시퀀스를 허용하지 않으므로 최소 길이를 1로 보정한다.
    processed["length"] = processed["token_ids"].map(lambda ids: max(1, min(len(ids), max_len)))
    processed["padded_ids"] = processed["token_ids"].map(lambda ids: pad_sequence(ids, max_len=max_len, pad_idx=pad_idx))

    # 6) label 정리
    processed["label"] = processed[label_col]

    return processed, vocab


# -----------------------------
# 7. torch Dataset
# -----------------------------
class KoreanSentimentDataset(Dataset):
    """한국어 감정분류용 PyTorch Dataset."""

    def __init__(self, processed_df: pd.DataFrame):
        self.input_ids = torch.tensor(processed_df["padded_ids"].tolist(), dtype=torch.long)
        self.labels = torch.tensor(processed_df["label"].tolist(), dtype=torch.long)
        self.lengths = torch.tensor(processed_df["length"].tolist(), dtype=torch.long)

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, idx: int):
        return self.input_ids[idx], self.labels[idx], self.lengths[idx]


# -----------------------------
# 8. 샘플 데이터 및 실행
# -----------------------------
def make_sample_dataframe() -> pd.DataFrame:
    """샘플 데이터프레임을 만든다."""
    return pd.DataFrame(
        {
            "review": [
                "이 영화는 정말 재미있고 감동적이었다!",
                "스토리가 너무 지루하고 별로였다.",
                "배우 연기가 훌륭해서 보는 내내 집중했다.",
                "기대했는데 너무 실망스러운 작품이었다.",
            ],
            "sentiment": [1, 0, 1, 0],
        }
    )


def print_shapes(processed_df: pd.DataFrame, dataset: KoreanSentimentDataset) -> None:
    """전처리 결과의 shape를 출력한다."""
    print("[DataFrame shape]", processed_df.shape)
    print("[input_ids shape]", tuple(dataset.input_ids.shape))
    print("[labels shape]", tuple(dataset.labels.shape))
    print("[lengths shape]", tuple(dataset.lengths.shape))


def load_or_create_dataframe(csv_path: Optional[str] = None) -> pd.DataFrame:
    """CSV 파일이 있으면 읽고, 없으면 샘플 데이터를 만든다."""
    if csv_path:
        path = Path(csv_path)
        if path.exists():
            return pd.read_csv(path)

    return make_sample_dataframe()


def main() -> None:
    """전처리 실행 함수."""
    # Windows 기준 경로. 실제 파일이 없으면 샘플 데이터로 대체된다.
    csv_path = r"data\raw\korean_movie_reviews.csv"

    df = load_or_create_dataframe(csv_path)
    print("[원본 데이터]")
    print(df.head())
    print()

    processed_df, vocab = preprocess_dataframe(
        df,
        text_col="review",
        label_col="sentiment",
        max_len=12,
        stopwords=DEFAULT_STOPWORDS,
        min_freq=1,
    )

    dataset = KoreanSentimentDataset(processed_df)

    print("[전처리 데이터]")
    print(processed_df[["review", "clean_text", "tokens", "token_ids", "padded_ids", "length", "label"]].head())
    print()

    print("[vocab 일부]")
    vocab_preview = list(vocab.items())[:15]
    print(vocab_preview)
    print()

    print_shapes(processed_df, dataset)
    print()

    # 첫 번째 샘플 확인
    sample_input_ids, sample_label, sample_length = dataset[0]
    print("[첫 번째 샘플]")
    print("input_ids:", sample_input_ids)
    print("label:", sample_label)
    print("length:", sample_length)


if __name__ == "__main__":
    main()
