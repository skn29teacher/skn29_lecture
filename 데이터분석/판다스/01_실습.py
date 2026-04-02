"""
Pandas Series 기초 실습
세션 1: Series 구조 이해 및 기본 조작

학습 목표:
1. Series 생성 방법 이해
2. 인덱싱과 슬라이싱 연습
3. 벡터화 연산 및 통계 함수 활용
4. 결측치 처리 방법 학습
"""

import pandas as pd
import numpy as np

print("=" * 60)
print("1. Series 생성 - 리스트로 생성")
print("=" * 60)

# 1.1 기본 생성 (자동 인덱스: 0, 1, 2, 3, ...)
scores = pd.Series([85, 92, 78, 95, 88])
print("\\n학생 점수 (자동 인덱스):")
print(scores)
print(f"\\n데이터 타입: {scores.dtype}")
print(f"크기: {scores.shape}")
print(f"요소 개수: {scores.size}")

# 1.2 사용자 정의 인덱스
scores_named = pd.Series(
    [85, 92, 78, 95, 88],
    index=['김철수', '이영희', '박민수', '정수진', '최영수']
)
print("\\n\\n학생 점수 (이름 인덱스):")
print(scores_named)


print("\\n" + "=" * 60)
print("2. Series 생성 - 딕셔너리로 생성")
print("=" * 60)

# 2.1 도시별 인구 데이터
population = pd.Series({
    '서울': 9720846,
    '부산': 3404423,
    '인천': 2947217,
    '대구': 2427954,
    '대전': 1471040
})
print("\\n도시별 인구:")
print(population)

# 2.2 제품별 가격
product_prices = pd.Series({
    'Apple': 1000,
    'Banana': 500,
    'Orange': 800,
    'Grape': 1500,
    'Melon': 3000
})
print("\\n\\n제품 가격:")
print(product_prices)


print("\\n" + "=" * 60)
print("3. Series 생성 - 스칼라 값으로 생성")
print("=" * 60)

# 3.1 모든 값이 동일한 Series
constant_series = pd.Series(100, index=['A', 'B', 'C', 'D', 'E'])
print("\\n초기 재고:")
print(constant_series)


print("\\n" + "=" * 60)
print("4. Series 인덱싱과 슬라이싱")
print("=" * 60)

# 4.1 단일 요소 접근
print(f"\\n김철수의 점수: {scores_named['김철수']}")
print(f"첫 번째 학생 점수: {scores_named[0]}")

# 4.2 슬라이싱
print("\\n처음 3명의 점수:")
print(scores_named[0:3])

# 4.3 여러 요소 선택
print("\\n특정 학생들의 점수:")
print(scores_named[['김철수', '정수진', '최영수']])

# 4.4 인덱스 음수 사용
print(f"\\n마지막 학생 점수: {scores_named[-1]}")


print("\\n" + "=" * 60)
print("5. Boolean 인덱싱 (조건 필터링)")
print("=" * 60)

# 5.1 단일 조건
print("\\n90점 이상 학생:")
high_scores = scores_named[scores_named >= 90]
print(high_scores)

# 5.2 복합 조건
print("\\n80점 이상 90점 미만 학생:")
mid_scores = scores_named[(scores_named >= 80) & (scores_named < 90)]
print(mid_scores)

# 5.3 인구 100만 이상 도시
print("\\n인구 200만 이상 도시:")
large_cities = population[population >= 2000000]
print(large_cities)


print("\\n" + "=" * 60)
print("6. Series 벡터화 연산")
print("=" * 60)

# 6.1 산술 연산
print("\\n모든 점수에 5점 추가:")
print(scores_named + 5)

print("\\n모든 점수에 1.1배:")
print(scores_named * 1.1)

# 6.2 제품 가격 할인
print("\\n모든 제품 10% 할인 가격:")
discounted_prices = product_prices * 0.9
print(discounted_prices)


print("\\n" + "=" * 60)
print("7. Series 통계 함수")
print("=" * 60)

print(f"\\n평균 점수: {scores_named.mean():.2f}")
print(f"최고 점수: {scores_named.max()}")
print(f"최저 점수: {scores_named.min()}")
print(f"표준편차: {scores_named.std():.2f}")
print(f"중앙값: {scores_named.median():.2f}")
print(f"합계: {scores_named.sum()}")

print("\\n기술 통계 요약:")
print(scores_named.describe())

# 인구 통계
print("\\n\\n인구 통계:")
print(population.describe())


print("\\n" + "=" * 60)
print("8. Series 간 연산")
print("=" * 60)

# 8.1 중간고사와 기말고사 점수
midterm = pd.Series([85, 92, 78], index=['김철수', '이영희', '박민수'])
final = pd.Series([88, 90, 82], index=['김철수', '이영희', '박민수'])

print("\\n중간고사:")
print(midterm)
print("\\n기말고사:")
print(final)

print("\\n총점:")
total = midterm + final
print(total)

print("\\n평균:")
average = (midterm + final) / 2
print(average)


print("\\n" + "=" * 60)
print("9. 결측치 처리")
print("=" * 60)

# 9.1 결측치가 있는 Series 생성
data_with_nan = pd.Series([10, 20, np.nan, 40, np.nan, 60])
print("\\n결측치가 있는 데이터:")
print(data_with_nan)

# 9.2 결측치 확인
print("\\n결측치 확인 (isnull):")
print(data_with_nan.isnull())

