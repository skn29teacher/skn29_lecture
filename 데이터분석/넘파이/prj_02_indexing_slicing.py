"""
NumPy 실습 2: 인덱싱과 슬라이싱
================================
이 실습에서는 NumPy 배열의 다양한 접근 방법을 학습합니다.
"""

import numpy as np

print("=" * 60)
print("NumPy 인덱싱과 슬라이싱 실습")
print("=" * 60)

# ============================================================
# 실습 2-1: 기본 인덱싱
# ============================================================
print("\n[실습 2-1] 기본 인덱싱")
print("-" * 40)

# 1차원 배열 생성
arr1d = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
print(f"1차원 배열: {arr1d}")

# TODO: 첫 번째 요소
print(f"첫 번째 요소 (arr1d[0]): {arr1d[0]}")

# TODO: 마지막 요소
print(f"마지막 요소 (arr1d[-1]): {arr1d[-1]}")

# TODO: 세 번째 요소
print(f"세 번째 요소 (arr1d[2]): {arr1d[2]}")

# TODO: 뒤에서 세 번째 요소
print(f"뒤에서 세 번째 (arr1d[-3]): {arr1d[-3]}")

# ============================================================
# 실습 2-2: 다차원 배열 인덱싱
# ============================================================
print("\n[실습 2-2] 다차원 배열 인덱싱")
print("-" * 40)

# 2차원 배열 생성
arr2d = np.array([[1, 2, 3, 4],
                  [5, 6, 7, 8],
                  [9, 10, 11, 12],
                  [13, 14, 15, 16]])
print(f"2차원 배열:\n{arr2d}")

# TODO: (0, 0) 위치 요소
print(f"\narr2d[0, 0]: {arr2d[0, 0]}")

# TODO: (2, 3) 위치 요소
print(f"arr2d[2, 3]: {arr2d[2, 3]}")

# TODO: 마지막 행, 마지막 열 요소
print(f"arr2d[-1, -1]: {arr2d[-1, -1]}")

# TODO: 두 번째 행 전체
print(f"arr2d[1] (두 번째 행): {arr2d[1]}")

# TODO: 세 번째 열 전체
print(f"arr2d[:, 2] (세 번째 열): {arr2d[:, 2]}")

# ============================================================
# 실습 2-3: 기본 슬라이싱
# ============================================================
print("\n[실습 2-3] 기본 슬라이싱")
print("-" * 40)

arr = np.arange(10)  # [0 1 2 3 4 5 6 7 8 9]
print(f"원본 배열: {arr}")

# TODO: 인덱스 2~6
print(f"arr[2:7]: {arr[2:7]}")

# TODO: 처음부터 5번째까지
print(f"arr[:5]: {arr[:5]}")

# TODO: 5번째부터 끝까지
print(f"arr[5:]: {arr[5:]}")

# TODO: 2씩 건너뛰기
print(f"arr[::2]: {arr[::2]}")

# TODO: 역순
print(f"arr[::-1]: {arr[::-1]}")

# TODO: 역순으로 2씩 건너뛰기
print(f"arr[::-2]: {arr[::-2]}")

# ============================================================
# 실습 2-4: 다차원 슬라이싱
# ============================================================
print("\n[실습 2-4] 다차원 슬라이싱")
print("-" * 40)

arr2d = np.arange(1, 17).reshape(4, 4)
print(f"4x4 배열:\n{arr2d}")

# TODO: 상위 2x2 부분 행렬
top_left = arr2d[:2, :2]
print(f"\n상위 2x2 (arr2d[:2, :2]):\n{top_left}")

# TODO: 하위 2x2 부분 행렬
bottom_right = arr2d[2:, 2:]
print(f"\n하위 2x2 (arr2d[2:, 2:]):\n{bottom_right}")

# TODO: 가운데 2x2 부분 행렬
center = arr2d[1:3, 1:3]
print(f"\n가운데 2x2 (arr2d[1:3, 1:3]):\n{center}")

# TODO: 모든 행의 첫 번째와 마지막 열
first_last_cols = arr2d[:, [0, -1]]
print(f"\n첫 번째, 마지막 열 (arr2d[:, [0, -1]]):\n{first_last_cols}")

# TODO: 짝수 행만
even_rows = arr2d[::2]
print(f"\n짝수 행 (arr2d[::2]):\n{even_rows}")

# ============================================================
# 실습 2-5: 팬시 인덱싱 (Fancy Indexing)
# ============================================================
print("\n[실습 2-5] 팬시 인덱싱")
print("-" * 40)

arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
print(f"원본 배열: {arr}")

# TODO: 인덱스 [0, 2, 5, 9]의 요소들
indices = [0, 2, 5, 9]
selected = arr[indices]
print(f"arr[[0, 2, 5, 9]]: {selected}")

# 2D 배열에서 팬시 인덱싱
arr2d = np.arange(1, 17).reshape(4, 4)
print(f"\n4x4 배열:\n{arr2d}")

# TODO: 0, 2번째 행 선택
rows = arr2d[[0, 2]]
print(f"\narr2d[[0, 2]] (0, 2번째 행):\n{rows}")

# TODO: 대각선 요소 선택
diagonal = arr2d[[0, 1, 2, 3], [0, 1, 2, 3]]
print(f"\n대각선 요소: {diagonal}")

# TODO: 역대각선 요소 선택
anti_diagonal = arr2d[[0, 1, 2, 3], [3, 2, 1, 0]]
print(f"역대각선 요소: {anti_diagonal}")

