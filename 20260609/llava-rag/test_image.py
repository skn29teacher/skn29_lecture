import requests
import json
from utils import image_to_base64
from pathlib import Path

# ── 설정 ──────────────────────────────────────────
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llava:7b"
IMAGE_PATH = "images/page2_img1.png"   # ← 여기에 테스트 이미지 경로 입력
# ──────────────────────────────────────────────────


def ask_llava(prompt: str, image_path: str = None) -> str:
    """
    LLaVA에 텍스트(+이미지)를 보내고 응답을 받는 함수
    
    Args:
        prompt: 질문 텍스트
        image_path: 이미지 파일 경로 (None이면 텍스트만)
    
    Returns:
        LLaVA의 응답 텍스트
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,   # 스트리밍 OFF (단순 테스트용)
    }

    # 이미지가 있으면 Base64로 인코딩해서 추가
    if image_path and Path(image_path).exists():
        payload["images"] = [image_to_base64(image_path)]
        print(f"[INFO] 이미지 첨부: {image_path}")
    else:
        print("[INFO] 텍스트 전용 모드")

    print(f"[INFO] LLaVA에 요청 중... (CPU 환경에서는 30초~수분 소요)")
    
    response = requests.post(OLLAMA_URL, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        return result.get("response", "응답 없음")
    else:
        return f"오류 발생: {response.status_code} - {response.text}"


def main():
    # ── 테스트 1: 텍스트만 ──
    print("\n" + "="*50)
    print("테스트 1: 텍스트 질문")
    print("="*50)
    answer = ask_llava("안녕하세요! 간단히 자기소개 해주세요.")
    print(f"LLaVA 응답:\n{answer}")

    # ── 테스트 2: 이미지 + 텍스트 ──
    if Path(IMAGE_PATH).exists():
        print("\n" + "="*50)
        print("테스트 2: 이미지 분석")
        print("="*50)
        answer = ask_llava(
            prompt="이 이미지를 한국어로 자세히 설명해주세요. 어떤 내용이 담겨있나요?",
            image_path=IMAGE_PATH
        )
        print(f"LLaVA 응답:\n{answer}")
    else:
        print(f"\n[SKIP] 이미지 파일 없음: {IMAGE_PATH}")
        print("images/ 폴더에 page2_img1.png 파일을 넣고 다시 실행해보세요.")


if __name__ == "__main__":
    main()