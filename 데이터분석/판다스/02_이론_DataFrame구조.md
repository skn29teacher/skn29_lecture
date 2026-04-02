# 세션 2: DataFrame 구조 이해 (2시간)

## 1. DataFrame 개념

### 1.1 DataFrame이란?
- 2차원 레이블이 있는 데이터 구조
- 행(Row)과 열(Column)로 구성된 표 형태
- 각 열은 서로 다른 데이터 타입 가능
- Series의 집합으로 볼 수 있음

### 1.2 DataFrame의 구조
```
         열1    열2    열3
인덱스0   값1    값2    값3
인덱스1   값4    값5    값6
인덱스2   값7    값8    값9
```

### 1.3 DataFrame vs Series
- **Series**: 1차원 (단일 컬럼)
- **DataFrame**: 2차원 (여러 컬럼)
- DataFrame의 각 컬럼은 Series 객체

---

## 2. DataFrame 구성 요소

### 2.1 인덱스(Index)
- 행을 식별하는 레이블
- 기본값: 0부터 시작하는 정수
- 사용자 정의 가능

### 2.2 컬럼(Columns)
- 열을 식별하는 레이블
- 각 컬럼은 하나의 Series
- 컬럼명은 문자열이 일반적

### 2.3 값(Values)
- 실제 데이터가 저장되는 부분
- 2차원 NumPy 배열로 저장
- 각 컬럼은 다른 타입 가능

---

## 3. DataFrame 생성 방법

### 3.1 딕셔너리로 생성
```python
# 가장 일반적인 방법
data = {
    'name': ['Kim', 'Lee', 'Park'],
    'age': [25, 30, 35],
    'city': ['Seoul', 'Busan', 'Incheon']
}
df = pd.DataFrame(data)
```

### 3.2 리스트의 딕셔너리로 생성
```python
data = [
    {'name': 'Kim', 'age': 25, 'city': 'Seoul'},
    {'name': 'Lee', 'age': 30, 'city': 'Busan'},
    {'name': 'Park', 'age': 35, 'city': 'Incheon'}
]
df = pd.DataFrame(data)
```

### 3.3 2차원 리스트로 생성
```python
data = [
    ['Kim', 25, 'Seoul'],
    ['Lee', 30, 'Busan'],
    ['Park', 35, 'Incheon']
]
df = pd.DataFrame(data, columns=['name', 'age', 'city'])
```

### 3.4 Series로 생성
```python
s1 = pd.Series(['Kim', 'Lee', 'Park'], name='name')
s2 = pd.Series([25, 30, 35], name='age')
df = pd.DataFrame({'name': s1, 'age': s2})
```

### 3.5 NumPy 배열로 생성
```python
import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
df = pd.DataFrame(arr, columns=['A', 'B', 'C'])
```

---

## 4. DataFrame 기본 속성

### 4.1 구조 확인
```python
df.shape        # (행 수, 열 수)
df.size         # 전체 요소 개수
df.ndim         # 차원 (항상 2)
df.index        # 인덱스 객체
df.columns      # 컬럼 객체
df.values       # NumPy 배열
df.dtypes       # 각 컬럼의 데이터 타입
```

### 4.2 데이터 미리보기
```python
df.head()       # 처음 5개 행
df.head(10)     # 처음 10개 행
df.tail()       # 마지막 5개 행
df.tail(3)      # 마지막 3개 행
```

### 4.3 정보 확인
```python
df.info()       # 전체 정보 (타입, 결측치 등)
df.describe()   # 기술통계 (수치형 컬럼만)
```

---

## 5. 컬럼(열) 접근 및 조작

### 5.1 단일 컬럼 선택
```python
# 두 가지 방법 (결과는 Series)
df['name']      # 딕셔너리 방식 (권장)
df.name         # 속성 방식 (컬럼명이 문자열이고 공백 없을 때)
```

### 5.2 여러 컬럼 선택
```python
# 결과는 DataFrame
df[['name', 'age']]
```

### 5.3 컬럼 추가
```python
# 새로운 컬럼 생성
df['salary'] = [3000, 4000, 5000]

# 기존 컬럼으로부터 계산
df['age_10years_later'] = df['age'] + 10
```

### 5.4 컬럼 삭제
```python
# 방법 1: drop 메서드
df.drop('salary', axis=1)           # 원본 유지
df.drop('salary', axis=1, inplace=True)  # 원본 수정

# 방법 2: del 키워드
del df['salary']
```

### 5.5 컬럼 이름 변경
```python
# 특정 컬럼만 변경
df.rename(columns={'name': '이름', 'age': '나이'})

# 모든 컬럼 변경
df.columns = ['이름', '나이', '도시']
```

---

## 6. 행(Row) 접근 및 조작

### 6.1 위치 기반 인덱싱: iloc
```python
df.iloc[0]          # 첫 번째 행 (Series)
df.iloc[0:2]        # 처음 2개 행 (DataFrame)
df.iloc[0, 1]       # 0행 1열 값
df.iloc[0:2, 0:2]   # 0-1행, 0-1열
```

