from __future__ import annotations

import os
import types
from typing import Any

MODEL_ID = os.getenv("MODEL_ID", "LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct")
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "You are EXAONE model from LG AI Research, a helpful assistant.",
)
EXAONE_LORA_TARGET_MODULES = ["q_proj", "k_proj", "v_proj", "out_proj", "c_fc_0", "c_fc_1", "c_proj"]


def load_dotenv_if_available() -> None:
    if os.getenv("DISABLE_DOTENV") == "1":
        return

    try:
        from dotenv import load_dotenv
    except Exception:
        return

    load_dotenv()


def resolve_torch_dtype(torch: Any, dtype: str = "auto") -> Any:
    dtype = dtype.lower()
    if dtype == "auto":
        if torch.cuda.is_available() and torch.cuda.is_bf16_supported():
            return torch.bfloat16
        if torch.cuda.is_available():
            return torch.float16
        return torch.float32
    if dtype in {"bf16", "bfloat16"}:
        return torch.bfloat16
    if dtype in {"fp16", "float16"}:
        return torch.float16
    if dtype in {"fp32", "float32"}:
        return torch.float32
    raise ValueError(f"Unsupported dtype: {dtype}")


def ensure_pad_token(tokenizer: Any) -> None:
    if tokenizer.pad_token_id is None:
        if tokenizer.eos_token is not None:
            tokenizer.pad_token = tokenizer.eos_token
        else:
            tokenizer.add_special_tokens({"pad_token": "<|pad|>"})


def primary_device(model: Any) -> Any:
    return next(model.parameters()).device


def print_cuda_memory(torch: Any, label: str = "cuda") -> None:
    if not torch.cuda.is_available():
        print(f"{label}_memory_allocated_gb: 0.000")
        return
    allocated = torch.cuda.memory_allocated() / 1024**3
    reserved = torch.cuda.memory_reserved() / 1024**3
    print(f"{label}_memory_allocated_gb: {allocated:.3f}")
    print(f"{label}_memory_reserved_gb: {reserved:.3f}")


def build_messages(prompt: str, system_prompt: str | None = None) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": system_prompt or SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]


def decode_new_tokens(tokenizer: Any, input_ids: Any, output_ids: Any) -> str:
    new_tokens = output_ids[0][input_ids.shape[-1] :]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()


def prepare_chat_inputs(tokenizer: Any, messages: list[dict[str, str]], device: Any) -> tuple[dict[str, Any], int]:
    encoded = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
        return_dict=True,
    )
    encoded = encoded.to(device)
    return dict(encoded), encoded["input_ids"].shape[-1]


def decode_new_tokens_from_prompt_len(tokenizer: Any, prompt_length: int, output_ids: Any) -> str:
    new_tokens = output_ids[0][prompt_length:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()


def patch_exaone_embedding_access(model: Any) -> Any:
    """Expose EXAONE's transformer.wte/lm_head to PEFT and gradient checkpointing."""
    if not hasattr(model, "transformer") or not hasattr(model.transformer, "wte"):
        return model

    def get_input_embeddings_for_lm(self: Any) -> Any:
        return self.transformer.wte

    def set_input_embeddings_for_lm(self: Any, value: Any) -> None:
        self.transformer.wte = value

    def get_output_embeddings_for_lm(self: Any) -> Any:
        return self.lm_head

    def set_output_embeddings_for_lm(self: Any, value: Any) -> None:
        self.lm_head = value

    def get_input_embeddings_for_base(self: Any) -> Any:
        return self.wte

    def set_input_embeddings_for_base(self: Any, value: Any) -> None:
        self.wte = value

    model.get_input_embeddings = types.MethodType(get_input_embeddings_for_lm, model)
    model.set_input_embeddings = types.MethodType(set_input_embeddings_for_lm, model)
    if hasattr(model, "lm_head"):
        model.get_output_embeddings = types.MethodType(get_output_embeddings_for_lm, model)
        model.set_output_embeddings = types.MethodType(set_output_embeddings_for_lm, model)

    model.transformer.get_input_embeddings = types.MethodType(get_input_embeddings_for_base, model.transformer)
    model.transformer.set_input_embeddings = types.MethodType(set_input_embeddings_for_base, model.transformer)
    return model
