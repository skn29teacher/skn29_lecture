"""
NumPy 종합 프로젝트: 이미지 처리
================================
지금까지 배운 모든 개념을 활용한 실제 이미지 처리 프로젝트입니다.

프로젝트 목표:
1. ndarray로 이미지 데이터 다루기
2. 인덱싱/슬라이싱으로 이미지 영역 조작
3. 브로드캐스팅으로 이미지 변환
4. 선형대수로 이미지 압축 (SVD)
"""

import numpy as np

print("=" * 60)
print("🖼️ NumPy 종합 프로젝트: 이미지 처리")
print("=" * 60)

# ============================================================
# 1단계: 이미지 데이터 생성 (ndarray 활용)
# ============================================================
print("\n[1단계] 이미지 데이터 생성")
print("-" * 40)

# 8x8 그레이스케일 이미지 (0-255)
np.random.seed(42)
grayscale_image = np.random.randint(0, 256, (8, 8), dtype=np.uint8)
print(f"그레이스케일 이미지 (8x8):\n{grayscale_image}")
print(f"shape: {grayscale_image.shape}, dtype: {grayscale_image.dtype}")

# 8x8 RGB 이미지
rgb_image = np.random.randint(0, 256, (8, 8, 3), dtype=np.uint8)
print(f"\nRGB 이미지 shape: {rgb_image.shape}")
print(f"  - 행: {rgb_image.shape[0]}")
print(f"  - 열: {rgb_image.shape[1]}")
print(f"  - 채널 (RGB): {rgb_image.shape[2]}")

# 간단한 패턴 이미지 생성
print("\n[체크보드 패턴 생성]")
checkerboard = np.zeros((8, 8), dtype=np.uint8)
checkerboard[::2, 1::2] = 255
checkerboard[1::2, ::2] = 255
print(f"체크보드:\n{checkerboard}")

# 그라디언트 이미지
print("\n[그라디언트 이미지 생성]")
gradient = np.linspace(0, 255, 8).astype(np.uint8)
gradient_image = np.tile(gradient, (8, 1))
print(f"가로 그라디언트:\n{gradient_image}")

# ============================================================
# 2단계: 이미지 영역 조작 (인덱싱/슬라이싱)
# ============================================================
print("\n[2단계] 이미지 영역 조작")
print("-" * 40)

# 샘플 이미지 생성
image = np.arange(64).reshape(8, 8).astype(np.uint8) * 4
print(f"원본 이미지:\n{image}")

# 특정 영역 추출 (ROI - Region of Interest)
roi = image[2:6, 2:6]
print(f"\nROI (중앙 4x4):\n{roi}")

# 특정 영역 수정
image_modified = image.copy()
image_modified[0:2, 0:2] = 255  # 좌상단 2x2를 흰색으로
print(f"\n좌상단 수정:\n{image_modified}")

# 이미지 뒤집기
flipped_h = image[:, ::-1]  # 좌우 반전
flipped_v = image[::-1, :]  # 상하 반전
print(f"\n좌우 반전:\n{flipped_h}")
print(f"\n상하 반전:\n{flipped_v}")

# 90도 회전
rotated_90 = np.rot90(image)
print(f"\n90도 회전:\n{rotated_90}")

# 채널 분리 (RGB)
print("\n[RGB 채널 분리]")
rgb = np.random.randint(0, 256, (4, 4, 3), dtype=np.uint8)
r_channel = rgb[:, :, 0]
g_channel = rgb[:, :, 1]
b_channel = rgb[:, :, 2]
print(f"R 채널:\n{r_channel}")

# ============================================================
# 3단계: 이미지 변환 (브로드캐스팅)
# ============================================================
print("\n[3단계] 이미지 변환 (브로드캐스팅)")
print("-" * 40)

image = np.arange(64).reshape(8, 8).astype(np.float64) / 64 * 255
print(f"원본 이미지 (float):\n{image.astype(int)}")

# 밝기 조절
brightness = 50
brighter = np.clip(image + brightness, 0, 255)
darker = np.clip(image - brightness, 0, 255)
print(f"\n밝기 +50:\n{brighter.astype(int)}")

# 대비 조절
contrast = 1.5
contrasted = np.clip((image - 128) * contrast + 128, 0, 255)
print(f"\n대비 x1.5:\n{contrasted.astype(int)}")

