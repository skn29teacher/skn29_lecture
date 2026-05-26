from __future__ import annotations

import argparse
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from common import (
    MODEL_ID,
    SYSTEM_PROMPT,
    build_messages,
    decode_new_tokens_from_prompt_len,
    ensure_pad_token,
    load_dotenv_if_available,
    patch_exaone_embedding_access,
    prepare_chat_inputs,
    primary_device,
    print_cuda_memory,
    resolve_torch_dtype,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run inference with base EXAONE plus a LoRA adapter.")
    parser.add_argument("--model-id", default=MODEL_ID)
    parser.add_argument("--adapter-path", type=Path, default=Path("outputs/exaone35-2.4b-koqa-lora"))
    parser.add_argument("--prompt", default="한국어 Q&A 데이터셋을 만들 때 가장 중요한 점은 뭐야?")
    parser.add_argument("--system-prompt", default=SYSTEM_PROMPT)
    parser.add_argument("--max-new-tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--dtype", default="auto", choices=["auto", "bf16", "bfloat16", "fp16", "float16"])
    parser.add_argument("--qlora", action="store_true", help="Load base model in 4-bit for QLoRA adapters.")
    parser.add_argument("--show-full", action="store_true")
    args = parser.parse_args()

    load_dotenv_if_available()
    dtype = resolve_torch_dtype(torch, args.dtype)
    if dtype == torch.float32:
        dtype = torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else torch.float16

    tokenizer = AutoTokenizer.from_pretrained(args.model_id, trust_remote_code=True)
    ensure_pad_token(tokenizer)

    device_map = {"": 0} if torch.cuda.is_available() else None
    if args.qlora:
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=dtype,
        )
        base_model = AutoModelForCausalLM.from_pretrained(
            args.model_id,
            quantization_config=quantization_config,
            device_map=device_map,
            trust_remote_code=True,
            low_cpu_mem_usage=True,
        )
    else:
        base_model = AutoModelForCausalLM.from_pretrained(
            args.model_id,
            torch_dtype=dtype,
            device_map=device_map,
            trust_remote_code=True,
            low_cpu_mem_usage=True,
        )
    base_model = patch_exaone_embedding_access(base_model)

    model = PeftModel.from_pretrained(base_model, str(args.adapter_path))
    model.eval()

    messages = build_messages(args.prompt, args.system_prompt)
    inputs, prompt_length = prepare_chat_inputs(tokenizer, messages, primary_device(model))

    generation_kwargs = {
        "max_new_tokens": args.max_new_tokens,
        "pad_token_id": tokenizer.pad_token_id,
        "eos_token_id": tokenizer.eos_token_id,
    }
    if args.temperature > 0:
        generation_kwargs.update({"do_sample": True, "temperature": args.temperature})
    else:
        generation_kwargs.update({"do_sample": False})

    with torch.no_grad():
        output = model.generate(**inputs, **generation_kwargs)

    if args.show_full:
        print(tokenizer.decode(output[0], skip_special_tokens=False))
    else:
        print(decode_new_tokens_from_prompt_len(tokenizer, prompt_length, output))
    print_cuda_memory(torch)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
