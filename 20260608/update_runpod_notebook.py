import json

file_path = r'C:\Users\Playdata\Documents\20260605\Step2_Finetuning\RunPod_Finetuning_KoAlpaca.ipynb'

with open(file_path, 'r', encoding='utf-8') as f:
    d = json.load(f)

robust_code = """from peft import LoraConfig, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig

# k-bit 학습을 위한 준비 및 메모리 누수 방지(필수)
model = prepare_model_for_kbit_training(model)
model.config.use_cache = False  # 학습 중 메모리 터짐 방지

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# 최신 trl 라이브러리에 맞춘 SFTConfig (OOM 방지 설정 포함)
training_args = SFTConfig(
    output_dir="./qwen-koalpaca-lora",
    per_device_train_batch_size=4,   # 4 또는 8 유지
    gradient_accumulation_steps=4,
    gradient_checkpointing=True,     # [핵심] VRAM 폭발 방지
    learning_rate=2e-4,
    logging_steps=10,
    # max_steps=100,                 # 전체 학습을 위해 주석 처리
    num_train_epochs=1,              # 전체 데이터 1에폭 학습
    optim="paged_adamw_8bit",        # 8bit 옵티마이저로 VRAM 절약
    fp16=False,
    bf16=True,                       # H100 전용 bfloat16 가속
    dataset_text_field="text", 
    max_seq_length=1024,             # 문장 최대 길이 1024 고정
    packing=False                    # 텍스트 이어붙이기 방지
)

trainer = SFTTrainer(
    model=model,
    train_dataset=train_dataset,
    args=training_args,
    peft_config=lora_config
)

print("🚀 완벽한 메모리 방어 설정 완료! 학습 준비가 끝났습니다.")
"""

# Replace cell 8's content
d['cells'][8]['source'] = [robust_code]

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=1)

print("Successfully updated cell 8 in RunPod_Finetuning_KoAlpaca.ipynb")
