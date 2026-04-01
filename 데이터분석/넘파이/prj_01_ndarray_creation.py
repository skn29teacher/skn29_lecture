"""
NumPy 실습 1: ndarray 생성
============================
이 실습에서는 다양한 방법으로 NumPy 배열을 생성하는 방법을 학습합니다.
"""

import numpy as np

print("=" * 60)
print("NumPy ndarray 생성 실습")
print("=" * 60)

# ============================================================
# 실습 1-1: 리스트로부터 배열 생성
# ============================================================
print("\n[실습 1-1] 리스트로부터 배열 생성")
print("-" * 40)

# TODO: 1차원 배열 생성 (1~5)
arr1d = np.array([1, 2, 3, 4, 5])
print(f"1차원 배열: {arr1d}")
print(f"  - shape: {arr1d.shape}")
print(f"  - ndim: {arr1d.ndim}")
print(f"  - dtype: {arr1d.dtype}")

# TODO: 2차원 배열 생성 (3x3)
arr2d = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
print(f"\n2차원 배열:\n{arr2d}")
print(f"  - shape: {arr2d.shape}")
print(f"  - ndim: {arr2d.ndim}")

# TODO: 3차원 배열 생성 (2x2x3)
arr3d = np.array([[[1, 2, 3], [4, 5, 6]],
                  [[7, 8, 9], [10, 11, 12]]])
print(f"\n3차원 배열 shape: {arr3d.shape}")

# ============================================================
# 실습 1-2: 특수 배열 생성
# ============================================================
print("\n[실습 1-2] 특수 배열 생성")
print("-" * 40)

# TODO: zeros - 0으로 채워진 배열 생성 (3x4)
zeros_arr = np.zeros((3, 4))
print(f"zeros (3x4):\n{zeros_arr}")

# TODO: ones - 1로 채워진 배열 생성 (2x3)
ones_arr = np.ones((2, 3))
print(f"\nones (2x3):\n{ones_arr}")

# TODO: full - 특정 값으로 채워진 배열 생성 (2x2, 값=7)
full_arr = np.full((2, 2), 7)
print(f"\nfull (2x2, value=7):\n{full_arr}")

# TODO: eye - 단위 행렬 생성 (4x4)
eye_arr = np.eye(4)
print(f"\neye (4x4):\n{eye_arr}")

# TODO: diag - 대각 행렬 생성
diag_arr = np.diag([1, 2, 3, 4])
print(f"\ndiag([1,2,3,4]):\n{diag_arr}")

# ============================================================
# 실습 1-3: 수열 생성
# ============================================================
print("\n[실습 1-3] 수열 생성")
print("-" * 40)

# TODO: arange - 0부터 9까지 정수 배열
arr_arange1 = np.arange(10)
print(f"arange(10): {arr_arange1}")

# TODO: arange - 5부터 15까지 2씩 증가
arr_arange2 = np.arange(5, 15, 2)
print(f"arange(5, 15, 2): {arr_arange2}")

# TODO: linspace - 0부터 1까지 5개로 균등 분할
arr_linspace = np.linspace(0, 1, 5)
print(f"linspace(0, 1, 5): {arr_linspace}")

# TODO: linspace - 0부터 100까지 11개로 균등 분할
arr_linspace2 = np.linspace(0, 100, 11)
print(f"linspace(0, 100, 11): {arr_linspace2}")

# TODO: logspace - 10^0 부터 10^3까지 4개
arr_logspace = np.logspace(0, 3, 4)
print(f"logspace(0, 3, 4): {arr_logspace}")

# ============================================================
# 실습 1-4: 난수 배열 생성
# ============================================================
print("\n[실습 1-4] 난수 배열 생성")
print("-" * 40)

# 재현성을 위한 시드 설정
np.random.seed(42)

# TODO: rand - 0~1 균등 분포 난수 (3x3)
rand_uniform = np.random.rand(3, 3)
print(f"균등 분포 난수 (3x3):\n{rand_uniform}")

