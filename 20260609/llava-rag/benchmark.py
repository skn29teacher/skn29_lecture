"""
LLaVA (Phase C) vs BLIP+distilgpt2 (Phase 3 기초) 품질 비교
- 동일 이미지, 동일 질문으로 두 방식의 답변을 나란히 출력
"""
import requests
import time
from pathlib import Path
from transformers import pipeline as hf_pipeline
from PIL import Image
from utils import image_to_base64


OLLAMA_URL = "http://localhost:11434/api/generate"
LLAVA_MODEL = "llava:7b"


def ask_llava(question: str, image_path: str) -> tuple[str, float]:
    """LLaVA로 이미지 질의응답"""
    start = time.time()
    payload = {
        "model": LLAVA_MODEL,
        "prompt": question,
        "images": [image_to_base64(image_path)],
        "stream": False,
        "options": {"temperature": 0.3, "num_predict": 256}
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=300)
    elapsed = time.time() - start

    if response.status_code == 200:
        return response.json().get("response", ""), elapsed
    return f"오류: {response.status_code}", elapsed


def ask_blip(image_path: str) -> tuple[str, float]:
    """BLIP 캡셔닝 (기초 방식) - 질문 없이 캡션만 생성"""
    start = time.time()

    captioner = hf_pipeline(
        "image-text-to-text",
        model="Salesforce/blip-image-captioning-base"
    )
    result = captioner(image_path)
    elapsed = time.time() - start
    caption = result[0]["generated_text"] if result else ""
    return caption, elapsed


def run_benchmark(image_path: str, question: str):
    """단일 이미지에 대해 두 방식 비교"""
    print("\n" + "="*60)
    print(f"이미지: {image_path}")
    print(f"질문: {question}")
    print("="*60)

    # BLIP
    print("\n[BLIP - 기초 방식] 캡션 생성 중...")
    blip_answer, blip_time = ask_blip(image_path)
    print(f"소요 시간: {blip_time:.1f}초")
    print(f"답변: {blip_answer}")

    # LLaVA
    print(f"\n[LLaVA - 심화 방식] 답변 생성 중 (수분 소요)...")
    llava_answer, llava_time = ask_llava(question, image_path)
    print(f"소요 시간: {llava_time:.1f}초")
    print(f"답변: {llava_answer}")

    # 비교 요약
    print("\n[비교 요약]")
    print(f"  BLIP  | {blip_time:5.1f}초 | {blip_answer[:80]}...")
    print(f"  LLaVA | {llava_time:5.1f}초 | {llava_answer[:80]}...")


def main():
    image_files = list(Path("images").glob("*.jpg")) + list(Path("images").glob("*.png"))

    if not image_files:
        print("[ERROR] images/ 폴더에 이미지가 없습니다.")
        return

    # 첫 번째 이미지로 벤치마크
    test_image = str(image_files[0])

    benchmark_cases = [
        "이 이미지에서 무엇을 볼 수 있나요?",
        "이미지에 텍스트나 숫자가 있다면 읽어주세요.",
        "이미지의 주요 내용을 3줄로 요약해주세요.",
    ]

    for question in benchmark_cases:
        run_benchmark(test_image, question)


if __name__ == "__main__":
    main()