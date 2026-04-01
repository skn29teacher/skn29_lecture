"""
NumPy 실습 3: 브로드캐스팅
===========================
이 실습에서는 NumPy의 브로드캐스팅 규칙과 활용법을 학습합니다.
"""

import numpy as np

print("=" * 60)
print("NumPy 브로드캐스팅 실습")
print("=" * 60)

# ============================================================
# 실습 3-1: 스칼라와 배열 연산
# ============================================================
print("\n[실습 3-1] 스칼라와 배열 연산")
print("-" * 40)

arr = np.array([1, 2, 3, 4, 5])
print(f"원본 배열: {arr}")

# TODO: 스칼라 덧셈
print(f"arr + 10: {arr + 10}")

# TODO: 스칼라 곱셈
print(f"arr * 3: {arr * 3}")

# TODO: 스칼라 나눗셈
print(f"arr / 2: {arr / 2}")

# TODO: 스칼라 거듭제곱
print(f"arr ** 2: {arr ** 2}")

# 2D 배열과 스칼라
arr2d = np.array([[1, 2, 3],
                  [4, 5, 6]])
print(f"\n2D 배열:\n{arr2d}")
print(f"arr2d * 2:\n{arr2d * 2}")

# ============================================================
# 실습 3-2: 1D 배열과 2D 배열 연산
# ============================================================
print("\n[실습 3-2] 1D 배열과 2D 배열 연산")
print("-" * 40)

arr2d = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
arr1d = np.array([10, 20, 30])

print(f"2D 배열 (3x3):\n{arr2d}")
print(f"1D 배열: {arr1d}")

# TODO: 2D + 1D (행에 더하기)
result_add = arr2d + arr1d
print(f"\narr2d + arr1d (각 행에 더함):\n{result_add}")

# TODO: 2D * 1D (행에 곱하기)
result_mul = arr2d * arr1d
print(f"\narr2d * arr1d (각 행에 곱함):\n{result_mul}")

# 브로드캐스팅 과정 설명
print("\n[브로드캐스팅 과정]")
print(f"arr2d shape: {arr2d.shape}  (3, 3)")
print(f"arr1d shape: {arr1d.shape}  (3,)")
print("→ arr1d는 (1, 3)으로 확장")
print("→ (1, 3)이 (3, 3)으로 브로드캐스트")

# ============================================================
# 실습 3-3: 열 방향 브로드캐스팅
# ============================================================
print("\n[실습 3-3] 열 방향 브로드캐스팅")
print("-" * 40)

arr2d = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
col_vector = np.array([[10], [20], [30]])  # (3, 1) shape

print(f"2D 배열 (3x3):\n{arr2d}")
print(f"열 벡터 (3x1):\n{col_vector}")

# TODO: 2D + 열 벡터 (열에 더하기)
result = arr2d + col_vector
print(f"\narr2d + col_vector (각 열에 더함):\n{result}")

# reshape을 이용한 열 벡터 생성
arr1d = np.array([10, 20, 30])
col_reshaped = arr1d.reshape(-1, 1)  # (3, 1)로 변환
print(f"\nreshape(-1, 1)로 열 벡터 생성: shape = {col_reshaped.shape}")

# ============================================================
# 실습 3-4: 외적 연산 (Outer Product)
# ============================================================
print("\n[실습 3-4] 외적 연산")
print("-" * 40)

row = np.array([1, 2, 3])      # (3,)
col = np.array([[10], [20], [30]])  # (3, 1)

print(f"행 벡터: {row}")
print(f"열 벡터:\n{col}")

# TODO: 외적 (곱셈표)
outer_product = col * row  # (3,1) * (3,) = (3,3)
print(f"\n외적 (col * row):\n{outer_product}")

# np.outer 함수 사용
outer_np = np.outer([10, 20, 30], [1, 2, 3])
print(f"\nnp.outer 결과:\n{outer_np}")

# ============================================================
# 실습 3-5: 브로드캐스팅 규칙 확인
# ============================================================
print("\n[실습 3-5] 브로드캐스팅 규칙 확인")
print("-" * 40)

# 호환 가능한 shape 조합
print("호환 가능한 조합:")
combinations = [
    ((3, 4), (4,)),
    ((3, 4), (1, 4)),
    ((3, 4), (3, 1)),
    ((5, 3, 4), (3, 4)),
    ((5, 3, 4), (1, 4)),
    ((5, 1, 4), (3, 1)),
]

for shape1, shape2 in combinations:
    result_shape = np.broadcast_shapes(shape1, shape2)
    print(f"  {shape1} + {shape2} → {result_shape}")

# 호환 불가능한 조합
print("\n호환 불가능한 조합:")
incompatible = [
    ((3, 4), (5,)),
    ((3, 4), (2, 3)),
    ((5, 3, 4), (2, 4)),
]

for shape1, shape2 in incompatible:
    try:
        np.broadcast_shapes(shape1, shape2)
    except ValueError as e:
        print(f"  {shape1} + {shape2} → Error!")

# ============================================================
# 실습 3-6: 실용적인 브로드캐스팅 예제
# ============================================================
print("\n[실습 3-6] 실용적인 브로드캐스팅 예제")
print("-" * 40)

