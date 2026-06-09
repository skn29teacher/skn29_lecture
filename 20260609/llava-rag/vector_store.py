import chromadb
from chromadb.config import Settings
from pathlib import Path
from embedder import CLIPEmbedder
from utils import image_to_base64


class ImageVectorStore:
    """
    ChromaDB 기반 이미지 벡터 저장소
    - 이미지를 CLIP 벡터로 저장
    - 텍스트 쿼리 또는 이미지 쿼리로 유사 이미지 검색
    """

    def __init__(
        self,
        embedder: CLIPEmbedder,
        db_path: str = "./chroma_db",
        collection_name: str = "image_collection"
    ):
        self.embedder = embedder

        # ChromaDB 영구 저장 클라이언트
        self.client = chromadb.PersistentClient(path=db_path)

        # 컬렉션 가져오기 또는 생성
        # cosine 거리 → CLIP L2 정규화 벡터에 최적
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"[INFO] VectorDB 초기화 완료: {db_path}/{collection_name}")
        print(f"[INFO] 현재 저장된 이미지 수: {self.collection.count()}")

    # ── 저장 ──────────────────────────────────────────────────────────

    def add_image(self, image_path: str, metadata: dict = None) -> str:
        """
        이미지 1개를 임베딩하여 DB에 저장
        
        Args:
            image_path: 이미지 파일 경로
            metadata: 추가 메타데이터 (파일명, 설명 등)
        
        Returns:
            저장된 문서 ID
        """
        path = Path(image_path)
        doc_id = path.stem   # 파일명(확장자 제외)을 ID로 사용

        # 이미 저장된 경우 스킵
        existing = self.collection.get(ids=[doc_id])
        if existing["ids"]:
            print(f"[SKIP] 이미 저장됨: {doc_id}")
            return doc_id

        # CLIP으로 이미지 임베딩
        embedding = self.embedder.embed_image(image_path)

        # 메타데이터 구성
        meta = {
            "file_name": path.name,
            "file_path": str(path.absolute()),
            "file_ext": path.suffix,
        }
        if metadata:
            meta.update(metadata)

        # ChromaDB에 저장
        # documents 필드: 이미지 경로를 텍스트로 저장 (검색 결과 참조용)
        self.collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[str(path.absolute())],
            metadatas=[meta]
        )
        print(f"[OK] 저장 완료: {doc_id} ({path.name})")
        return doc_id

    def add_images_from_folder(self, folder_path: str) -> list[str]:
        """
        폴더 내 모든 이미지를 일괄 저장
        
        Args:
            folder_path: 이미지가 담긴 폴더 경로
        
        Returns:
            저장된 문서 ID 리스트
        """
        folder = Path(folder_path)
        extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
        image_files = [f for f in folder.iterdir() if f.suffix.lower() in extensions]

        if not image_files:
            print(f"[WARN] 이미지 파일 없음: {folder_path}")
            return []

        print(f"[INFO] {len(image_files)}개 이미지 발견 → 임베딩 시작")
        ids = []
        for image_file in image_files:
            doc_id = self.add_image(str(image_file))
            ids.append(doc_id)

        print(f"[INFO] 총 {len(ids)}개 저장 완료. DB 총 이미지: {self.collection.count()}")
        return ids

    # ── 검색 ──────────────────────────────────────────────────────────

    def search_by_text(self, query_text: str, top_k: int = 3) -> list[dict]:
        """
        텍스트 쿼리로 유사한 이미지 검색 (핵심 기능!)
        예: "강아지 사진" → 강아지가 찍힌 이미지 반환
        
        Args:
            query_text: 검색 텍스트
            top_k: 반환할 결과 수
        
        Returns:
            유사도 순으로 정렬된 이미지 정보 리스트
        """
        # 텍스트를 이미지와 동일한 벡터 공간으로 임베딩
        query_embedding = self.embedder.embed_text(query_text)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, self.collection.count()),
            include=["documents", "metadatas", "distances"]
        )

        return self._format_results(results)

    def search_by_image(self, query_image_path: str, top_k: int = 3) -> list[dict]:
        """
        이미지 쿼리로 유사한 이미지 검색
        예: 특정 이미지 → 비슷한 이미지들 반환
        
        Args:
            query_image_path: 쿼리 이미지 경로
            top_k: 반환할 결과 수
        
        Returns:
            유사도 순으로 정렬된 이미지 정보 리스트
        """
        query_embedding = self.embedder.embed_image(query_image_path)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, self.collection.count()),
            include=["documents", "metadatas", "distances"]
        )

        return self._format_results(results)

    def _format_results(self, raw_results: dict) -> list[dict]:
        """ChromaDB 결과를 깔끔한 딕셔너리 리스트로 변환"""
        formatted = []
        ids = raw_results["ids"][0]
        docs = raw_results["documents"][0]
        metas = raw_results["metadatas"][0]
        distances = raw_results["distances"][0]

        for doc_id, doc, meta, dist in zip(ids, docs, metas, distances):
            # cosine distance → similarity (0~1, 높을수록 유사)
            similarity = 1 - dist
            formatted.append({
                "id": doc_id,
                "file_path": doc,
                "file_name": meta.get("file_name", ""),
                "similarity": round(similarity, 4),
                "metadata": meta
            })

        return formatted

    def get_stats(self) -> dict:
        """DB 현황 조회"""
        return {
            "total_images": self.collection.count(),
            "collection_name": self.collection.name,
        }