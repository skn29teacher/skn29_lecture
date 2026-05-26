from __future__ import annotations

import argparse
import importlib.metadata as metadata
import os
import platform
import shutil
import subprocess
import sys

from common import load_dotenv_if_available


PACKAGES = [
    "torch",
    "transformers",
    "accelerate",
    "datasets",
    "peft",
    "trl",
    "bitsandbytes",
    "huggingface_hub",
    "safetensors",
]


def package_version(name: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return "NOT_INSTALLED"


def print_nvidia_smi() -> None:
    if not shutil.which("nvidia-smi"):
        print("nvidia_smi: NOT_FOUND")
        return
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("nvidia_smi:")
        for line in result.stdout.strip().splitlines():
            print(f"  {line}")
    except Exception as exc:
        print(f"nvidia_smi_error: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check RunPod GPU and Python training environment.")
    parser.add_argument("--require-cuda", action="store_true", help="Exit non-zero if CUDA is unavailable.")
    parser.add_argument("--require-token", action="store_true", help="Exit non-zero if no Hugging Face token is available.")
    args = parser.parse_args()

    load_dotenv_if_available()
    hf_token_present = bool(os.getenv("HF_TOKEN"))
    try:
        from huggingface_hub import get_token

        hf_token_present = hf_token_present or bool(get_token())
    except Exception:
        pass

    print(f"python: {sys.version.split()[0]}")
    print(f"platform: {platform.platform()}")
    print(f"hf_home: {os.getenv('HF_HOME', '<not set>')}")
    print(f"hf_token_present: {hf_token_present}")
    print_nvidia_smi()

    print("packages:")
    for package in PACKAGES:
        print(f"  {package}: {package_version(package)}")

    try:
        import torch
    except Exception as exc:
        print(f"torch_import_error: {exc}")
        return 1

    cuda_available = torch.cuda.is_available()
    print(f"cuda_available: {cuda_available}")
    if cuda_available:
        print(f"cuda_device_count: {torch.cuda.device_count()}")
        print(f"cuda_device_0: {torch.cuda.get_device_name(0)}")
        print(f"cuda_version_from_torch: {torch.version.cuda}")
        print(f"bf16_supported: {torch.cuda.is_bf16_supported()}")
        free_bytes, total_bytes = torch.cuda.mem_get_info(0)
        print(f"cuda_mem_free_gb: {free_bytes / 1024**3:.2f}")
        print(f"cuda_mem_total_gb: {total_bytes / 1024**3:.2f}")

    if args.require_cuda and not cuda_available:
        print("ERROR: CUDA is required but unavailable.", file=sys.stderr)
        return 2
    if args.require_token and not hf_token_present:
        print("ERROR: HF_TOKEN is required but missing.", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
