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