"""
Pandas DataFrame 기초 실습
세션 2: DataFrame 구조 이해 및 기본 조작

학습 목표:
1. DataFrame 생성 방법 이해
2. 행과 열 접근 및 조작
3. Boolean 인덱싱 활용
4. 통계 함수 및 정렬
5. 결측치 처리
"""

import pandas as pd
import numpy as np

print("=" * 60)
print("1. DataFrame 생성 - 딕셔너리로 생성")
print("=" * 60)

# 1.1 기본 생성
data = {
    'name': ['김철수', '이영희', '박민수', '정수진', '최영수'],
    'age': [25, 30, 35, 28, 32],
    'city': ['서울', '부산', '인천', '대구', '대전'],
    'salary': [3000, 4000, 3500, 3800, 4200]
}
df = pd.DataFrame(data)

print("\\n직원 정보:")
print(df)

print(f"\\n데이터 형태: {df.shape}")  # (행, 열)
print(f"전체 요소 개수: {df.size}")
print(f"차원: {df.ndim}")

print("\\n각 컬럼의 데이터 타입:")
print(df.dtypes)


print("\\n" + "=" * 60)
print("2. DataFrame 생성 - 다양한 방법")
print("=" * 60)

# 2.1 리스트의 딕셔너리로 생성
data_list = [
    {'name': '김철수', 'score': 85, 'grade': 'B'},
    {'name': '이영희', 'score': 92, 'grade': 'A'},
    {'name': '박민수', 'score': 78, 'grade': 'C'}
]
df_students = pd.DataFrame(data_list)
print("\\n학생 성적 (리스트의 딕셔너리):")
print(df_students)

# 2.2 2차원 리스트로 생성
data_2d = [
    ['Apple', 1000, 50],
    ['Banana', 500, 100],
    ['Orange', 800, 75]
]
df_products = pd.DataFrame(data_2d, columns=['product', 'price', 'stock'])
print("\\n제품 정보 (2차원 리스트):")
print(df_products)

# 2.3 NumPy 배열로 생성
arr = np.random.randint(50, 100, size=(5, 3))
df_scores = pd.DataFrame(arr, columns=['국어', '영어', '수학'])
df_scores.index = ['학생1', '학생2', '학생3', '학생4', '학생5']
print("\\n과목별 점수 (NumPy 배열):")
print(df_scores)


print("\\n" + "=" * 60)
print("3. DataFrame 구조 확인")
print("=" * 60)

print("\\n처음 3개 행 (head):")
print(df.head(3))

print("\\n마지막 2개 행 (tail):")
print(df.tail(2))

print("\\n인덱스:")
print(df.index)

print("\\n컬럼명:")
print(df.columns)

print("\\n값 (NumPy 배열):")
print(df.values)


print("\\n" + "=" * 60)
print("4. DataFrame 정보 확인")
print("=" * 60)

print("\\ninfo() - 전체 정보:")
print(df.info())

print("\\ndescribe() - 기술통계:")
print(df.describe())


print("\\n" + "=" * 60)
print("5. 컬럼(열) 접근")
print("=" * 60)

# 5.1 단일 컬럼 선택 (결과는 Series)
print("\\n이름 컬럼:")
print(df['name'])
print(f"타입: {type(df['name'])}")

# 5.2 여러 컬럼 선택 (결과는 DataFrame)
print("\\n이름과 나이 컬럼:")
print(df[['name', 'age']])
print(f"타입: {type(df[['name', 'age']])}")

# 5.3 속성 방식 접근
print(f"\\n평균 나이: {df.age.mean():.2f}")


print("\\n" + "=" * 60)
print("6. 컬럼 추가 및 수정")
print("=" * 60)

# 6.1 새로운 컬럼 추가
df['bonus'] = df['salary'] * 0.1
print("\\n보너스 컬럼 추가:")
print(df)

# 6.2 기존 컬럼으로 계산
df['total_income'] = df['salary'] + df['bonus']
print("\\n총 수입 컬럼 추가:")
print(df[['name', 'salary', 'bonus', 'total_income']])

# 6.3 조건부 컬럼 추가
df['is_senior'] = df['age'] >= 30
print("\\n30세 이상 여부:")
print(df[['name', 'age', 'is_senior']])


