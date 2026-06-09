from rag_pipeline import MultimodalRAGPipeline
from pathlib import Path


def print_result(result: dict):
    print("\n" + "-"*60)

    print("[검색된 문서 청크]")
    if result["retrieved_texts"]:
        for i, t in enumerate(result["retrieved_texts"], 1):
            preview = t["text"][:80].replace("\n", " ")
            print(f"  {i}. [{t['source']}] 유사도: {t['similarity']:.4f}")
            print(f"     {preview}...")
    else:
        print("  없음")

    print("\n[검색된 이미지]")
    if result["retrieved_images"]:
        for i, img in enumerate(result["retrieved_images"], 1):
            print(f"  {i}. {img['file_name']} (유사도: {img['similarity']:.4f})")
    else:
        print("  없음")

    print("\n[LLaVA 답변]")
    print(result["answer"])
    print("-"*60)


def main():
    pipeline = MultimodalRAGPipeline(top_k_text=3, top_k_image=2)

    # 문서 인덱싱
    if Path("docs").exists():
        print("[INDEX] docs/ 폴더 문서 인덱싱 중...")
        pipeline.text_store.add_documents_from_folder("docs")
    else:
        Path("docs").mkdir()
        print("[INFO] docs/ 폴더를 생성했습니다. PDF 또는 txt 파일을 넣어주세요.")

    # 이미지 인덱싱
    if Path("images").exists():
        print("[INDEX] images/ 폴더 이미지 인덱싱 중...")
        pipeline.image_store.add_images_from_folder("images")
    else:
        print("[WARN] images/ 폴더 없음")

    print("\n" + "="*60)
    print("멀티모달 RAG 시스템 준비 완료 (텍스트 + 이미지)")
    print("종료: q 입력")
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