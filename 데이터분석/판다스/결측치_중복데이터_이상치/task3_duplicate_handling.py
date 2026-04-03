"""
Task 3 — 중복 데이터 탐지 및 정제
====================================
데이터 내의 완전히 동일한 행(중복 데이터)을 탐지하고,
다양한 옵션에 따라 중복을 정제하는 실습을 진행합니다.
"""

import os
import pandas as pd

# ── 데이터 로드 ────────────────────────────────────────
data_path = os.path.join(os.path.dirname(__file__), "..", "data", "messy_data.csv")
df = pd.read_csv(data_path)

print("=" * 65)
print("  Task 3 -- 중복 데이터 탐지 및 정제")
print("=" * 65)

# ================================================================
# STEP 1: 중복 데이터 탐지 (duplicated)
# ================================================================
print("\n" + "-" * 65)
print("  STEP 1 | 중복 데이터 탐지 (duplicated)")
print("-" * 65)

print(f"\n▶ 원본 데이터 Shape: {df.shape}")

# 전체 컬럼을 기준으로 중복 탐지 (keep='first'가 기본값, 첫 번째 발견은 False, 이후 중복은 True)
duplicates_all = df.duplicated()
num_duplicates = duplicates_all.sum()
print(f"\n▶ 완전히 중복된 행의 수: {num_duplicates}")

if num_duplicates > 0:
    print(f"\n▶ 중복된 행 데이터 (일부):")
    # 중복의 원본과 중복본을 모두 보기 위해 keep=False 사용
    print(df[df.duplicated(keep=False)].sort_values(by="id").head(6))

# ================================================================
# STEP 2: 특정 컬럼 기준 중복 탐지
# ================================================================
print("\n" + "-" * 65)
print("  STEP 2 | 특정 컬럼 기준 중복 탐지")
print("-" * 65)

# id는 고유해야 한다고 가정할 때, id 컬럼 기준 중복
dup_by_id = df.duplicated(subset=['id']).sum()
print(f"\n▶ 'id' 컬럼 기준 중복 행 수: {dup_by_id}")

# name과 department의 조합으로 중복 탐지
dup_by_name_dept = df.duplicated(subset=['name', 'department']).sum()
print(f"▶ 'name', 'department' 컬럼 기준 중복 행 수: {dup_by_name_dept}")

# ================================================================
# STEP 3: 중복 데이터 정제 (drop_duplicates)
# ================================================================
print("\n" + "-" * 65)
print("  STEP 3 | 중복 데이터 정제 (drop_duplicates)")
print("-" * 65)

# 3-1. keep='first' (기본값) : 첫 번째 항목 유지, 나머지 삭제
df_keep_first = df.drop_duplicates(keep='first')
print(f"\n▶ keep='first' 적용 시 Shape: {df.shape} -> {df_keep_first.shape}")
print(f"   삭제된 행 수: {len(df) - len(df_keep_first)}")

# 3-2. keep='last' : 마지막 항목 유지, 이전 중복 삭제
df_keep_last = df.drop_duplicates(keep='last')
print(f"\n▶ keep='last' 적용 시 Shape: {df.shape} -> {df_keep_last.shape}")
print(f"   삭제된 행 수: {len(df) - len(df_keep_last)}")

# 3-3. keep=False : 중복이 존재하는 모든 행을 일괄 삭제 (고유한 값만 남김)
df_keep_none = df.drop_duplicates(keep=False)
print(f"\n▶ keep=False 적용 시 Shape: {df.shape} -> {df_keep_none.shape}")
print(f"   삭제된 행 수: {len(df) - len(df_keep_none)}")

# 3-4. 특정 컬럼('id')을 기준으로 최신(또는 특정) 정보를 남길 때
# 예: 마지막으로 입력된 데이터가 최신이라고 가정하고 'id' 기준 중복 제거
df_unique_id = df.drop_duplicates(subset=['id'], keep='last')
print(f"\n▶ subset=['id'], keep='last' 적용 시 Shape: {df.shape} -> {df_unique_id.shape}")
print(f"   삭제된 행 수: {len(df) - len(df_unique_id)}")

# ================================================================
# STEP 4: 정제된 데이터 확인 및 저장
# ================================================================
print("\n" + "-" * 65)
print("  STEP 4 | 최종 결과 확인")
print("-" * 65)

df_final = df_keep_first.copy()
print(f"\n▶ 정제 완료 후 Shape: {df_final.shape}")
print(f"▶ 남은 중복 행 수: {df_final.duplicated().sum()}")

output_dir = os.path.join(os.path.dirname(__file__), "..", "data")
output_path = os.path.join(output_dir, "task3_deduped.csv")
df_final.to_csv(output_path, index=False, encoding="utf-8-sig")
print(f"\n✅ 중복 제제 완료 데이터 저장 → {output_path}")
