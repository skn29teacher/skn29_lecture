"""
Pandas 인덱스 조작 및 데이터 필터링 실습
세션 4: 고급 데이터 접근 및 필터링 기법

학습 목표:
1. 인덱스 설정 및 재설정
2. loc/iloc 마스터하기
3. Boolean 인덱싱 및 query()
4. 날짜 인덱스 활용
5. MultiIndex 다루기
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("=" * 60)
print("1. 인덱스 기본 조작")
print("=" * 60)

# 샘플 데이터 생성
data = {
    'employee_id': range(1, 11),
    'name': ['김철수', '이영희', '박민수', '정수진', '최영수', 
             '한지민', '오세훈', '강민아', '윤서준', '임채원'],
    'department': ['영업', '개발', '개발', '영업', '인사',
                   '개발', '영업', '인사', '개발', '영업'],
    'age': [28, 32, 35, 29, 40, 26, 38, 31, 42, 27],
    'salary': [3500, 4500, 5000, 3800, 6000, 3200, 5500, 4200, 6500, 3600]
}
df = pd.DataFrame(data)

print("\n원본 데이터:")
print(df)

print("\n기본 인덱스:")
print(df.index)

# 인덱스를 employee_id로 설정
df_indexed = df.set_index('employee_id')
print("\nemployee_id를 인덱스로:")
print(df_indexed)

# 인덱스 이름 설정
df_indexed.index.name = '직원번호'
print("\n인덱스 이름 변경:")
print(df_indexed.head())

# 인덱스 재설정 (컬럼으로 복귀)
df_reset = df_indexed.reset_index()
print("\n인덱스 재설정:")
print(df_reset.head())


print("\n" + "=" * 60)
print("2. loc - 레이블 기반 인덱싱")
print("=" * 60)

df = df.set_index('employee_id')

# 단일 행 접근
print("\n직원 ID 3번:")
print(df.loc[3])

# 여러 행 접근
print("\n직원 ID 2, 4, 6번:")
print(df.loc[[2, 4, 6]])

# 슬라이싱 (끝 포함!)
print("\n직원 ID 3~5번:")
print(df.loc[3:5])

# 특정 행의 특정 컬럼
print(f"\n직원 ID 2번의 이름: {df.loc[2, 'name']}")
print(f"직원 ID 5번의 급여: {df.loc[5, 'salary']}")

# 여러 행의 여러 컬럼
print("\n직원 ID 1~3번의 이름과 급여:")
print(df.loc[1:3, ['name', 'salary']])

# 모든 행의 특정 컬럼
print("\n모든 직원의 부서:")
print(df.loc[:, 'department'])


print("\n" + "=" * 60)
print("3. iloc - 위치 기반 인덱싱")
print("=" * 60)

# 단일 행
print("\n첫 번째 직원:")
print(df.iloc[0])

# 여러 행
print("\n첫 번째, 세 번째, 다섯 번째 직원:")
print(df.iloc[[0, 2, 4]])

# 슬라이싱 (끝 미포함!)
print("\n처음 3명:")
print(df.iloc[0:3])

# 특정 위치의 값
print(f"\n0행 1열의 값: {df.iloc[0, 1]}")

# 범위 선택
print("\n처음 3행, 처음 2열:")
print(df.iloc[0:3, 0:2])

# 음수 인덱스 (뒤에서부터)
print("\n마지막 3명:")
print(df.iloc[-3:])


print("\n" + "=" * 60)
print("4. Boolean 인덱싱 - 단일 조건")
print("=" * 60)

# 나이가 30 이상
print("\n나이 30세 이상:")
senior = df[df['age'] >= 30]
print(senior[['name', 'age']])

# 개발팀 직원
print("\n개발팀:")
devs = df[df['department'] == '개발']
print(devs[['name', 'department']])

# 급여 5000 이상
print("\n급여 5000 이상:")
high_earners = df[df['salary'] >= 5000]
print(high_earners[['name', 'salary']])


print("\n" + "=" * 60)
print("5. Boolean 인덱싱 - 복합 조건")
print("=" * 60)

# AND 조건 (&)
print("\n나이 30 이상 AND 급여 5000 이상:")
condition = (df['age'] >= 30) & (df['salary'] >= 5000)
print(df[condition][['name', 'age', 'salary']])

# OR 조건 (|)
print("\n영업팀 OR 인사팀:")
condition = (df['department'] == '영업') | (df['department'] == '인사')
print(df[condition][['name', 'department']])

# NOT 조건 (~)
print("\n개발팀이 아닌 직원:")
condition = ~(df['department'] == '개발')
print(df[condition][['name', 'department']])

# 여러 조건 조합
print("\n개발팀이고 나이 35 이상이거나 급여 6000 이상:")
condition = (df['department'] == '개발') & ((df['age'] >= 35) | (df['salary'] >= 6000))
print(df[condition][['name', 'department', 'age', 'salary']])


print("\n" + "=" * 60)
print("6. isin()과 between() 메서드")
print("=" * 60)

# isin() - 특정 값들에 포함
print("\n영업팀 또는 개발팀:")
departments = ['영업', '개발']
print(df[df['department'].isin(departments)][['name', 'department']])

# isin() 제외
print("\n영업팀과 개발팀 제외:")
print(df[~df['department'].isin(departments)][['name', 'department']])

# between() - 범위
print("\n나이 30~35세:")
print(df[df['age'].between(30, 35)][['name', 'age']])

print("\n급여 4000~5500:")
print(df[df['salary'].between(4000, 5500)][['name', 'salary']])


print("\n" + "=" * 60)
print("7. query() 메서드")
print("=" * 60)

# 기본 쿼리
print("\n나이 30 이상 (query):")
print(df.query('age >= 30')[['name', 'age']])

# 복합 조건
print("\n나이 30 이상 AND 급여 5000 이상:")
print(df.query('age >= 30 and salary >= 5000')[['name', 'age', 'salary']])

# 변수 사용
min_age = 35
print(f"\n나이 {min_age} 이상:")
print(df.query('age >= @min_age')[['name', 'age']])

# 리스트 변수
target_depts = ['영업', '인사']
print("\n영업팀 또는 인사팀:")
print(df.query('department in @target_depts')[['name', 'department']])


print("\n" + "=" * 60)
print("8. 조건부 값 변경")
print("=" * 60)

df_copy = df.copy()

# loc를 이용한 변경
df_copy.loc[df_copy['age'] >= 35, 'level'] = 'Senior'
df_copy.loc[df_copy['age'] < 35, 'level'] = 'Junior'

print("\n연령대별 레벨 할당:")
print(df_copy[['name', 'age', 'level']])

# numpy.where() 사용
df_copy['salary_grade'] = np.where(df_copy['salary'] >= 5000, 'High', 'Normal')

print("\n급여 등급:")
print(df_copy[['name', 'salary', 'salary_grade']])

# 다중 조건 (중첩)
df_copy['performance'] = np.where(
    df_copy['salary'] >= 6000, 'Excellent',
    np.where(df_copy['salary'] >= 5000, 'Good',
             np.where(df_copy['salary'] >= 4000, 'Average', 'Below Average'))
)

print("\n성과 평가:")
print(df_copy[['name', 'salary', 'performance']])


print("\n" + "=" * 60)
print("9. cut()과 qcut() - 구간 나누기")
print("=" * 60)

# cut() - 동일 너비 구간
bins = [20, 30, 40, 50]
labels = ['20대', '30대', '40대']
df_copy['age_group'] = pd.cut(df_copy['age'], bins=bins, labels=labels)

print("\n연령대 그룹:")
print(df_copy[['name', 'age', 'age_group']])

# qcut() - 분위수로 나누기
df_copy['salary_quartile'] = pd.qcut(df_copy['salary'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])

print("\n급여 분위수:")
print(df_copy[['name', 'salary', 'salary_quartile']])


print("\n" + "=" * 60)
print("10. 샘플링")
print("=" * 60)

# 무작위 3명 샘플
print("\n무작위 3명:")
print(df.sample(n=3)[['name', 'department']])

# 20% 샘플링
print(f"\n20% 샘플링 ({int(len(df) * 0.2)}명):")
print(df.sample(frac=0.2)[['name', 'department']])

# 시드 고정 (재현성)
print("\n시드 고정 샘플 (random_state=42):")
print(df.sample(n=3, random_state=42)[['name', 'department']])

# 상위 3명 (급여 기준)
print("\n급여 상위 3명:")
print(df.nlargest(3, 'salary')[['name', 'salary']])

# 하위 3명 (나이 기준)
print("\n나이 하위 3명:")
print(df.nsmallest(3, 'age')[['name', 'age']])


print("\n" + "=" * 60)
print("11. 중복 데이터 처리")
print("=" * 60)

# 중복이 있는 데이터 생성
duplicate_data = pd.DataFrame({
    'name': ['김철수', '이영희', '박민수', '김철수', '이영희', '정수진'],
    'department': ['영업', '개발', '인사', '영업', '개발', '영업'],
    'salary': [3500, 4500, 4000, 3500, 4500, 3800]
})

print("\n중복이 있는 데이터:")
print(duplicate_data)

# 중복 확인
print("\n중복 행 확인:")
print(duplicate_data.duplicated())

print(f"\n중복 행 개수: {duplicate_data.duplicated().sum()}")

# 중복 제거 (첫 번째 유지)
print("\n중복 제거 (첫 번째 유지):")
print(duplicate_data.drop_duplicates())

# 특정 컬럼 기준 중복 제거
print("\nname 컬럼 기준 중복 제거:")
print(duplicate_data.drop_duplicates(subset=['name']))

# 마지막 항목 유지
print("\n중복 제거 (마지막 유지):")
print(duplicate_data.drop_duplicates(keep='last'))


print("\n" + "=" * 60)
print("12. 날짜 인덱스 다루기")
print("=" * 60)

# 날짜 데이터 생성
dates = pd.date_range('2024-01-01', periods=365, freq='D')
sales_data = pd.DataFrame({
    'date': dates,
    'sales': np.random.randint(100, 500, 365),
    'customers': np.random.randint(50, 200, 365)
})

# 날짜를 인덱스로 설정
sales_data.set_index('date', inplace=True)

print("\n매출 데이터 (처음 5일):")
print(sales_data.head())

# 특정 날짜 접근
print("\n2024년 1월 1일 매출:")
print(sales_data.loc['2024-01-01'])

# 날짜 범위 접근
print("\n2024년 1월 1일~5일:")
print(sales_data.loc['2024-01-01':'2024-01-05'])

# 월별 접근
print("\n2024년 3월 데이터 (처음 5일):")
print(sales_data.loc['2024-03'].head())

# 날짜 속성 활용
print("\n1월 데이터 (month로 필터):")
january = sales_data[sales_data.index.month == 1]
print(f"1월 데이터: {len(january)}일")
print(january.head())

# 요일별 분석
sales_data['dayofweek'] = sales_data.index.dayofweek
sales_data['is_weekend'] = sales_data['dayofweek'].isin([5, 6])

print("\n주말 매출 (처음 10건):")
weekend_sales = sales_data[sales_data['is_weekend']]
print(weekend_sales.head(10))


print("\n" + "=" * 60)
print("13. MultiIndex (계층적 인덱스)")
print("=" * 60)

# MultiIndex 데이터 생성
cities = ['서울', '서울', '서울', '부산', '부산', '부산']
depts = ['영업', '개발', '인사', '영업', '개발', '인사']
multi_data = pd.DataFrame({
    'city': cities,
    'department': depts,
    'employees': [10, 15, 5, 8, 12, 4],
    'avg_salary': [4000, 5000, 4500, 3800, 4800, 4200]
})

# MultiIndex 설정
df_multi = multi_data.set_index(['city', 'department'])
print("\nMultiIndex DataFrame:")
print(df_multi)

# 외부 인덱스로 접근
print("\n서울 지점:")
print(df_multi.loc['서울'])

# 특정 조합 접근
print("\n서울 영업팀:")
print(df_multi.loc[('서울', '영업')])

# xs() 메서드
print("\n모든 영업팀 (xs 사용):")
print(df_multi.xs('영업', level='department'))

# 인덱스 재설정
print("\nMultiIndex 해제:")
print(df_multi.reset_index())


print("\n" + "=" * 60)
print("14. 실전 예제 1: 고객 데이터 분석")
print("=" * 60)

# 고객 데이터 로드 및 분석
customers = pd.read_json('data/customers.json')

print("\n고객 데이터:")
print(customers.head())

# 도시별 필터링
print("\n서울 고객:")
seoul_customers = customers[customers['city'] == '서울']
print(seoul_customers[['name', 'city']])

# 이메일 도메인 분석
customers['email_domain'] = customers['email'].str.split('@').str[1]
print("\n이메일 도메인별 고객 수:")
print(customers['email_domain'].value_counts())

# 가입일 기준 필터링
customers['join_date'] = pd.to_datetime(customers['join_date'])
recent_customers = customers[customers['join_date'] >= '2024-07-01']
print(f"\n2024년 7월 이후 가입 고객: {len(recent_customers)}명")


print("\n" + "=" * 60)
print("15. 실전 예제 2: 제품 재고 관리")
print("=" * 60)

products = pd.read_csv('data/products.csv', encoding='utf-8-sig')

print("\n제품 데이터:")
print(products.head())

# 저재고 제품
low_stock = products[products['stock'] < 30]
print(f"\n저재고 제품 ({len(low_stock)}개):")
print(low_stock[['product_name', 'stock', 'supplier']])

# 카테고리별 필터링
print("\n전자제품:")
electronics = products[products['category'] == '전자제품']
print(electronics[['product_name', 'price', 'stock']])

# 가격대별 분류
products['price_range'] = pd.cut(products['price'], 
                                  bins=[0, 50000, 200000, 1000000],
                                  labels=['저가', '중가', '고가'])

print("\n가격대별 제품 수:")
print(products['price_range'].value_counts())

# 공급업체별 제품 수
print("\n공급업체별 제품 수:")
print(products['supplier'].value_counts())

# 재입고 필요 제품 (재고 20개 미만, 가격 100,000원 이상)
restock_needed = products[(products['stock'] < 20) & (products['price'] >= 100000)]
print(f"\n긴급 재입고 필요: {len(restock_needed)}개")
print(restock_needed[['product_name', 'stock', 'price']])


print("\n" + "=" * 60)
print("16. 실전 예제 3: 성적 데이터 분석")
print("=" * 60)

students = pd.read_csv('data/students.csv', encoding='utf-8-sig')

# 학생 ID를 인덱스로
students.set_index('student_id', inplace=True)

print("\n학생 데이터:")
print(students.head())

# 총점과 평균 계산
students['total'] = students[['math', 'english', 'science']].sum(axis=1)
students['average'] = students[['math', 'english', 'science']].mean(axis=1)

# 성적 등급 부여
students['grade_level'] = pd.cut(students['average'],
                                   bins=[0, 70, 80, 90, 100],
                                   labels=['D', 'C', 'B', 'A'])

print("\n성적 등급:")
print(students[['name', 'average', 'grade_level']].head(10))

# 우수 학생 (평균 85점 이상)
excellent = students[students['average'] >= 85]
print(f"\n우수 학생: {len(excellent)}명")
print(excellent[['name', 'average']])

# 과목별 우수자 (90점 이상)
print("\n수학 우수자:")
math_excellent = students[students['math'] >= 90]
print(math_excellent[['name', 'math']])

# 여러 조건: 평균 80점 이상이고 모든 과목 70점 이상
all_pass = students[
    (students['average'] >= 80) &
    (students['math'] >= 70) &
    (students['english'] >= 70) &
    (students['science'] >= 70)
]
print(f"\n모든 과목 70점 이상 + 평균 80점 이상: {len(all_pass)}명")


print("\n" + "=" * 60)
print("17. 성능 비교: 반복문 vs 벡터화")
print("=" * 60)

import time

# 테스트 데이터
test_df = pd.DataFrame({
    'value': np.random.randint(1, 100, 10000)
})

# 방법 1: 반복문 (느림)
start = time.time()
test_df['category_loop'] = ''
for idx in test_df.index:
    if test_df.loc[idx, 'value'] >= 50:
        test_df.loc[idx, 'category_loop'] = 'High'
    else:
        test_df.loc[idx, 'category_loop'] = 'Low'
loop_time = time.time() - start

# 방법 2: 벡터화 (빠름)
start = time.time()
test_df['category_vectorized'] = np.where(test_df['value'] >= 50, 'High', 'Low')
vectorized_time = time.time() - start

print(f"\n반복문 시간: {loop_time:.4f}초")
print(f"벡터화 시간: {vectorized_time:.4f}초")
print(f"속도 향상: {loop_time / vectorized_time:.1f}배")


print("\n" + "=" * 60)
print("인덱스 조작 및 데이터 필터링 실습 완료!")
print("=" * 60)

print("\n주요 학습 내용:")
print("  1. 인덱스 설정 및 재설정")
print("  2. loc (레이블), iloc (위치) 인덱싱")
print("  3. Boolean 인덱싱과 query()")
print("  4. 조건부 값 변경 (loc, np.where)")
print("  5. cut(), qcut()로 구간 나누기")
print("  6. 샘플링 및 중복 처리")
print("  7. 날짜 인덱스 활용")
print("  8. MultiIndex 다루기")
print("  9. 벡터화 연산의 중요성")
