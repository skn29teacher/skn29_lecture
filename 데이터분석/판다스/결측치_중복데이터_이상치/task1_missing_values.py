"""
Task 1 — 결측치(NaN) 탐지 및 대치
===================================
Messy Dummy Dataset의 결측치를 탐지하고
다양한 방법(삭제, 대치, 보간)으로 처리합니다.
"""

import os
import pandas as pd
import numpy as np

# ── 데이터 로드 ────────────────────────────────────────
data_path = os.path.join(os.path.dirname(__file__), "..", "data", "messy_data.csv")
df = pd.read_csv(data_path)

print("=" * 65)
print("  🔍  Task 1 — 결측치(NaN) 탐지 및 대치")
print("=" * 65)

# ================================================================
# STEP 1: 결측치 탐지
# ================================================================
print("\n" + "─" * 65)
print("  STEP 1 │ 결측치 탐지")
print("─" * 65)

print(f"\n▶ 원본 데이터 Shape : {df.shape}")
print(f"\n▶ 전체 결측치 개수  : {df.isnull().sum().sum()}")
print(f"\n▶ 컬럼별 결측치 현황 :")
print(df.isnull().sum())
print(f"\n▶ 컬럼별 결측치 비율(%) :")
print((df.isnull().mean() * 100).round(2))

# 결측치가 있는 행만 필터링
print(f"\n▶ 결측치가 포함된 행 수 : {df.isnull().any(axis=1).sum()}")
print(f"\n▶ 결측치 히트맵 (처음 20행) :")
print(df.head(20).isnull().astype(int))

# ================================================================
# STEP 2: 결측치 삭제 (dropna)
# ================================================================
print("\n" + "─" * 65)
print("  STEP 2 │ 결측치 삭제 — dropna()")
print("─" * 65)

# 2-1. 결측치가 하나라도 있는 행 삭제
df_drop_any = df.dropna(how="any")
print(f"\n▶ dropna(how='any')  → Shape : {df.shape} → {df_drop_any.shape}")
print(f"  삭제된 행 수 : {len(df) - len(df_drop_any)}")

# 2-2. 모든 값이 NaN인 행만 삭제
df_drop_all = df.dropna(how="all")
print(f"\n▶ dropna(how='all')  → Shape : {df.shape} → {df_drop_all.shape}")
print(f"  삭제된 행 수 : {len(df) - len(df_drop_all)}")

# 2-3. 특정 컬럼 기준 삭제
df_drop_subset = df.dropna(subset=["age", "salary"])
print(f"\n▶ dropna(subset=['age','salary']) → Shape : {df.shape} → {df_drop_subset.shape}")
print(f"  삭제된 행 수 : {len(df) - len(df_drop_subset)}")

# 2-4. thresh 사용 — 최소 N개 유효값이 있어야 보존
df_drop_thresh = df.dropna(thresh=5)
print(f"\n▶ dropna(thresh=5)   → Shape : {df.shape} → {df_drop_thresh.shape}")
print(f"  삭제된 행 수 : {len(df) - len(df_drop_thresh)}")

# ================================================================
# STEP 3: 결측치 대치 (fillna)
# ================================================================
print("\n" + "─" * 65)
print("  STEP 3 │ 결측치 대치 — fillna()")
print("─" * 65)

df_fill = df.copy()

# 3-1. 고정값으로 대치
df_fill_zero = df.copy()
df_fill_zero["score"] = df_fill_zero["score"].fillna(0)
print(f"\n▶ score 컬럼 NaN → 0 대치")
print(f"  NaN 수 : {df['score'].isnull().sum()} → {df_fill_zero['score'].isnull().sum()}")

# 3-2. 평균(mean)으로 대치
df_fill_mean = df.copy()
age_mean = df_fill_mean["age"].mean()
df_fill_mean["age"] = df_fill_mean["age"].fillna(age_mean)
print(f"\n▶ age 컬럼 NaN → 평균({age_mean:.1f}) 대치")
print(f"  NaN 수 : {df['age'].isnull().sum()} → {df_fill_mean['age'].isnull().sum()}")

