import open_clip
import torch
from PIL import Image
from pathlib import Path
import numpy as np


class CLIPEmbedder:
    """
    OpenCLIP 기반 멀티모달 임베더
    - 이미지와 텍스트를 동일한 512차원 벡터 공간에 임베딩
    - 즉, 텍스트 쿼리로 이미지 검색 가능!
    """

    def __init__(self, model_name: str = "ViT-B-32", pretrained: str = "openai"):
        print(f"[INFO] CLIP 모델 로딩 중: {model_name} ({pretrained})...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[INFO] 디바이스: {self.device}")

        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            model_name,
            pretrained=pretrained,
            device=self.device
        )
        self.tokenizer = open_clip.get_tokenizer(model_name)
        self.model.eval()
        print("[INFO] CLIP 모델 로딩 완료!")

    def embed_image(self, image_path: str) -> list[float]:
        """
        이미지 파일 → 512차원 벡터 반환
        
        Args:
            image_path: 이미지 파일 경로
        
        Returns:
            512차원 float 리스트
        """
        image = self.preprocess(
            Image.open(image_path).convert("RGB")
        ).unsqueeze(0).to(self.device)

        with torch.no_grad():
            features = self.model.encode_image(image)
            # L2 정규화 → 코사인 유사도 검색에 최적화
            features = features / features.norm(dim=-1, keepdim=True)

        return features.cpu().numpy()[0].tolist()

    def embed_text(self, text: str) -> list[float]:
        """
        텍스트 → 512차원 벡터 반환 (이미지 벡터와 동일 공간!)
        
        Args:
            text: 임베딩할 텍스트
        
        Returns:
            512차원 float 리스트
        """
        tokens = self.tokenizer([text]).to(self.device)

        with torch.no_grad():
            features = self.model.encode_text(tokens)
            features = features / features.norm(dim=-1, keepdim=True)

        return features.cpu().numpy()[0].tolist()

    def embed_images_batch(self, image_paths: list[str]) -> list[list[float]]:
        """
        여러 이미지를 한 번에 임베딩 (배치 처리)
        
        Args:
            image_paths: 이미지 경로 리스트
        
        Returns:
            벡터 리스트
        """
        embeddings = []
        for idx, path in enumerate(image_paths):
            print(f"[INFO] 임베딩 중 ({idx+1}/{len(image_paths)}): {path}")
            embeddings.append(self.embed_image(path))
        return embeddings