print(f"\\n결측치 개수: {data_with_nan.isnull().sum()}")
print(f"유효한 데이터 개수: {data_with_nan.notnull().sum()}")

# 9.3 결측치 제거
print("\\n결측치 제거:")
print(data_with_nan.dropna())

# 9.4 결측치를 0으로 채우기
print("\\n결측치를 0으로 채우기:")
print(data_with_nan.fillna(0))

# 9.5 결측치를 평균으로 채우기
print("\\n결측치를 평균으로 채우기:")
print(data_with_nan.fillna(data_with_nan.mean()))

# 9.6 결측치를 앞의 값으로 채우기 (forward fill)
print("\\n결측치를 앞의 값으로 채우기:")
print(data_with_nan.fillna(method='ffill'))


print("\\n" + "=" * 60)
print("10. Series 정렬")
print("=" * 60)

# 10.1 값 기준 정렬
print("\\n점수 오름차순 정렬:")
print(scores_named.sort_values())

print("\\n점수 내림차순 정렬:")
print(scores_named.sort_values(ascending=False))

# 10.2 인덱스 기준 정렬
print("\\n이름 순 정렬:")
print(scores_named.sort_index())

# 10.3 인구 순 정렬
print("\\n인구 많은 순서:")
print(population.sort_values(ascending=False))


print("\\n" + "=" * 60)
print("11. 실전 예제 1: 월별 매출 데이터 분석")
print("=" * 60)

# 월별 매출 데이터 (단위: 백만원)
monthly_sales = pd.Series({
    '1월': 150,
    '2월': 180,
    '3월': 210,
    '4월': 190,
    '5월': 220,
    '6월': 250,
    '7월': 280,
    '8월': 260,
    '9월': 240,
    '10월': 270,
    '11월': 290,
    '12월': 310
})

print("\\n월별 매출:")
print(monthly_sales)

print(f"\\n총 매출: {monthly_sales.sum()}백만원")
print(f"평균 매출: {monthly_sales.mean():.2f}백만원")
print(f"최고 매출 달: {monthly_sales.idxmax()}")
print(f"최고 매출액: {monthly_sales.max()}백만원")

print("\\n매출 200백만원 이상인 달:")
print(monthly_sales[monthly_sales >= 200])

# 전년 대비 성장률 (가정: 5% 증가)
print("\\n전년 동월 대비 매출 (5% 감소 가정):")
previous_year = monthly_sales / 1.05
print(previous_year.round(2))


print("\\n" + "=" * 60)
print("12. 실전 예제 2: 학급 성적 관리")
print("=" * 60)

# 학생들의 수학 점수
math_scores = pd.Series({
    '학생1': 85,
    '학생2': 92,
    '학생3': 78,
    '학생4': 95,
    '학생5': 88,
    '학생6': 76,
    '학생7': 90,
    '학생8': 82,
    '학생9': 87,
    '학생10': 91
})

print("\\n수학 점수:")
print(math_scores)

print(f"\\n반 평균: {math_scores.mean():.2f}점")
print(f"1등 점수: {math_scores.max()}점")
print(f"꼴등 점수: {math_scores.min()}점")
print(f"점수 범위: {math_scores.max() - math_scores.min()}점")

# 등급 부여 (90점 이상 A, 80점 이상 B, 70점 이상 C, 그 외 D)
print("\\nA등급 (90점 이상) 학생:")
print(math_scores[math_scores >= 90])

print("\\nB등급 (80-89점) 학생:")
print(math_scores[(math_scores >= 80) & (math_scores < 90)])

print("\\nC등급 (70-79점) 학생:")
print(math_scores[(math_scores >= 70) & (math_scores < 80)])

# 표준화 점수 (Z-score)
print("\\n표준화 점수:")
z_scores = (math_scores - math_scores.mean()) / math_scores.std()
print(z_scores.round(2))


print("\\n" + "=" * 60)
print("13. 실전 예제 3: 주식 가격 변동 분석")
print("=" * 60)

# 일주일간 주식 종가
stock_prices = pd.Series({
    '월': 50000,
    '화': 51500,
    '수': 50800,
    '목': 52300,
    '금': 53000
})

print("\\n일별 주식 가격:")
print(stock_prices)

# 일일 변동액
print("\\n일일 변동액:")
daily_changes = stock_prices.diff()
print(daily_changes)

# 일일 변동률 (%)
print("\\n일일 변동률 (%):")
daily_returns = stock_prices.pct_change() * 100
print(daily_returns.round(2))

print(f"\\n주간 수익률: {((stock_prices['금'] - stock_prices['월']) / stock_prices['월'] * 100):.2f}%")
print(f"최고가: {stock_prices.max():,}원")
print(f"최저가: {stock_prices.min():,}원")
print(f"변동폭: {stock_prices.max() - stock_prices.min():,}원")


print("\\n" + "=" * 60)
print("14. Series 주요 메서드 정리")
print("=" * 60)

sample = pd.Series([5, 2, 8, 1, 9, 3, 7])

print(f"\\nhead(3): 처음 3개\\n{sample.head(3)}")
print(f"\\ntail(3): 마지막 3개\\n{sample.tail(3)}")
print(f"\\nunique(): 고유값\\n{sample.unique()}")
print(f"\\nvalue_counts(): 값 빈도수\\n{sample.value_counts()}")
print(f"\\nnunique(): 고유값 개수\\n{sample.nunique()}")


print("\\n" + "=" * 60)
print("Series 기초 실습 완료!")
print("=" * 60)
