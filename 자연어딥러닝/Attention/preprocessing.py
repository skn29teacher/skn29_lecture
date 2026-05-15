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