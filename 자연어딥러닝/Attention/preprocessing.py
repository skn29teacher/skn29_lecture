# 데이터클리닝, 토큰화, 불용어 제거, vocab 생성, padding, Dataset구성
from dataclasses import dataclass
import re
import pandas as pd
import torch
from torch.utils.data import Dataset

# 기본불용어 목록
DEFAULT_STOPWORDS ={
    "이", "그", "저", "것", "수", "등", "들", "좀", "정말", "너무", "그리고",
    "하지만", "또", "더", "가장", "매우", "그냥", "아주", "진짜", "약간",
}

def clean_text(text: str) ->str:
    """문장에서 한국어 감정분류에 불필요한 기호를 지운다.

    역할:
    - 숫자, 영어, 특수문자 제거
    - 여러 공백을 하나로 정리
    - 앞뒤 공백 제거

    입력 예시:
        "I 정말!! 재미있다 :) 123"

    출력 예시:
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
    - clean_text 이후에도 혹시 남아 있을 수 있는 비한국어 토큰을 제거한다.
    - 초보자가 단계별로 확인하기 쉽도록 별도 함수로 분리했다.

    주의:
    - 여기서는 한글 음절(가-힣)과 공백만 남긴다.
    - 필요하면 조사/어미 분석은 별도의 형태소 분석기로 확장하면 된다.
    """
    text = re.sub(r"[^가-힣\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
from typing import Dict, Iterable,List,Optional,Sequence,Tuple

def tokenized(text:str) ->List[str]:
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

def remove_stopwords(tokens:Sequence[str], stopwords:Optional[Iterable[str]] = None) ->List[str]:
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

# 4. vocab 생성
# -----------------------------
def build_vocab(
    token_lists: Sequence[Sequence[str]],
    min_freq: int = 1,
    special_tokens: Optional[Sequence[str]] = None,
) -> Dict[str, int]:
    """토큰 목록으로부터 vocab을 생성한다.

    역할:
    - 자주 등장하는 단어에 인덱스를 부여한다.
    - 모델 입력은 문자열이 아니라 숫자여야 하므로 이 단계가 필요하다.

    기본 특수 토큰:
    - <pad>: padding용
    - <unk>: 사전에 없는 단어용

    반환:
        token -> index 형태의 딕셔너리
    """
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
    """토큰을 정수 인덱스로 바꾼다.

    역할:
    - vocab에 있는 토큰은 해당 인덱스로 변환한다.
    - vocab에 없는 토큰은 <unk> 인덱스로 변환한다.
    """
    unk_idx = vocab.get("<unk>", 1)
    return [vocab.get(token, unk_idx) for token in tokens]


# -----------------------------
# 5. padding
# -----------------------------
def pad_sequence(ids: Sequence[int], max_len: int, pad_idx: int = 0) -> List[int]:
    """시퀀스 길이를 고정 길이로 맞춘다.

    역할:
    - 문장 길이가 제각각이면 배치 학습이 어렵다.
    - padding을 통해 모든 문장을 같은 길이로 맞춘다.

    규칙:
    - 길이가 max_len보다 길면 자른다.
    - 길이가 max_len보다 짧으면 pad_idx로 채운다.
    """
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
    """데이터프레임 전체를 전처리한다.

    역할:
    - pandas DataFrame을 입력으로 받아 전처리 결과를 만든다.
    - 토큰, 정수 인코딩, padding까지 한 번에 처리한다.
    - torch Dataset으로 바로 넘기기 쉬운 컬럼을 생성한다.

    반환:
        processed_df: tokens / token_ids / padded_ids / length / label 포함 DataFrame
        vocab: 생성된 vocab 딕셔너리
    """
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
    processed["length"] = processed["token_ids"].map(len)
    processed["padded_ids"] = processed["token_ids"].map(lambda ids: pad_sequence(ids, max_len=max_len, pad_idx=pad_idx))

    # 6) label 정리
    processed["label"] = processed[label_col]

    return processed, vocab


# -----------------------------
# 7. torch Dataset
# -----------------------------
class KoreanSentimentDataset(Dataset):
    """한국어 감정분류용 PyTorch Dataset.

    역할:
    - 학습 루프에서 사용할 수 있도록 텐서 형태로 데이터를 제공한다.
    - __getitem__에서 (input_ids, label, length)를 반환한다.
    """

    def __init__(self, processed_df: pd.DataFrame):
        self.input_ids = torch.tensor(processed_df["padded_ids"].tolist(), dtype=torch.long)
        self.labels = torch.tensor(processed_df["label"].tolist(), dtype=torch.long)
        self.lengths = torch.tensor(processed_df["length"].tolist(), dtype=torch.long)

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, idx: int):
        return self.input_ids[idx], self.labels[idx], self.lengths[idx]