# 반전
inverted = 255 - image
print(f"\n색상 반전:\n{inverted.astype(int)}")

# RGB to Grayscale (가중 평균)
print("\n[RGB → Grayscale 변환]")
rgb_sample = np.random.randint(0, 256, (4, 4, 3), dtype=np.float64)
weights = np.array([0.299, 0.587, 0.114])  # ITU-R BT.601
grayscale = np.sum(rgb_sample * weights, axis=2)
print(f"RGB 이미지 shape: {rgb_sample.shape}")
print(f"Grayscale shape: {grayscale.shape}")
print(f"Grayscale 결과:\n{grayscale.astype(int)}")

# 정규화
print("\n[이미지 정규화]")
image = np.random.randint(50, 200, (4, 4)).astype(np.float64)
print(f"원본:\n{image.astype(int)}")

# Min-Max 정규화 (0-1)
normalized = (image - image.min()) / (image.max() - image.min())
print(f"\n정규화 (0-1):\n{normalized}")

# 0-255로 재스케일
rescaled = (normalized * 255).astype(np.uint8)
print(f"\n재스케일 (0-255):\n{rescaled}")

# ============================================================
# 4단계: 이미지 압축 (SVD - 선형대수)
# ============================================================
print("\n[4단계] 이미지 압축 (SVD)")
print("-" * 40)

# 더 큰 이미지 생성
np.random.seed(42)
large_image = np.random.randint(0, 256, (16, 16)).astype(np.float64)
print(f"원본 이미지 크기: {large_image.shape}")
print(f"원본 데이터 요소 수: {large_image.size}")

# SVD 분해
U, S, Vt = np.linalg.svd(large_image)
print(f"\nSVD 분해:")
print(f"  U shape: {U.shape}")
print(f"  특이값 개수: {len(S)}")
print(f"  Vt shape: {Vt.shape}")

# 특이값 확인
print(f"\n특이값 (상위 5개): {S[:5].astype(int)}")

# 다양한 rank로 압축
def compress_image(U, S, Vt, k):
    """k개의 특이값만 사용하여 이미지 압축"""
    return U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]

print("\n[압축률에 따른 품질]")
for k in [1, 2, 4, 8, 16]:
    compressed = compress_image(U, S, Vt, k)
    error = np.mean((large_image - compressed) ** 2)
    
    # 저장에 필요한 요소 수
    original_size = large_image.size
    compressed_size = U[:, :k].size + k + Vt[:k, :].size
    compression_ratio = original_size / compressed_size
    
    print(f"  k={k:2d}: MSE={error:8.2f}, 압축률={compression_ratio:.2f}x")

# 최종 압축 결과 비교
print("\n[압축 결과 비교 (k=4)]")
compressed_4 = compress_image(U, S, Vt, 4)
print(f"원본 (4x4 영역):\n{large_image[:4, :4].astype(int)}")
print(f"\n압축 후 (4x4 영역):\n{compressed_4[:4, :4].astype(int)}")

# ============================================================
# 5단계: 이미지 필터링 (컨볼루션)
# ============================================================
print("\n[5단계] 이미지 필터링")
print("-" * 40)

def apply_filter(image, kernel):
    """간단한 2D 컨볼루션 (패딩 없음)"""
    h, w = image.shape
    kh, kw = kernel.shape
    output = np.zeros((h - kh + 1, w - kw + 1))
    
    for i in range(output.shape[0]):
        for j in range(output.shape[1]):
            region = image[i:i+kh, j:j+kw]
            output[i, j] = np.sum(region * kernel)
    
    return output

# 샘플 이미지
image = np.array([
    [10, 10, 10, 10, 10],
    [10, 50, 50, 50, 10],
    [10, 50, 100, 50, 10],
    [10, 50, 50, 50, 10],
    [10, 10, 10, 10, 10]
], dtype=np.float64)

print(f"원본 이미지:\n{image.astype(int)}")

# 평균 필터 (블러)
blur_kernel = np.ones((3, 3)) / 9
blurred = apply_filter(image, blur_kernel)
print(f"\n평균 필터 (블러):\n{blurred.astype(int)}")

# 샤프닝 필터
sharpen_kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
], dtype=np.float64)
sharpened = apply_filter(image, sharpen_kernel)
print(f"\n샤프닝 필터:\n{sharpened.astype(int)}")

