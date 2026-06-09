import requests
from pathlib import Path
from embedder import CLIPEmbedder
from vector_store import ImageVectorStore
from utils import image_to_base64


class MultimodalRAGPipeline:
    """
    End-to-End 로컬 멀티모달 RAG 파이프라인
    
    흐름:
      1. 사용자 질문 수신
      2. CLIP으로 질문 임베딩 → ChromaDB 검색
      3. 유사 이미지 Top-K 검색
      4. 이미지(Base64) + 질문 → LLaVA 주입
      5. 최종 답변 반환
    """

    def __init__(
        self,
        ollama_url: str = "http://localhost:11434/api/generate",
        model_name: str = "llava:7b",
        db_path: str = "./chroma_db",
        top_k: int = 2,
    ):
        self.ollama_url = ollama_url
        self.model_name = model_name
        self.top_k = top_k

        print("[INFO] RAG 파이프라인 초기화 중...")
        self.embedder = CLIPEmbedder()
        self.store = ImageVectorStore(self.embedder, db_path=db_path)
        print("[INFO] RAG 파이프라인 준비 완료")

    # ── Step 1: 검색 ──────────────────────────────────────────────────

    def retrieve(self, query: str) -> list[dict]:
        """
        텍스트 쿼리로 ChromaDB에서 유사 이미지 검색

        Args:
            query: 사용자 질문 텍스트

        Returns:
            유사도 순 이미지 정보 리스트
        """
        print(f"\n[RETRIEVE] 쿼리: '{query}'")
        results = self.store.search_by_text(query, top_k=self.top_k)

        if not results:
            print("[RETRIEVE] 검색 결과 없음")
            return []

        for i, r in enumerate(results, 1):
            print(f"  {i}. {r['file_name']} (유사도: {r['similarity']:.4f})")

        return results

    # ── Step 2: 생성 ──────────────────────────────────────────────────

    def generate(self, query: str, retrieved_images: list[dict]) -> str:
        """
        검색된 이미지 + 질문을 LLaVA에 주입하여 답변 생성

        Args:
            query: 사용자 질문
            retrieved_images: retrieve()에서 반환된 이미지 리스트

        Returns:
            LLaVA 생성 답변
        """
        if not retrieved_images:
            return self._generate_text_only(query)

        # 유사도 임계값 필터 (0.2 미만은 관련 없는 이미지로 판단)
        SIMILARITY_THRESHOLD = 0.2
        valid_images = [r for r in retrieved_images if r["similarity"] >= SIMILARITY_THRESHOLD]

        if not valid_images:
            print("[GENERATE] 유사도 임계값 미달 - 텍스트 전용 모드로 전환")
            return self._generate_text_only(query)

        # 이미지들을 Base64로 인코딩
        images_b64 = []
        used_files = []
        for r in valid_images:
            file_path = r["file_path"]
            if Path(file_path).exists():
                images_b64.append(image_to_base64(file_path))
                used_files.append(r["file_name"])
            else:
                print(f"[WARN] 파일 없음: {file_path}")

        if not images_b64:
            return self._generate_text_only(query)

        print(f"[GENERATE] LLaVA에 이미지 {len(images_b64)}장 + 질문 주입 중...")
        print(f"[GENERATE] 사용 이미지: {used_files}")

        # 프롬프트 구성
        prompt = self._build_prompt(query, used_files)

        # Ollama API 호출
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "images": images_b64,
            "stream": False,
            "options": {
                "temperature": 0.3,    # 낮을수록 일관된 답변 (RAG에 적합)
                "num_predict": 512,    # 최대 생성 토큰 수
            }
        }

        response = requests.post(self.ollama_url, json=payload, timeout=300)

        if response.status_code == 200:
            answer = response.json().get("response", "응답 없음")
            return answer
        else:
            return f"LLaVA 오류: {response.status_code} - {response.text}"

    def _generate_text_only(self, query: str) -> str:
        """이미지 없이 텍스트만으로 LLaVA에 질문"""
        print("[GENERATE] 텍스트 전용 모드")
        payload = {
            "model": self.model_name,
            "prompt": query,
            "stream": False,
            "options": {"temperature": 0.3, "num_predict": 512}
        }
        response = requests.post(self.ollama_url, json=payload, timeout=300)
        if response.status_code == 200:
            return response.json().get("response", "응답 없음")
        return f"LLaVA 오류: {response.status_code}"

    def _build_prompt(self, query: str, image_names: list[str]) -> str:
        """RAG 프롬프트 구성"""
        image_list = ", ".join(image_names)
        prompt = f"""You are a helpful assistant analyzing images.

The following image(s) were retrieved as relevant context: {image_list}

Please analyze the provided image(s) carefully and answer the following question in Korean:

Question: {query}

Answer based on what you actually see in the image(s). Be specific and detailed."""
        return prompt

    # ── 통합 실행 ─────────────────────────────────────────────────────

    def query(self, question: str) -> dict:
        """
        RAG 파이프라인 전체 실행 (외부에서 호출하는 메인 메서드)

        Args:
            question: 사용자 질문

        Returns:
            {
              "question": str,
              "retrieved_images": list,
              "answer": str
            }
        """
        print("\n" + "="*60)
        print(f"질문: {question}")
        print("="*60)

        # 1. 검색
        retrieved = self.retrieve(question)

        # 2. 생성
        answer = self.generate(question, retrieved)

        return {
            "question": question,
            "retrieved_images": retrieved,
            "answer": answer
        }