# 예제 1: 데이터 정규화 (Z-score)
print("\n[예제 1] 데이터 정규화")
data = np.array([[65, 70, 75],
                 [80, 85, 90],
                 [70, 75, 80]])
print(f"원본 데이터:\n{data}")

mean = data.mean(axis=0)  # 열별 평균
std = data.std(axis=0)    # 열별 표준편차
print(f"열별 평균: {mean}")
print(f"열별 표준편차: {std}")

normalized = (data - mean) / std  # 브로드캐스팅
print(f"정규화 결과:\n{normalized}")

# 예제 2: 거리 계산 (유클리드 거리)
print("\n[예제 2] 거리 계산")
points = np.array([[0, 0],
                   [1, 0],
                   [0, 1],
                   [1, 1]])
center = np.array([0.5, 0.5])
print(f"점들:\n{points}")
print(f"중심점: {center}")

distances = np.sqrt(np.sum((points - center) ** 2, axis=1))
print(f"중심점으로부터 거리: {distances}")

# 예제 3: 이미지 밝기 조절
print("\n[예제 3] 이미지 밝기 조절 (시뮬레이션)")
image = np.random.randint(0, 256, (3, 3), dtype=np.uint8)
print(f"원본 이미지:\n{image}")

# 밝기 증가 (브로드캐스팅)
brightness_increase = 50
brighter = np.clip(image + brightness_increase, 0, 255)
print(f"밝기 +50:\n{brighter}")

# 예제 4: 채널별 가중치 적용 (RGB)
print("\n[예제 4] RGB 채널 가중치")
rgb_image = np.random.randint(0, 256, (2, 2, 3))  # 2x2 RGB
print(f"RGB 이미지 shape: {rgb_image.shape}")
print(f"RGB 이미지:\n{rgb_image}")

# 그레이스케일 변환 가중치
weights = np.array([0.299, 0.587, 0.114])  # RGB to Gray
grayscale = np.sum(rgb_image * weights, axis=2)
print(f"\n그레이스케일 변환 (가중 평균):\n{grayscale}")

# ============================================================
# 실습 3-7: 브로드캐스팅 성능
# ============================================================
print("\n[실습 3-7] 브로드캐스팅 vs 반복문")
print("-" * 40)

import time

# 큰 배열 생성
size = 1000000
arr = np.random.rand(size)
scalar = 2.5

# 방법 1: 브로드캐스팅
start = time.time()
result1 = arr * scalar
time_broadcast = time.time() - start

# 방법 2: 반복문 (비교용)
start = time.time()
result2 = np.empty(size)
for i in range(size):
    result2[i] = arr[i] * scalar
time_loop = time.time() - start

print(f"브로드캐스팅 시간: {time_broadcast:.6f}초")
print(f"반복문 시간: {time_loop:.6f}초")
print(f"속도 향상: {time_loop/time_broadcast:.1f}배")

# ============================================================
# 도전 과제
# ============================================================
print("\n" + "=" * 60)
print("🎯 도전 과제")
print("=" * 60)

print("""
[과제 1] 구구단 표 생성 (2~9단)
힌트: 외적 활용

[과제 2] 두 점 집합 간의 모든 거리 계산 (거리 행렬)
힌트: 브로드캐스팅과 np.newaxis 활용

[과제 3] Min-Max 정규화 구현 (0~1 범위로 스케일링)
힌트: (x - min) / (max - min)
""")

# 과제 1 해답
print("\n[과제 1 해답] 구구단 표")
rows = np.arange(2, 10).reshape(-1, 1)  # 2~9 (열 벡터)
cols = np.arange(1, 10)                  # 1~9 (행 벡터)
multiplication_table = rows * cols
print(f"구구단 표:\n{multiplication_table}")

# 과제 2 해답
print("\n[과제 2 해답] 거리 행렬")
points_a = np.array([[0, 0], [1, 1], [2, 2]])  # 3개 점
points_b = np.array([[0, 1], [1, 2]])           # 2개 점

print(f"점 집합 A:\n{points_a}")
print(f"점 집합 B:\n{points_b}")

# 브로드캐스팅을 이용한 거리 계산
# points_a: (3, 2) → (3, 1, 2)
# points_b: (2, 2) → (1, 2, 2)
diff = points_a[:, np.newaxis, :] - points_b[np.newaxis, :, :]  # (3, 2, 2)
distances = np.sqrt(np.sum(diff ** 2, axis=2))  # (3, 2)
print(f"\n거리 행렬 (A의 각 점에서 B의 각 점까지):\n{distances}")

# 과제 3 해답
print("\n[과제 3 해답] Min-Max 정규화")
data = np.array([[10, 200, 30],
                 [40, 50, 60],
                 [70, 80, 90]])
print(f"원본 데이터:\n{data}")

# 열별 min-max 정규화
min_vals = data.min(axis=0)
max_vals = data.max(axis=0)
normalized = (data - min_vals) / (max_vals - min_vals)
print(f"\n열별 Min: {min_vals}")
print(f"열별 Max: {max_vals}")
print(f"정규화 결과:\n{normalized}")

print("\n" + "=" * 60)
print("실습 3 완료!")
print("=" * 60)