print("\\n" + "=" * 60)
print("7. 컬럼 삭제 및 이름 변경")
print("=" * 60)

# 7.1 컬럼 삭제 (원본은 유지)
df_dropped = df.drop('is_senior', axis=1)
print("\\nis_senior 컬럼 삭제 후:")
print(df_dropped.columns.tolist())

# 7.2 컬럼 이름 변경
df_renamed = df.rename(columns={'name': '이름', 'age': '나이'})
print("\\n컬럼 이름 변경:")
print(df_renamed.head())


print("\\n" + "=" * 60)
print("8. 행(Row) 접근 - iloc (위치 기반)")
print("=" * 60)

print("\\n첫 번째 행 (iloc[0]):")
print(df.iloc[0])

print("\\n처음 3개 행 (iloc[0:3]):")
print(df.iloc[0:3])

print("\\n0행 1열의 값 (iloc[0, 1]):")
print(df.iloc[0, 1])

print("\\n처음 2개 행, 처음 2개 열 (iloc[0:2, 0:2]):")
print(df.iloc[0:2, 0:2])

print("\\n모든 행, 1-2열 (iloc[:, 1:3]):")
print(df.iloc[:, 1:3])


print("\\n" + "=" * 60)
print("9. 행(Row) 접근 - loc (레이블 기반)")
print("=" * 60)

print("\\n인덱스 0인 행 (loc[0]):")
print(df.loc[0])

print("\\n인덱스 0~2 행 (loc[0:2]):")  # 끝 포함!
print(df.loc[0:2])

print("\\n0행의 name 값 (loc[0, 'name']):")
print(df.loc[0, 'name'])

print("\\n0-2행의 name, age 컬럼 (loc[0:2, ['name', 'age']]):")
print(df.loc[0:2, ['name', 'age']])


print("\\n" + "=" * 60)
print("10. Boolean 인덱싱 (조건 필터링)")
print("=" * 60)

# 10.1 단일 조건
print("\\n나이가 30 이상인 직원:")
senior_employees = df[df['age'] >= 30]
print(senior_employees[['name', 'age']])

print("\\n서울에 사는 직원:")
seoul_employees = df[df['city'] == '서울']
print(seoul_employees[['name', 'city']])

# 10.2 복합 조건 (AND: &)
print("\\n나이 30 이상이고 급여 4000 이상:")
filtered = df[(df['age'] >= 30) & (df['salary'] >= 4000)]
print(filtered[['name', 'age', 'salary']])

# 10.3 복합 조건 (OR: |)
print("\\n서울 또는 부산에 사는 직원:")
filtered = df[(df['city'] == '서울') | (df['city'] == '부산')]
print(filtered[['name', 'city']])

# 10.4 NOT 조건 (~)
print("\\n30세 미만이 아닌 직원 (30세 이상):")
filtered = df[~(df['age'] < 30)]
print(filtered[['name', 'age']])

# 10.5 isin() 메서드
print("\\n서울, 부산, 인천에 사는 직원:")
filtered = df[df['city'].isin(['서울', '부산', '인천'])]
print(filtered[['name', 'city']])


print("\\n" + "=" * 60)
print("11. DataFrame 정렬")
print("=" * 60)

# 11.1 단일 컬럼 정렬
print("\\n나이 순 정렬 (오름차순):")
print(df.sort_values('age')[['name', 'age']])

print("\\n급여 순 정렬 (내림차순):")
print(df.sort_values('salary', ascending=False)[['name', 'salary']])

# 11.2 여러 컬럼 정렬
print("\\n도시 순, 나이 순 정렬:")
print(df.sort_values(['city', 'age'])[['name', 'city', 'age']])

# 11.3 인덱스 정렬
df_shuffled = df.sample(frac=1)  # 무작위 섞기
print("\\n인덱스 순 정렬:")
print(df_shuffled.sort_index())


print("\\n" + "=" * 60)
print("12. DataFrame 통계 함수")
print("=" * 60)

print("\\n각 컬럼의 평균:")
print(df[['age', 'salary']].mean())

print("\\n각 컬럼의 합계:")
print(df[['age', 'salary']].sum())

print("\\n각 컬럼의 최댓값:")
print(df[['age', 'salary']].max())

