#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${VENV_DIR:-$PROJECT_DIR/.venv}"

if [ "$(id -u)" -eq 0 ]; then
  SUDO=""
else
  SUDO="sudo"
fi

echo "[1/5] Installing system packages"
DEBIAN_FRONTEND=noninteractive $SUDO apt-get update
DEBIAN_FRONTEND=noninteractive $SUDO apt-get install -y \
  git git-lfs python3 python3-venv python3-pip \
  build-essential ninja-build tmux htop curl
git lfs install || true

echo "[2/5] Creating virtual environment at $VENV_DIR"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

echo "[3/5] Upgrading pip tooling"
python -m pip install -U pip setuptools wheel packaging

echo "[4/5] Installing PyTorch CUDA 12.8 wheels"
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

echo "[5/5] Installing training dependencies"
pip install -U -r "$PROJECT_DIR/requirements-train.txt"
python -m ipykernel install --user --name exaone35 --display-name "Python (exaone35)" || true

echo
echo "Environment check:"
python "$PROJECT_DIR/scripts/check_env.py"

echo
echo "Done. Activate with:"
echo "  source $VENV_DIR/bin/activate"
echo
echo "In JupyterLab, select kernel:"
echo "  Python (exaone35)"