# 3-3. 중앙값(median)으로 대치
df_fill_median = df.copy()
salary_median = df_fill_median["salary"].median()
df_fill_median["salary"] = df_fill_median["salary"].fillna(salary_median)
print(f"\n▶ salary 컬럼 NaN → 중앙값({salary_median:,.0f}) 대치")
print(f"  NaN 수 : {df['salary'].isnull().sum()} → {df_fill_median['salary'].isnull().sum()}")

# 3-4. 최빈값(mode)으로 대치 — 범주형에 적합
df_fill_mode = df.copy()
dept_mode = df_fill_mode["department"].mode()[0]
# department에는 NaN이 없지만 시연용
print(f"\n▶ department 컬럼 최빈값 : '{dept_mode}' (참고: 현재 NaN 없음)")

# 3-5. 앞/뒤 값으로 채우기 (forward fill / backward fill)
df_ffill = df.copy()
df_ffill["score"] = df_ffill["score"].ffill()
print(f"\n▶ score 컬럼 ffill(앞의 값으로 채움)")
print(f"  NaN 수 : {df['score'].isnull().sum()} → {df_ffill['score'].isnull().sum()}")

df_bfill = df.copy()
df_bfill["score"] = df_bfill["score"].bfill()
print(f"\n▶ score 컬럼 bfill(뒤의 값으로 채움)")
print(f"  NaN 수 : {df['score'].isnull().sum()} → {df_bfill['score'].isnull().sum()}")

# ================================================================
# STEP 4: 보간법 (interpolate)
# ================================================================
print("\n" + "─" * 65)
print("  STEP 4 │ 보간법 — interpolate()")
print("─" * 65)

# 4-1. 선형 보간
df_interp = df.copy()
df_interp["score"] = df_interp["score"].interpolate(method="linear")
print(f"\n▶ score 컬럼 선형 보간(linear)")
print(f"  NaN 수 : {df['score'].isnull().sum()} → {df_interp['score'].isnull().sum()}")

# 4-2. 다항식 보간
df_interp2 = df.copy()
df_interp2["salary"] = df_interp2["salary"].interpolate(method="polynomial", order=2)
print(f"\n▶ salary 컬럼 다항식 보간(polynomial, order=2)")
print(f"  NaN 수 : {df['salary'].isnull().sum()} → {df_interp2['salary'].isnull().sum()}")

# ================================================================
# STEP 5: 종합 적용 및 전·후 비교
# ================================================================
print("\n" + "─" * 65)
print("  STEP 5 │ 종합 적용 — 전·후 비교")
print("─" * 65)

df_cleaned = df.copy()
df_cleaned["age"] = df_cleaned["age"].fillna(df_cleaned["age"].median())
df_cleaned["salary"] = df_cleaned["salary"].fillna(df_cleaned["salary"].median())
df_cleaned["score"] = df_cleaned["score"].interpolate(method="linear").bfill()

print(f"\n▶ 전처리 전 Shape : {df.shape}")
print(f"  전처리 전 NaN   : {df.isnull().sum().sum()}")
print(f"\n▶ 전처리 후 Shape : {df_cleaned.shape}")
print(f"  전처리 후 NaN   : {df_cleaned.isnull().sum().sum()}")
print(f"\n▶ 전처리 전 Info :")
df.info()
print(f"\n▶ 전처리 후 Info :")
df_cleaned.info()

# 정제된 데이터 저장
output_dir = os.path.join(os.path.dirname(__file__), "..", "data")
output_path = os.path.join(output_dir, "task1_cleaned.csv")
df_cleaned.to_csv(output_path, index=False, encoding="utf-8-sig")
print(f"\n✅ 결측치 대치 완료 데이터 저장 → {output_path}")
