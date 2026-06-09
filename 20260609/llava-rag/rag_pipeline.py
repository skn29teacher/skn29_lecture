import requests
from pathlib import Path
from embedder import CLIPEmbedder
from vector_store import ImageVectorStore
from text_store import TextVectorStore
from utils import image_to_base64


class MultimodalRAGPipeline:
    """
    완전한 멀티모달 RAG 파이프라인

    흐름:
      1. 사용자 질문 수신
      2. 텍스트 검색 (text_collection) → 관련 문장/단락
      3. 이미지 검색 (image_collection) → 관련 이미지
      4. 문장 컨텍스트 + 이미지 → LLaVA 주입
      5. 최종 답변 반환
    """

    SIMILARITY_THRESHOLD = 0.2

    def __init__(
        self,
        ollama_url: str = "http://localhost:11434/api/generate",
        model_name: str = "llava:7b",
        db_path: str = "./chroma_db",
        top_k_text: int = 3,
        top_k_image: int = 2,
    ):
        self.ollama_url = ollama_url
        self.model_name = model_name
        self.top_k_text = top_k_text
        self.top_k_image = top_k_image

        print("[INFO] RAG 파이프라인 초기화 중...")
        self.embedder = CLIPEmbedder()
        self.image_store = ImageVectorStore(self.embedder, db_path=db_path)
        self.text_store = TextVectorStore(db_path=db_path)
        print("[INFO] RAG 파이프라인 준비 완료\n")

    # ── 검색 ──────────────────────────────────────────────────────────

    def retrieve(self, query: str) -> dict:
        """
        텍스트 + 이미지 동시 검색

        Returns:
            {"texts": [...], "images": [...]}
        """
        print(f"[RETRIEVE] 쿼리: '{query}'")

        # 텍스트 검색
        text_results = self.text_store.search(query, top_k=self.top_k_text)
        print(f"[RETRIEVE] 텍스트 청크 {len(text_results)}개 검색됨")
        for i, r in enumerate(text_results, 1):
            preview = r["text"][:60].replace("\n", " ")
            print(f"  {i}. [{r['source']}] 유사도: {r['similarity']:.4f} | {preview}...")

        # 이미지 검색
        image_results = self.image_store.search_by_text(query, top_k=self.top_k_image)
        print(f"[RETRIEVE] 이미지 {len(image_results)}개 검색됨")
        for i, r in enumerate(image_results, 1):
            print(f"  {i}. {r['file_name']} (유사도: {r['similarity']:.4f})")

        return {"texts": text_results, "images": image_results}

    # ── 생성 ──────────────────────────────────────────────────────────

    def generate(self, query: str, retrieved: dict) -> str:
        """
        검색된 텍스트 + 이미지를 LLaVA에 주입하여 답변 생성

        Args:
            query: 사용자 질문
            retrieved: retrieve()의 반환값

        Returns:
            LLaVA 생성 답변
        """
        text_results = retrieved.get("texts", [])
        image_results = retrieved.get("images", [])

        # 유사도 임계값 필터
        valid_texts = [r for r in text_results if r["similarity"] >= self.SIMILARITY_THRESHOLD]
        valid_images = [r for r in image_results if r["similarity"] >= self.SIMILARITY_THRESHOLD]

        # 텍스트 컨텍스트 구성
        context_text = ""
        if valid_texts:
            chunks = [f"[출처: {r['source']}]\n{r['text']}" for r in valid_texts]
            context_text = "\n\n".join(chunks)

        # 이미지 Base64 인코딩
        images_b64 = []
        used_image_names = []
        for r in valid_images:
            if Path(r["file_path"]).exists():
                images_b64.append(image_to_base64(r["file_path"]))
                used_image_names.append(r["file_name"])

        print(f"\n[GENERATE] 텍스트 청크 {len(valid_texts)}개 + 이미지 {len(images_b64)}장 → LLaVA 주입")

        # 프롬프트 구성
        prompt = self._build_prompt(query, context_text, used_image_names)

        # Ollama API 호출
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 512,
            }
        }

        if images_b64:
            payload["images"] = images_b64

        print("[GENERATE] LLaVA 응답 대기 중 (CPU 환경에서 수분 소요)...")
        response = requests.post(self.ollama_url, json=payload, timeout=300)

        if response.status_code == 200:
            return response.json().get("response", "응답 없음")
        return f"LLaVA 오류: {response.status_code} - {response.text}"

    def _build_prompt(
        self,
        query: str,
        context_text: str,
        image_names: list[str]
    ) -> str:
        """텍스트 컨텍스트 + 이미지 정보를 포함한 RAG 프롬프트"""

        prompt_parts = ["You are a helpful assistant. Answer in Korean.\n"]

        if context_text:
            prompt_parts.append(
                f"[검색된 문서 컨텍스트]\n{context_text}\n"
            )

        if image_names:
            prompt_parts.append(
                f"[첨부 이미지]\n{', '.join(image_names)}\n"
                "위 이미지를 직접 분석하여 답변에 활용하세요.\n"
            )

        prompt_parts.append(f"[질문]\n{query}")

        return "\n".join(prompt_parts)

    # ── 통합 실행 ─────────────────────────────────────────────────────

    def query(self, question: str) -> dict:
        """RAG 파이프라인 전체 실행"""
        print("\n" + "="*60)
        print(f"질문: {question}")
        print("="*60)

        retrieved = self.retrieve(question)
        answer = self.generate(question, retrieved)

        return {
            "question": question,
            "retrieved_texts": retrieved["texts"],
            "retrieved_images": retrieved["images"],
            "answer": answer
        }