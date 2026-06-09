from embedder import CLIPEmbedder
from vector_store import ImageVectorStore
from pathlib import Path


def main():
    # ── 초기화 ────────────────────────────────────────────────────────
    embedder = CLIPEmbedder()               # CLIP 모델 로드
    store = ImageVectorStore(embedder)      # ChromaDB 연결

    # ── Step 1: images/ 폴더의 모든 이미지 저장 ────────────────────────
    print("\n" + "="*50)
    print("Step 1: 이미지 임베딩 & DB 저장")
    print("="*50)

    if not Path("images").exists():
        print("[WARN] images/ 폴더가 없습니다. 생성합니다.")
        Path("images").mkdir()
        print("images/ 폴더에 이미지를 넣고 다시 실행하세요.")
        return

    store.add_images_from_folder("images")
    print(f"\nDB 현황: {store.get_stats()}")

    # ── Step 2: 텍스트로 이미지 검색 ───────────────────────────────────
    print("\n" + "="*50)
    print("Step 2: 텍스트 쿼리로 이미지 검색")
    print("="*50)

    # 원하는 검색어로 변경하세요
    text_queries = [
        "a chart or graph",        # 차트/그래프
        "a cat or dog",            # 동물
        "text document",           # 문서
    ]

    for query in text_queries:
        print(f"\n 쿼리: '{query}'")
        results = store.search_by_text(query, top_k=2)

        if results:
            for i, r in enumerate(results, 1):
                print(f"  {i}. {r['file_name']} (유사도: {r['similarity']:.4f})")
        else:
            print("  결과 없음")

    # ── Step 3: 이미지로 유사 이미지 검색 ──────────────────────────────
    print("\n" + "="*50)
    print("Step 3: 이미지 쿼리로 유사 이미지 검색")
    print("="*50)

    image_files = list(Path("images").glob("*.jpg")) + list(Path("images").glob("*.png"))

    if len(image_files) >= 2:
        query_img = str(image_files[0])
        print(f" 쿼리 이미지: {query_img}")
        results = store.search_by_image(query_img, top_k=3)

        for i, r in enumerate(results, 1):
            print(f"  {i}. {r['file_name']} (유사도: {r['similarity']:.4f})")
    else:
        print("[SKIP] 이미지가 2개 이상 있어야 유사 이미지 검색 테스트 가능합니다.")


if __name__ == "__main__":
    main()