# TODO: randn - 표준 정규 분포 난수 (3x3)
rand_normal = np.random.randn(3, 3)
print(f"\n정규 분포 난수 (3x3):\n{rand_normal}")

# TODO: randint - 0~10 정수 난수 (3x3)
rand_int = np.random.randint(0, 10, size=(3, 3))
print(f"\n정수 난수 0~10 (3x3):\n{rand_int}")

# TODO: choice - 리스트에서 무작위 선택
choices = np.random.choice(['A', 'B', 'C', 'D'], size=5)
print(f"\n무작위 선택: {choices}")

# ============================================================
# 실습 1-5: dtype 지정과 변환
# ============================================================
print("\n[실습 1-5] dtype 지정과 변환")
print("-" * 40)

# TODO: float32로 배열 생성
arr_float32 = np.array([1, 2, 3], dtype=np.float32)
print(f"float32 배열: {arr_float32}, dtype: {arr_float32.dtype}")

# TODO: complex128로 배열 생성
arr_complex = np.array([1, 2, 3], dtype=np.complex128)
print(f"complex128 배열: {arr_complex}, dtype: {arr_complex.dtype}")

# TODO: astype으로 형변환
arr_int = np.array([1.7, 2.3, 3.9])
arr_converted = arr_int.astype(np.int32)
print(f"\n원본 (float): {arr_int}")
print(f"변환 (int32): {arr_converted}")

# ============================================================
# 실습 1-6: reshape
# ============================================================
print("\n[실습 1-6] reshape")
print("-" * 40)

# 1차원 배열 생성
arr = np.arange(12)
print(f"원본 배열: {arr}")

# TODO: (3, 4)로 reshape
arr_3x4 = arr.reshape(3, 4)
print(f"\nreshape(3, 4):\n{arr_3x4}")

# TODO: (2, 6)로 reshape
arr_2x6 = arr.reshape(2, 6)
print(f"\nreshape(2, 6):\n{arr_2x6}")

# TODO: (2, 2, 3)로 reshape
arr_2x2x3 = arr.reshape(2, 2, 3)
print(f"\nreshape(2, 2, 3):\n{arr_2x2x3}")

# TODO: -1 사용 (자동 계산)
arr_auto = arr.reshape(4, -1)
print(f"\nreshape(4, -1) -> shape: {arr_auto.shape}")

# ============================================================
# 도전 과제
# ============================================================
print("\n" + "=" * 60)
print("🎯 도전 과제")
print("=" * 60)

print("""
[과제 1] 1부터 100까지의 숫자 중 3의 배수만 포함하는 배열 생성
힌트: np.arange와 step 활용

[과제 2] 5x5 체크보드 패턴 생성 (0과 1이 번갈아 나타남)
힌트: zeros로 시작, 슬라이싱으로 값 채우기

[과제 3] 평균이 50, 표준편차가 10인 정규분포에서 1000개 샘플 추출 후
         기본 통계량(평균, 표준편차, 최소, 최대) 출력
힌트: np.random.normal 사용
""")

# 과제 1 해답
print("\n[과제 1 해답]")
multiples_of_3 = np.arange(3, 101, 3)
print(f"3의 배수: {multiples_of_3}")

# 과제 2 해답
print("\n[과제 2 해답]")
checkerboard = np.zeros((5, 5), dtype=int)
checkerboard[::2, 1::2] = 1
checkerboard[1::2, ::2] = 1
print(f"체크보드:\n{checkerboard}")

# 과제 3 해답
print("\n[과제 3 해답]")
samples = np.random.normal(loc=50, scale=10, size=1000)
print(f"평균: {samples.mean():.2f}")
print(f"표준편차: {samples.std():.2f}")
print(f"최소: {samples.min():.2f}")
print(f"최대: {samples.max():.2f}")

print("\n" + "=" * 60)
print("실습 1 완료!")
print("=" * 60)