# ============================================================
# 실습 2-6: 불리언 인덱싱
# ============================================================
print("\n[실습 2-6] 불리언 인덱싱")
print("-" * 40)

arr = np.array([15, 8, 23, 4, 42, 16, 7, 35, 19, 50])
print(f"원본 배열: {arr}")

# TODO: 20보다 큰 요소
mask_gt20 = arr > 20
print(f"\n조건 (arr > 20): {mask_gt20}")
print(f"20보다 큰 요소: {arr[mask_gt20]}")

# TODO: 짝수 요소
even_elements = arr[arr % 2 == 0]
print(f"짝수 요소: {even_elements}")

# TODO: 10~30 사이의 요소
range_elements = arr[(arr >= 10) & (arr <= 30)]
print(f"10~30 사이: {range_elements}")

# TODO: 10 미만 또는 40 초과
extreme_elements = arr[(arr < 10) | (arr > 40)]
print(f"10 미만 또는 40 초과: {extreme_elements}")

# 2D 배열에서 불리언 인덱싱
arr2d = np.arange(1, 17).reshape(4, 4)
print(f"\n4x4 배열:\n{arr2d}")

# TODO: 8보다 큰 요소 (1D로 반환됨)
gt8 = arr2d[arr2d > 8]
print(f"8보다 큰 요소: {gt8}")

# ============================================================
# 실습 2-7: 조건에 따른 값 변경
# ============================================================
print("\n[실습 2-7] 조건에 따른 값 변경")
print("-" * 40)

arr = np.array([1, 5, 3, 8, 2, 9, 4, 7, 6, 10])
print(f"원본 배열: {arr}")

# TODO: 5보다 큰 값을 0으로 변경
arr_copy = arr.copy()
arr_copy[arr_copy > 5] = 0
print(f"5보다 큰 값 -> 0: {arr_copy}")

# TODO: np.where를 사용한 조건부 변경
result = np.where(arr > 5, arr * 2, arr)
print(f"5보다 크면 2배, 아니면 유지: {result}")

# TODO: np.clip을 사용한 범위 제한
clipped = np.clip(arr, 3, 7)
print(f"np.clip(arr, 3, 7): {clipped}")

# ============================================================
# 실습 2-8: 뷰(View)와 복사(Copy)
# ============================================================
print("\n[실습 2-8] 뷰(View)와 복사(Copy)")
print("-" * 40)

# 뷰 예시
arr = np.array([1, 2, 3, 4, 5])
view = arr[1:4]  # 슬라이싱은 뷰
print(f"원본 배열: {arr}")
print(f"슬라이스 (뷰): {view}")

view[0] = 100  # 뷰 수정
print(f"뷰 수정 후 원본: {arr}")  # 원본도 변경됨

# 복사 예시
arr = np.array([1, 2, 3, 4, 5])
copy = arr[1:4].copy()  # 명시적 복사
print(f"\n원본 배열: {arr}")
print(f"복사본: {copy}")

copy[0] = 100  # 복사본 수정
print(f"복사본 수정 후 원본: {arr}")  # 원본 유지

# 뷰인지 확인하는 방법
arr = np.array([1, 2, 3, 4, 5])
view = arr[1:4]
copy = arr[1:4].copy()

print(f"\nview.base is arr: {view.base is arr}")  # True (뷰)
print(f"copy.base is arr: {copy.base is arr}")    # False (복사)

# ============================================================
# 도전 과제
# ============================================================
print("\n" + "=" * 60)
print("🎯 도전 과제")
print("=" * 60)

print("""
[과제 1] 5x5 배열에서 테두리 요소만 추출하기
힌트: 슬라이싱과 팬시 인덱싱 조합

[과제 2] 학생 성적 배열에서 60점 이상인 학생만 필터링하고,
         80점 이상은 'A', 70점 이상은 'B', 나머지는 'C' 등급 부여
힌트: np.where 중첩 사용

[과제 3] 6x6 배열에서 3x3 블록 4개로 분할하기
힌트: 슬라이싱 활용
""")

# 과제 1 해답
print("\n[과제 1 해답]")
arr = np.arange(1, 26).reshape(5, 5)
print(f"5x5 배열:\n{arr}")

# 테두리 추출 방법 1: 인덱싱 조합
top = arr[0, :]
bottom = arr[-1, :]
left = arr[1:-1, 0]
right = arr[1:-1, -1]
border = np.concatenate([top, right, bottom[::-1], left[::-1]])
print(f"테두리 요소 (시계방향): {border}")

# 과제 2 해답
print("\n[과제 2 해답]")
scores = np.array([85, 72, 45, 90, 65, 78, 55, 88, 95, 62])
print(f"성적: {scores}")

# 60점 이상 필터링
passing = scores[scores >= 60]
print(f"60점 이상: {passing}")

# 등급 부여
grades = np.where(scores >= 80, 'A', 
                  np.where(scores >= 70, 'B',
                           np.where(scores >= 60, 'C', 'F')))
print(f"등급: {grades}")

# 과제 3 해답
print("\n[과제 3 해답]")
arr = np.arange(1, 37).reshape(6, 6)
print(f"6x6 배열:\n{arr}")

block1 = arr[:3, :3]
block2 = arr[:3, 3:]
block3 = arr[3:, :3]
block4 = arr[3:, 3:]

print(f"\n블록 1 (좌상단):\n{block1}")
print(f"\n블록 2 (우상단):\n{block2}")
print(f"\n블록 3 (좌하단):\n{block3}")
print(f"\n블록 4 (우하단):\n{block4}")

print("\n" + "=" * 60)
print("실습 2 완료!")
print("=" * 60)
