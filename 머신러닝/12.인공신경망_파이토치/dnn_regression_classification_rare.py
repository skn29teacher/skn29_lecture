"""
교육용 DNN 실습:
1) 회귀 (Diabetes)
2) 다중분류 (Wine)
3) 희귀 이진분류 (OpenML Credit Card Fraud)

실행 예시:
    python scripts/dnn_regression_classification_rare.py --task all
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import torch
from sklearn.datasets import fetch_openml, load_diabetes, load_wine
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    mean_squared_error,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch import nn
from torch.utils.data import DataLoader, TensorDataset, WeightedRandomSampler


def set_seed(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


class MLP(nn.Module):
    def __init__(self, input_dim: int, hidden_dims: List[int], output_dim: int, dropout: float = 0.1) -> None:
        super().__init__()
        layers: List[nn.Module] = []
        prev = input_dim
        for h in hidden_dims:
            layers.extend([nn.Linear(prev, h), nn.ReLU(), nn.Dropout(dropout)])
            prev = h
        layers.append(nn.Linear(prev, output_dim))
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class BinaryFocalLossWithLogits(nn.Module):
    def __init__(self, alpha: float = 0.25, gamma: float = 2.0, reduction: str = "mean") -> None:
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        bce = nn.functional.binary_cross_entropy_with_logits(logits, targets, reduction="none")
        probs = torch.sigmoid(logits)
        pt = probs * targets + (1.0 - probs) * (1.0 - targets)
        alpha_t = self.alpha * targets + (1.0 - self.alpha) * (1.0 - targets)
        loss = alpha_t * ((1.0 - pt) ** self.gamma) * bce
        if self.reduction == "mean":
            return loss.mean()
        if self.reduction == "sum":
            return loss.sum()
        return loss


@dataclass
class TrainConfig:
    epochs: int = 50
    batch_size: int = 128
    lr: float = 1e-3
    weight_decay: float = 1e-4


def run_regression_epoch(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer | None,
    device: torch.device,
) -> float:
    is_train = optimizer is not None
    model.train(is_train)
    losses: List[float] = []

    context = torch.enable_grad() if is_train else torch.no_grad()
    with context:
        for xb, yb in loader:
            xb = xb.to(device)
            yb = yb.to(device)
            pred = model(xb)
            loss = criterion(pred, yb)
            losses.append(float(loss.item()))

            if is_train:
                optimizer.zero_grad(set_to_none=True)
                loss.backward()
                optimizer.step()
    return float(np.mean(losses))


def run_classification_epoch(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer | None,
    device: torch.device,
) -> float:
    is_train = optimizer is not None
    model.train(is_train)
    losses: List[float] = []

    context = torch.enable_grad() if is_train else torch.no_grad()
    with context:
        for xb, yb in loader:
            xb = xb.to(device)
            yb = yb.to(device)
            logits = model(xb)
            loss = criterion(logits, yb)
            losses.append(float(loss.item()))

            if is_train:
                optimizer.zero_grad(set_to_none=True)
                loss.backward()
                optimizer.step()
    return float(np.mean(losses))


def make_regression_loaders(batch_size: int) -> Tuple[DataLoader, DataLoader, DataLoader, int]:
    X, y = load_diabetes(return_X_y=True)
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.30, random_state=42)
    X_valid, X_test, y_valid, y_test = train_test_split(X_temp, y_temp, test_size=0.50, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_valid = scaler.transform(X_valid)
    X_test = scaler.transform(X_test)

    x_train_t = torch.tensor(X_train, dtype=torch.float32)
    x_valid_t = torch.tensor(X_valid, dtype=torch.float32)
    x_test_t = torch.tensor(X_test, dtype=torch.float32)
    y_train_t = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
    y_valid_t = torch.tensor(y_valid, dtype=torch.float32).unsqueeze(1)
    y_test_t = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)

    # DataLoader를 쓰면 미니배치/셔플이 자동 처리되어 학습 안정성과 속도를 함께 확보할 수 있다.
    train_loader = DataLoader(TensorDataset(x_train_t, y_train_t), batch_size=batch_size, shuffle=True)
    valid_loader = DataLoader(TensorDataset(x_valid_t, y_valid_t), batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(TensorDataset(x_test_t, y_test_t), batch_size=batch_size, shuffle=False)
    return train_loader, valid_loader, test_loader, X_train.shape[1]


def make_wine_loaders(batch_size: int) -> Tuple[DataLoader, DataLoader, DataLoader, int]:
    X, y = load_wine(return_X_y=True)
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)
    X_valid, X_test, y_valid, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_valid = scaler.transform(X_valid)
    X_test = scaler.transform(X_test)

    x_train_t = torch.tensor(X_train, dtype=torch.float32)
    x_valid_t = torch.tensor(X_valid, dtype=torch.float32)
    x_test_t = torch.tensor(X_test, dtype=torch.float32)
    y_train_t = torch.tensor(y_train, dtype=torch.long)
    y_valid_t = torch.tensor(y_valid, dtype=torch.long)
    y_test_t = torch.tensor(y_test, dtype=torch.long)

    train_loader = DataLoader(TensorDataset(x_train_t, y_train_t), batch_size=batch_size, shuffle=True)
    valid_loader = DataLoader(TensorDataset(x_valid_t, y_valid_t), batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(TensorDataset(x_test_t, y_test_t), batch_size=batch_size, shuffle=False)
    return train_loader, valid_loader, test_loader, X_train.shape[1]


def make_rare_creditcard_loaders(
    batch_size: int,
    max_samples: int | None,
) -> Tuple[DataLoader, DataLoader, DataLoader, int, np.ndarray]:
    bundle = fetch_openml(data_id=1597, as_frame=True)
    X = bundle.data.to_numpy(dtype=np.float32)
    y = bundle.target.astype(int).to_numpy()

    if max_samples is not None and max_samples < len(X):
        X, _, y, _ = train_test_split(X, y, train_size=max_samples, stratify=y, random_state=42)

    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)
    X_valid, X_test, y_valid, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_valid = scaler.transform(X_valid)
    X_test = scaler.transform(X_test)

    x_train_t = torch.tensor(X_train, dtype=torch.float32)
    x_valid_t = torch.tensor(X_valid, dtype=torch.float32)
    x_test_t = torch.tensor(X_test, dtype=torch.float32)
    y_train_t = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
    y_valid_t = torch.tensor(y_valid, dtype=torch.float32).unsqueeze(1)
    y_test_t = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)

    class_count = np.bincount(y_train)
    sample_weights = (1.0 / np.maximum(class_count, 1))[y_train]
    sampler = WeightedRandomSampler(
        weights=torch.tensor(sample_weights, dtype=torch.float64),
        num_samples=len(sample_weights),
        replacement=True,
    )

    train_loader = DataLoader(
        TensorDataset(x_train_t, y_train_t),
        batch_size=batch_size,
        sampler=sampler,
    )
    valid_loader = DataLoader(TensorDataset(x_valid_t, y_valid_t), batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(TensorDataset(x_test_t, y_test_t), batch_size=batch_size, shuffle=False)
    return train_loader, valid_loader, test_loader, X_train.shape[1], y_train


def evaluate_regression(model: nn.Module, loader: DataLoader, device: torch.device) -> Dict[str, float]:
    model.eval()
    y_true, y_pred = [], []
    with torch.no_grad():
        for xb, yb in loader:
            xb = xb.to(device)
            pred = model(xb).cpu().numpy().squeeze()
            y_pred.append(np.atleast_1d(pred))
            y_true.append(yb.numpy().squeeze())
    y_true_np = np.concatenate(y_true)
    y_pred_np = np.concatenate(y_pred)
    rmse = float(np.sqrt(mean_squared_error(y_true_np, y_pred_np)))
    return {"rmse": rmse}


def evaluate_multiclass(model: nn.Module, loader: DataLoader, device: torch.device) -> Dict[str, float]:
    model.eval()
    y_true, y_pred = [], []
    with torch.no_grad():
        for xb, yb in loader:
            xb = xb.to(device)
            logits = model(xb)
            pred = logits.argmax(dim=1).cpu().numpy()
            y_pred.append(pred)
            y_true.append(yb.numpy())
    y_true_np = np.concatenate(y_true).astype(int)
    y_pred_np = np.concatenate(y_pred).astype(int)
    return {
        "accuracy": float(accuracy_score(y_true_np, y_pred_np)),
        "macro_f1": float(f1_score(y_true_np, y_pred_np, average="macro")),
    }


def evaluate_binary_rare(model: nn.Module, loader: DataLoader, device: torch.device) -> Dict[str, float]:
    model.eval()
    y_true, y_prob = [], []
    with torch.no_grad():
        for xb, yb in loader:
            xb = xb.to(device)
            prob = torch.sigmoid(model(xb)).cpu().numpy().squeeze()
            y_prob.append(np.atleast_1d(prob))
            y_true.append(yb.numpy().squeeze())
    y_true_np = np.concatenate(y_true).astype(int)
    y_prob_np = np.concatenate(y_prob)
    y_pred_np = (y_prob_np >= 0.5).astype(int)
    return {
        "roc_auc": float(roc_auc_score(y_true_np, y_prob_np)),
        "pr_auc": float(average_precision_score(y_true_np, y_prob_np)),
        "recall": float(recall_score(y_true_np, y_pred_np, zero_division=0)),
        "f1": float(f1_score(y_true_np, y_pred_np, zero_division=0)),
    }


def print_metrics(title: str, metrics: Dict[str, float]) -> None:
    print(f"\n[{title}]")
    for k, v in metrics.items():
        print(f"  {k:>10}: {v:.4f}")


def run_regression(config: TrainConfig, device: torch.device) -> None:
    print("\n" + "=" * 70)
    print("1) 회귀: Diabetes")
    print("=" * 70)

    train_loader, valid_loader, test_loader, input_dim = make_regression_loaders(config.batch_size)
    model = MLP(input_dim=input_dim, hidden_dims=[64, 32], output_dim=1, dropout=0.1).to(device)
    criterion = nn.MSELoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.lr, weight_decay=config.weight_decay)

    for epoch in range(1, config.epochs + 1):
        train_loss = run_regression_epoch(model, train_loader, criterion, optimizer, device)
        valid_loss = run_regression_epoch(model, valid_loader, criterion, None, device)
        if epoch == 1 or epoch % 10 == 0:
            print(f"Epoch {epoch:03d} | train={train_loss:.4f} | valid={valid_loss:.4f}")

    print_metrics("Regression test", evaluate_regression(model, test_loader, device))


def run_multiclass(config: TrainConfig, device: torch.device) -> None:
    print("\n" + "=" * 70)
    print("2) 다중분류: Wine")
    print("=" * 70)

    train_loader, valid_loader, test_loader, input_dim = make_wine_loaders(config.batch_size)
    model = MLP(input_dim=input_dim, hidden_dims=[64, 32], output_dim=3, dropout=0.1).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.lr, weight_decay=config.weight_decay)

    for epoch in range(1, config.epochs + 1):
        train_loss = run_classification_epoch(model, train_loader, criterion, optimizer, device)
        valid_loss = run_classification_epoch(model, valid_loader, criterion, None, device)
        if epoch == 1 or epoch % 10 == 0:
            print(f"Epoch {epoch:03d} | train={train_loss:.4f} | valid={valid_loss:.4f}")

    print_metrics("Wine test", evaluate_multiclass(model, test_loader, device))


def run_rare_binary(config: TrainConfig, device: torch.device, max_samples: int | None, use_focal: bool) -> None:
    print("\n" + "=" * 70)
    print("3) 희귀 이진분류: OpenML Credit Card Fraud")
    print("=" * 70)

    train_loader, valid_loader, test_loader, input_dim, y_train = make_rare_creditcard_loaders(
        batch_size=config.batch_size,
        max_samples=max_samples,
    )

    pos = float((y_train == 1).sum())
    neg = float((y_train == 0).sum())
    print(f"Train class distribution -> negative: {int(neg)}, positive: {int(pos)}")

    model = MLP(input_dim=input_dim, hidden_dims=[128, 64], output_dim=1, dropout=0.15).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.lr, weight_decay=config.weight_decay)

    if use_focal:
        criterion: nn.Module = BinaryFocalLossWithLogits(alpha=0.75, gamma=2.0)
        print("Loss: BinaryFocalLossWithLogits(alpha=0.75, gamma=2.0)")
    else:
        pos_weight = torch.tensor([neg / max(pos, 1.0)], dtype=torch.float32, device=device)
        criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
        print(f"Loss: BCEWithLogitsLoss(pos_weight={float(pos_weight.item()):.3f})")

    for epoch in range(1, config.epochs + 1):
        train_loss = run_classification_epoch(model, train_loader, criterion, optimizer, device)
        valid_loss = run_classification_epoch(model, valid_loader, criterion, None, device)
        if epoch == 1 or epoch % 10 == 0:
            print(f"Epoch {epoch:03d} | train={train_loss:.4f} | valid={valid_loss:.4f}")

    print_metrics("Rare-class test", evaluate_binary_rare(model, test_loader, device))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="DNN 회귀/분류/희귀분류 학습 루프 실습")
    parser.add_argument(
        "--task",
        type=str,
        default="all",
        choices=["all", "regression", "classification", "rare"],
        help="실행할 실습 선택",
    )
    parser.add_argument("--epochs", type=int, default=40, help="학습 epoch 수")
    parser.add_argument("--batch-size", type=int, default=128, help="배치 크기")
    parser.add_argument("--lr", type=float, default=1e-3, help="학습률")
    parser.add_argument(
        "--rare-max-samples",
        type=int,
        default=120000,
        help="희귀분류 학습용 최대 샘플 수 (None이면 전체)",
    )
    parser.add_argument(
        "--rare-use-focal-loss",
        action="store_true",
        help="희귀분류에 Focal Loss 사용 (기본은 BCEWithLogitsLoss + pos_weight)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    set_seed(42)
    device = get_device()
    print(f"Device: {device}")

    config = TrainConfig(
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
    )

    if args.task in {"all", "regression"}:
        run_regression(config, device)
    if args.task in {"all", "classification"}:
        run_multiclass(config, device)
    if args.task in {"all", "rare"}:
        max_samples = args.rare_max_samples
        run_rare_binary(
            config=config,
            device=device,
            max_samples=max_samples,
            use_focal=args.rare_use_focal_loss,
        )

    print("\n완료: 요청한 DNN 학습 루프 실습 실행이 끝났습니다.")


if __name__ == "__main__":
    main()