# 에지 검출 (Sobel)
sobel_x = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
], dtype=np.float64)

sobel_y = np.array([
    [-1, -2, -1],
    [0, 0, 0],
    [1, 2, 1]
], dtype=np.float64)

edge_x = apply_filter(image, sobel_x)
edge_y = apply_filter(image, sobel_y)
edge_magnitude = np.sqrt(edge_x**2 + edge_y**2)

print(f"\n에지 강도 (Sobel):\n{edge_magnitude.astype(int)}")

# ============================================================
# 6단계: 이미지 통계 분석
# ============================================================
print("\n[6단계] 이미지 통계 분석")
print("-" * 40)

image = np.random.randint(0, 256, (8, 8)).astype(np.float64)
print(f"이미지 (8x8):\n{image.astype(int)}")

# 기본 통계
print(f"\n[기본 통계]")
print(f"  최솟값: {image.min():.0f}")
print(f"  최댓값: {image.max():.0f}")
print(f"  평균: {image.mean():.2f}")
print(f"  표준편차: {image.std():.2f}")
print(f"  중앙값: {np.median(image):.2f}")

# 히스토그램 (간단 버전)
print(f"\n[히스토그램 (구간별 픽셀 수)]")
bins = [0, 64, 128, 192, 256]
hist, _ = np.histogram(image, bins=bins)
for i in range(len(bins)-1):
    bar = '█' * (hist[i] // 2)
    print(f"  {bins[i]:3d}-{bins[i+1]:3d}: {hist[i]:2d} {bar}")

# 퍼센타일
print(f"\n[퍼센타일]")
for p in [10, 25, 50, 75, 90]:
    print(f"  {p}%: {np.percentile(image, p):.1f}")

# ============================================================
# 최종 요약
# ============================================================
print("\n" + "=" * 60)
print("📋 프로젝트 요약")
print("=" * 60)

print("""
✅ ndarray 생성: 이미지를 다차원 배열로 표현
   - 그레이스케일: 2D 배열 (H, W)
   - RGB: 3D 배열 (H, W, 3)

✅ 인덱싱/슬라이싱: 이미지 영역 조작
   - ROI 추출, 뒤집기, 회전
   - 채널 분리

✅ 브로드캐스팅: 이미지 변환
   - 밝기/대비 조절
   - RGB → Grayscale
   - 정규화

✅ 선형대수: 이미지 압축
   - SVD를 이용한 이미지 압축
   - 특이값 분해와 근사

✅ 추가 응용: 필터링, 통계 분석
""")

# ============================================================
# 추가 과제
# ============================================================
print("=" * 60)
print("🎯 추가 도전 과제")
print("=" * 60)

print("""
[과제 1] 이미지 모자이크
        - 이미지를 4x4 블록으로 나누고
        - 각 블록을 블록 평균값으로 채우기

[과제 2] 간단한 이미지 블렌딩
        - 두 이미지를 α 값으로 혼합
        - blended = α * img1 + (1-α) * img2

[과제 3] PCA를 이용한 차원 축소
        - 여러 이미지를 벡터화하고
        - 주성분 분석으로 특징 추출
""")

# 과제 1 해답
print("\n[과제 1 해답] 이미지 모자이크")
image = np.arange(64).reshape(8, 8).astype(np.float64)
print(f"원본:\n{image.astype(int)}")

mosaic = image.copy()
block_size = 2
for i in range(0, 8, block_size):
    for j in range(0, 8, block_size):
        block = image[i:i+block_size, j:j+block_size]
        mosaic[i:i+block_size, j:j+block_size] = block.mean()

print(f"\n모자이크 (2x2 블록):\n{mosaic.astype(int)}")

# 과제 2 해답
print("\n[과제 2 해답] 이미지 블렌딩")
img1 = np.zeros((4, 4)) + 100
img2 = np.ones((4, 4)) * 200

alpha = 0.3
blended = alpha * img1 + (1 - alpha) * img2
print(f"이미지 1 (100):\n{img1.astype(int)}")
print(f"\n이미지 2 (200):\n{img2.astype(int)}")
print(f"\n블렌딩 (α=0.3):\n{blended.astype(int)}")

print("\n" + "=" * 60)
print("🎉 프로젝트 완료!")
print("=" * 60)