print("\\n급여 통계:")
print(f"평균: {df['salary'].mean():.2f}")
print(f"중앙값: {df['salary'].median():.2f}")
print(f"표준편차: {df['salary'].std():.2f}")
print(f"최댓값: {df['salary'].max()}")
print(f"최솟값: {df['salary'].min()}")


print("\\n" + "=" * 60)
print("13. 결측치 처리")
print("=" * 60)

# 13.1 결측치가 있는 DataFrame 생성
data_with_nan = {
    'name': ['A', 'B', 'C', 'D', 'E'],
    'age': [25, np.nan, 35, 28, np.nan],
    'salary': [3000, 4000, np.nan, 3800, 4200],
    'city': ['서울', '부산', '인천', np.nan, '대전']
}
df_nan = pd.DataFrame(data_with_nan)
print("\\n결측치가 있는 데이터:")
print(df_nan)

# 13.2 결측치 확인
print("\\n결측치 여부:")
print(df_nan.isnull())

print("\\n각 컬럼의 결측치 개수:")
print(df_nan.isnull().sum())

# 13.3 결측치가 있는 행 제거
print("\\n결측치 행 제거:")
print(df_nan.dropna())

# 13.4 특정 컬럼의 결측치만 제거
print("\\nage 컬럼의 결측치가 있는 행 제거:")
print(df_nan.dropna(subset=['age']))

# 13.5 결측치를 값으로 채우기
print("\\n결측치를 0으로 채우기:")
print(df_nan.fillna(0))

print("\\n각 컬럼의 평균으로 채우기:")
print(df_nan.fillna(df_nan.mean()))

# 13.6 특정 컬럼의 결측치만 채우기
df_nan_filled = df_nan.copy()
df_nan_filled['age'] = df_nan_filled['age'].fillna(df_nan_filled['age'].mean())
df_nan_filled['city'] = df_nan_filled['city'].fillna('미상')
print("\\n특정 컬럼만 채우기:")
print(df_nan_filled)


print("\\n" + "=" * 60)
print("14. 데이터 타입 변환")
print("=" * 60)

# 타입 변환 예제
df_convert = pd.DataFrame({
    'A': ['1', '2', '3'],
    'B': [1.1, 2.2, 3.3],
    'C': [10, 20, 30]
})

print("\\n원본 데이터 타입:")
print(df_convert.dtypes)

# 타입 변환
df_convert['A'] = df_convert['A'].astype('int')
df_convert['B'] = df_convert['B'].astype('int')
df_convert['C'] = df_convert['C'].astype('str')

print("\\n변환 후 데이터 타입:")
print(df_convert.dtypes)
print("\\n변환 후 데이터:")
print(df_convert)


print("\\n" + "=" * 60)
print("15. 실전 예제 1: 학생 성적 관리")
print("=" * 60)

# 학생 성적 데이터
students_data = {
    'name': ['김철수', '이영희', '박민수', '정수진', '최영수', '한지민'],
    '국어': [85, 92, 78, 95, 88, 90],
    '영어': [90, 88, 85, 92, 94, 87],
    '수학': [88, 95, 80, 90, 92, 85],
    '과학': [92, 89, 88, 94, 90, 93]
}
df_students = pd.DataFrame(students_data)

print("\\n학생 성적:")
print(df_students)

# 총점과 평균 계산
df_students['총점'] = df_students[['국어', '영어', '수학', '과학']].sum(axis=1)
df_students['평균'] = df_students[['국어', '영어', '수학', '과학']].mean(axis=1)

print("\\n총점과 평균 추가:")
print(df_students)

# 평균 순으로 정렬
print("\\n평균 점수 순위:")
df_sorted = df_students.sort_values('평균', ascending=False)
print(df_sorted[['name', '평균']])

# 평균 90점 이상 학생
print("\\n평균 90점 이상 학생:")
excellent_students = df_students[df_students['평균'] >= 90]
print(excellent_students[['name', '평균']])

# 과목별 평균
print("\\n과목별 평균 점수:")
subject_mean = df_students[['국어', '영어', '수학', '과학']].mean()
print(subject_mean)


print("\\n" + "=" * 60)
print("16. 실전 예제 2: 제품 재고 관리")
print("=" * 60)

