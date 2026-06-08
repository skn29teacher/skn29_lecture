# # Windows/Mac 로컬 환경 패키지 설치
# !pip install huggingface_hub gguf
# # Windows C++ 빌드 에러를 방지하기 위해 사전 컴파일된 CPU 전용 버전을 설치합니다.
# !pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu

# # 모델을 GGUF로 변환해 주는 공식 스크립트를 쓰기 위해 llama.cpp 저장소 다운로드
# !git clone https://github.com/ggerganov/llama.cpp.git

# !python -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('Qwen/Qwen2.5-0.5B-Instruct').save_pretrained('./Qwen-KoAlpaca-Merged')"

# # 모델을 FP16 정밀도의 GGUF 포맷으로 변환합니다.
# !python llama.cpp/convert_hf_to_gguf.py ./Qwen-KoAlpaca-Merged --outtype f16 --outfile qwen_koalpaca_fp16.gguf

# 로컬 CPU 고속 추론 테스트
from llama_cpp import Llama
import sys

# GGUF 모델 로드(GPU가 없어도 CPU 단일 멀티코어를 활용해 고속으로 구동)
llm = Llama(
    model_path='./qwen_koalpaca_fp16.gguf',
    n_ctx=1024,
    n_threads=4,
    verbose=False
)

if __name__=="__main__":
    prompt = '프랑스 파리를 여행하려고 해. 꼭 가봐야 할 명소를 두 곳만 추천해줘'
    # 파인튜닝 시 학습했던 Qwen Chat Template 포맷을 그대로 입력합니다.
    formatted_prompt = f"<|im_start|>system\nYou are a helpful AI assistant. Respond in Korean.<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"

    print('답변 생성중.....(cpu 추론)')
    output = llm(
        formatted_prompt,
        max_tokens=150,
        temperature=0.7,
        stop = ["<|im_end|>"]
    )
    print('파인튜닝 완료 모델의 답변')
    print(output['choices'][0]['text'].stip())
