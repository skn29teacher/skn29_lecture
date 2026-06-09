import base64
from pathlib import Path


def image_to_base64(image_path: str) -> str:
    """이미지 파일을 Base64 문자열로 변환"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def load_image_bytes(image_path: str) -> bytes:
    """이미지 파일을 bytes로 로드"""
    with open(image_path, "rb") as f:
        return f.read()