### 6.2 레이블 기반 인덱싱: loc
```python
df.loc[0]           # 인덱스 0인 행
df.loc[0:2]         # 인덱스 0~2 (끝 포함!)
df.loc[0, 'name']   # 0행의 name 컬럼
df.loc[0:2, ['name', 'age']]  # 특정 행과 컬럼
```

### 6.3 행 추가
```python
# 새로운 행 추가
new_row = pd.Series({'name': 'Choi', 'age': 40, 'city': 'Daegu'})
df = df.append(new_row, ignore_index=True)

# 또는 concat 사용
df = pd.concat([df, new_row.to_frame().T], ignore_index=True)
```

### 6.4 행 삭제
```python
df.drop(0)                    # 인덱스 0 삭제
df.drop([0, 1])               # 여러 행 삭제
df.drop(0, inplace=True)      # 원본 수정
```

---

## 7. Boolean 인덱싱

### 7.1 단일 조건
```python
# 나이가 30 이상인 행
df[df['age'] >= 30]

# 서울에 사는 사람
df[df['city'] == 'Seoul']
```

### 7.2 복합 조건
```python
# AND 조건 (&)
df[(df['age'] >= 25) & (df['age'] <= 35)]

# OR 조건 (|)
df[(df['city'] == 'Seoul') | (df['city'] == 'Busan')]

# NOT 조건 (~)
df[~(df['age'] < 30)]
```

### 7.3 isin() 메서드
```python
# 여러 값 중 하나라도 해당
df[df['city'].isin(['Seoul', 'Busan'])]
```

---

## 8. DataFrame 정렬

### 8.1 값 기준 정렬
```python
# 단일 컬럼 정렬
df.sort_values('age')                    # 오름차순
df.sort_values('age', ascending=False)   # 내림차순

# 여러 컬럼 정렬
df.sort_values(['city', 'age'])
df.sort_values(['city', 'age'], ascending=[True, False])
```

### 8.2 인덱스 기준 정렬
```python
df.sort_index()
```

---

## 9. DataFrame 통계 함수

### 9.1 기본 통계
```python
df.mean()       # 각 컬럼의 평균
df.sum()        # 각 컬럼의 합
df.max()        # 각 컬럼의 최댓값
df.min()        # 각 컬럼의 최솟값
df.std()        # 각 컬럼의 표준편차
```

### 9.2 특정 컬럼 통계
```python
df['age'].mean()
df['age'].sum()
```

### 9.3 describe()
```python
# 수치형 컬럼의 기술통계
df.describe()

# 모든 컬럼 포함 (문자열 등)
df.describe(include='all')
```

---

## 10. 결측치 처리

### 10.1 결측치 확인
```python
df.isnull()         # 결측치면 True
df.isnull().sum()   # 각 컬럼의 결측치 개수
df.notnull()        # 결측치가 아니면 True
```

### 10.2 결측치 처리
```python
# 결측치가 있는 행 제거
df.dropna()

# 결측치가 있는 열 제거
df.dropna(axis=1)

# 모든 값이 결측치인 행만 제거
df.dropna(how='all')

# 특정 컬럼에 결측치가 있는 행 제거
df.dropna(subset=['age'])

# 결측치 채우기
df.fillna(0)                    # 0으로 채우기
df.fillna(df.mean())            # 평균으로 채우기
df.fillna(method='ffill')       # 앞의 값으로 채우기
df.fillna(method='bfill')       # 뒤의 값으로 채우기
```

---

## 11. 데이터 타입 변환

### 11.1 타입 확인
```python
df.dtypes
df['age'].dtype
```

### 11.2 타입 변환
```python
# 단일 컬럼
df['age'] = df['age'].astype('float')

# 여러 컬럼
df = df.astype({'age': 'int', 'salary': 'float'})

# 문자열로 변환
df['age'] = df['age'].astype('str')
```

---

## 12. 실습 예제

### 예제 1: 학생 성적 데이터
- 여러 과목의 성적을 DataFrame으로 생성
- 총점, 평균 계산
- 특정 기준 이상 학생 필터링

### 예제 2: 직원 정보 관리
- 이름, 나이, 부서, 급여 정보를 DataFrame으로 생성
- 부서별 평균 급여 계산
- 조건에 맞는 직원 검색

### 예제 3: 매출 데이터 분석
- 제품별, 월별 매출 데이터 생성
- 결측치 처리
- 정렬 및 통계 분석

---

## 13. 주요 개념 정리

1. **DataFrame은 행과 열로 구성된 2차원 데이터 구조**
2. **각 컬럼은 Series 객체이며 다른 타입 가능**
3. **loc (레이블), iloc (위치) 로 행/열 접근**
4. **Boolean 인덱싱으로 조건부 필터링**
5. **결측치를 효과적으로 처리하는 다양한 메서드 제공**

---

## 14. 연습 문제

1. 5명의 학생에 대한 3과목 성적 DataFrame 만들고 분석하기
2. 제품 정보 DataFrame에서 특정 가격 범위 필터링하기
3. 결측치가 있는 직원 데이터를 적절히 처리하기
4. 여러 조건을 조합하여 복잡한 필터링 수행하기
