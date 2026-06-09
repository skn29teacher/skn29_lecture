import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformer


class TextVectorStore:
    """
    문서(PDF/TXT)를 청크로 분할하여 ChromaDB에 저장하고 검색하는 클래스

    - 임베딩 모델: sentence-transformers (paraphrase-multilingual, 한국어 지원)
    - 저장 단위: 문장 단위 청크 (overlap 포함)
    """

    SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}

    def __init__(
        self,
        db_path: str = "./chroma_db",
        collection_name: str = "text_collection",
        embed_model: str = "paraphrase-multilingual-MiniLM-L12-v2",  # 한국어 지원
        chunk_size: int = 300,      # 청크당 최대 글자 수
        chunk_overlap: int = 50,    # 청크 간 겹치는 글자 수
    ):
        print(f"[INFO] 텍스트 임베딩 모델 로딩 중: {embed_model}")
        self.embedder = SentenceTransformer(embed_model)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"[INFO] 텍스트 DB 초기화 완료 - 저장된 청크 수: {self.collection.count()}")

    # ── 텍스트 추출 ────────────────────────────────────────────────────

    def _extract_text_from_file(self, file_path: str) -> str:
        """파일에서 텍스트 추출 (txt / pdf 지원)"""
        path = Path(file_path)

        if path.suffix.lower() == ".pdf":
            return self._extract_from_pdf(file_path)
        elif path.suffix.lower() in (".txt", ".md"):
            return path.read_text(encoding="utf-8", errors="ignore")
        else:
            raise ValueError(f"지원하지 않는 파일 형식: {path.suffix}")

    def _extract_from_pdf(self, file_path: str) -> str:
        """PDF에서 텍스트 추출"""
        try:
            import pdfplumber
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except ImportError:
            raise ImportError("PDF 처리를 위해 설치 필요: pip install pdfplumber")

    # ── 청크 분할 ──────────────────────────────────────────────────────

    def _split_into_chunks(self, text: str, source_name: str) -> list[dict]:
        """
        텍스트를 chunk_size 단위로 분할 (overlap 포함)

        Returns:
            [{"text": str, "chunk_id": str, "source": str, "chunk_index": int}, ...]
        """
        # 빈 줄 기준으로 1차 분할 후 재조합
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        chunks = []
        current_chunk = ""
        chunk_index = 0

        for para in paragraphs:
            # 현재 청크에 추가했을 때 chunk_size 초과하면 저장 후 새 청크 시작
            if len(current_chunk) + len(para) > self.chunk_size and current_chunk:
                chunks.append({
                    "text": current_chunk.strip(),
                    "chunk_id": f"{source_name}__chunk_{chunk_index}",
                    "source": source_name,
                    "chunk_index": chunk_index
                })
                # overlap: 이전 청크 끝부분을 다음 청크 시작에 포함
                current_chunk = current_chunk[-self.chunk_overlap:] + " " + para
                chunk_index += 1
            else:
                current_chunk += " " + para

        # 마지막 남은 청크 저장
        if current_chunk.strip():
            chunks.append({
                "text": current_chunk.strip(),
                "chunk_id": f"{source_name}__chunk_{chunk_index}",
                "source": source_name,
                "chunk_index": chunk_index
            })

        return chunks

    # ── 저장 ──────────────────────────────────────────────────────────

    def add_document(self, file_path: str) -> int:
        """
        문서 1개를 청크로 분할하여 ChromaDB에 저장

        Returns:
            저장된 청크 수
        """
        path = Path(file_path)
        source_name = path.stem

        # 이미 인덱싱된 문서인지 확인
        existing = self.collection.get(where={"source": source_name})
        if existing["ids"]:
            print(f"[SKIP] 이미 인덱싱됨: {source_name} ({len(existing['ids'])}개 청크)")
            return 0

        print(f"[INFO] 문서 처리 중: {path.name}")
        text = self._extract_text_from_file(file_path)

        if not text.strip():
            print(f"[WARN] 텍스트 추출 실패 또는 빈 문서: {file_path}")
            return 0

        chunks = self._split_into_chunks(text, source_name)
        print(f"[INFO] {len(chunks)}개 청크로 분할됨")

        # 임베딩 생성
        texts = [c["text"] for c in chunks]
        embeddings = self.embedder.encode(texts, show_progress_bar=True).tolist()

        # ChromaDB 저장
        self.collection.add(
            ids=[c["chunk_id"] for c in chunks],
            embeddings=embeddings,
            documents=texts,
            metadatas=[{
                "source": c["source"],
                "chunk_index": c["chunk_index"],
                "file_path": str(path.absolute())
            } for c in chunks]
        )

        print(f"[OK] 저장 완료: {source_name} ({len(chunks)}개 청크)")
        return len(chunks)

    def add_documents_from_folder(self, folder_path: str) -> int:
        """폴더 내 모든 문서 일괄 저장"""
        folder = Path(folder_path)
        files = [
            f for f in folder.iterdir()
            if f.suffix.lower() in self.SUPPORTED_EXTENSIONS
        ]

        if not files:
            print(f"[WARN] 지원 문서 없음: {folder_path}")
            return 0

        print(f"[INFO] {len(files)}개 문서 발견")
        total = sum(self.add_document(str(f)) for f in files)
        print(f"[INFO] 총 {total}개 청크 저장 완료")
        return total

    # ── 검색 ──────────────────────────────────────────────────────────

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """
        텍스트 쿼리로 유사 청크 검색

        Returns:
            [{"text": str, "source": str, "chunk_index": int, "similarity": float}, ...]
        """
        if self.collection.count() == 0:
            return []

        query_embedding = self.embedder.encode([query]).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=min(top_k, self.collection.count()),
            include=["documents", "metadatas", "distances"]
        )

        formatted = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            formatted.append({
                "text": doc,
                "source": meta.get("source", ""),
                "chunk_index": meta.get("chunk_index", 0),
                "file_path": meta.get("file_path", ""),
                "similarity": round(1 - dist, 4)
            })

        return formatted

    def get_stats(self) -> dict:
        return {"total_chunks": self.collection.count()}