# 제품 데이터
products_data = {
    'product_id': ['P001', 'P002', 'P003', 'P004', 'P005'],
    'product_name': ['노트북', '마우스', '키보드', '모니터', '헤드셋'],
    'category': ['전자', '주변기기', '주변기기', '전자', '주변기기'],
    'price': [1200000, 25000, 45000, 350000, 80000],
    'stock': [15, 50, 30, 20, 45],
    'supplier': ['A사', 'B사', 'B사', 'C사', 'A사']
}
df_products = pd.DataFrame(products_data)

print("\\n제품 정보:")
print(df_products)

# 재고 금액 계산
df_products['stock_value'] = df_products['price'] * df_products['stock']
print("\\n재고 금액 추가:")
print(df_products[['product_name', 'price', 'stock', 'stock_value']])

# 카테고리별 그룹 분석 (간단한 통계)
print("\\n전자 제품:")
electronics = df_products[df_products['category'] == '전자']
print(electronics[['product_name', 'price', 'stock']])

print("\\n주변기기:")
peripherals = df_products[df_products['category'] == '주변기기']
print(peripherals[['product_name', 'price', 'stock']])

# 재고 20개 이하 제품
print("\\n재고 20개 이하 제품 (재입고 필요):")
low_stock = df_products[df_products['stock'] <= 20]
print(low_stock[['product_name', 'stock']])

# 가격대별 제품
print("\\n100,000원 이상 제품:")
expensive = df_products[df_products['price'] >= 100000]
print(expensive[['product_name', 'price']])


print("\\n" + "=" * 60)
print("17. 실전 예제 3: 직원 급여 분석")
print("=" * 60)

# 직원 데이터
employees = {
    'id': range(1, 11),
    'name': ['김철수', '이영희', '박민수', '정수진', '최영수', 
             '한지민', '오세훈', '강민아', '윤서준', '임채원'],
    'department': ['영업', '개발', '개발', '영업', '인사',
                   '개발', '영업', '인사', '개발', '영업'],
    'position': ['사원', '대리', '과장', '대리', '부장',
                 '사원', '과장', '대리', '부장', '사원'],
    'salary': [3000, 4000, 5000, 4200, 7000,
               3500, 5500, 4300, 7500, 3200],
    'years': [1, 3, 5, 4, 10, 2, 6, 4, 12, 1]
}
df_emp = pd.DataFrame(employees)

print("\\n직원 정보:")
print(df_emp)

# 통계 분석
print(f"\\n평균 급여: {df_emp['salary'].mean():.0f}만원")
print(f"최고 급여: {df_emp['salary'].max()}만원")
print(f"최저 급여: {df_emp['salary'].min()}만원")

# 부서별 필터링
print("\\n개발팀 직원:")
dev_team = df_emp[df_emp['department'] == '개발']
print(dev_team[['name', 'position', 'salary']])

# 급여 5000만원 이상 직원
print("\\n고액 연봉자 (5000만원 이상):")
high_earners = df_emp[df_emp['salary'] >= 5000]
print(high_earners[['name', 'department', 'position', 'salary']])

# 복합 조건: 개발팀이면서 대리 이상
print("\\n개발팀의 대리 이상 직원:")
senior_devs = df_emp[
    (df_emp['department'] == '개발') & 
    (df_emp['position'].isin(['대리', '과장', '부장']))
]
print(senior_devs[['name', 'position', 'salary']])

# 급여 순 정렬
print("\\n급여 상위 5명:")
top5 = df_emp.sort_values('salary', ascending=False).head(5)
print(top5[['name', 'department', 'salary']])


print("\\n" + "=" * 60)
print("18. DataFrame 주요 메서드 정리")
print("=" * 60)

sample_df = pd.DataFrame({
    'A': [1, 2, 2, 3, 3, 3],
    'B': ['a', 'a', 'b', 'b', 'c', 'c']
})

print("\\n원본 데이터:")
print(sample_df)

print("\\nvalue_counts() - 각 값의 빈도:")
print(sample_df['A'].value_counts())

print("\\nunique() - 고유값:")
print(sample_df['A'].unique())

print(f"\\nnunique() - 고유값 개수: {sample_df['A'].nunique()}")


print("\\n" + "=" * 60)
print("DataFrame 기초 실습 완료!")
print("=" * 60)
