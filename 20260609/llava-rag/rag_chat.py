from rag_pipeline import MultimodalRAGPipeline
from vector_store import ImageVectorStore
from embedder import CLIPEmbedder
from pathlib import Path


def index_images(pipeline: MultimodalRAGPipeline, folder: str = "images"):
    """실행 시 images/ 폴더 자동 인덱싱"""
    print(f"\n[INDEX] '{folder}' 폴더 이미지 인덱싱 중...")
    pipeline.store.add_images_from_folder(folder)
    stats = pipeline.store.get_stats()
    print(f"[INDEX] 완료 - 총 {stats['total_images']}개 이미지 인덱싱됨")


def print_result(result: dict):
    """RAG 결과 출력"""
    print("\n" + "-"*60)
    print("[검색된 이미지]")
    if result["retrieved_images"]:
        for i, img in enumerate(result["retrieved_images"], 1):
            print(f"  {i}. {img['file_name']} (유사도: {img['similarity']:.4f})")
    else:
        print("  없음")

    print("\n[LLaVA 답변]")
    print(result["answer"])
    print("-"*60)


def main():
    # 파이프라인 초기화
    pipeline = MultimodalRAGPipeline(
        top_k=2   # 상위 2개 이미지 검색 후 LLaVA에 주입
    )

    # images/ 폴더 이미지 인덱싱
    if Path("images").exists():
        index_images(pipeline)
    else:
        print("[WARN] images/ 폴더 없음. 이미지를 추가한 뒤 다시 실행하세요.")
        return

    # 대화 루프
    print("\n" + "="*60)
    print("로컬 멀티모달 RAG 시스템 준비 완료")
    print("종료: 'q' 또는 'quit' 입력")
    print("="*60)

    while True:
        try:
            question = input("\n질문을 입력하세요: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n종료합니다.")
            break

        if not question:
            continue
        if question.lower() in ("q", "quit", "exit"):
            print("종료합니다.")
            break

        result = pipeline.query(question)
        print_result(result)


if __name__ == "__main__":
    main()