"""
Task 0 — Messy Dummy Dataset 생성
=================================
결측치(NaN), 극단적 이상치, 중복행이 의도적으로 포함된
교육용 더미 데이터셋을 직접 생성합니다.
"""

import numpy as np
import pandas as pd

np.random.seed(42)

n = 100  # 기본 행 수

# ── 1. 기본 데이터 프레임 생성 ──────────────────────────
data = {
    "id": range(1, n + 1),
    "name": [f"user_{i}" for i in range(1, n + 1)],
    "age": np.random.randint(18, 65, size=n).astype(float),
    "salary": np.random.normal(50000, 15000, size=n).round(0),
    "score": np.random.uniform(0, 100, size=n).round(2),
    "department": np.random.choice(
        ["영업", "개발", "마케팅", "인사", "재무"], size=n
    ),
}

df = pd.DataFrame(data)

# ── 2. 결측치(NaN) 주입 ─────────────────────────────────
nan_idx_age = np.random.choice(n, size=8, replace=False)
nan_idx_salary = np.random.choice(n, size=6, replace=False)
nan_idx_score = np.random.choice(n, size=10, replace=False)

df.loc[nan_idx_age, "age"] = np.nan
df.loc[nan_idx_salary, "salary"] = np.nan
df.loc[nan_idx_score, "score"] = np.nan

# ── 3. 극단적 이상치 주입 ───────────────────────────────
outlier_idx = np.random.choice(n, size=5, replace=False)
df.loc[outlier_idx, "salary"] = [300000, -50000, 500000, 400000, -30000]

outlier_idx2 = np.random.choice(n, size=4, replace=False)
df.loc[outlier_idx2, "age"] = [150, 200, -5, 300]

# ── 4. 중복행 주입 ─────────────────────────────────────
dup_rows = df.sample(n=12, random_state=42)
df = pd.concat([df, dup_rows], ignore_index=True)

# ── 5. 결과 확인 ───────────────────────────────────────
print("=" * 60)
print("   Messy Dummy Dataset 생성 완료")
print("=" * 60)
print(f"\n Shape : {df.shape}")
print(f"\n Info  :")
df.info()
print(f"\n 결측치 현황 :\n{df.isnull().sum()}")
print(f"\n 중복행 수   : {df.duplicated().sum()}")
print(f"\n Describe :\n{df.describe()}")
print(f"\n 처음 10행 :\n{df.head(10)}")

# ── 6. CSV 저장 ────────────────────────────────────────
import os
output_dir = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "messy_data.csv")
df.to_csv(output_path, index=False, encoding="utf-8-sig")
print(f"\n 저장 완료 → {output_path}")