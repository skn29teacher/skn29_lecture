# 📘 Task 1 — 결측치(NaN) 탐지 및 대치

## 1. 결측치란?

**결측치(Missing Value, NaN)** 는 데이터가 수집·저장되는 과정에서 값이 누락된 것을 말합니다.

| 발생 원인 | 예시 |
|-----------|------|
| 입력 누락 | 설문 응답 미기재, 센서 고장 |
| 시스템 오류 | DB 장애로 일부 레코드 유실 |
| 데이터 병합 | JOIN 시 매칭되지 않는 행 |
| 의도적 비공개 | 급여·나이 등 민감 정보 |

> **왜 중요한가?**  
> 결측치를 그대로 두면 통계량(평균, 분산)이 왜곡되고, 머신러닝 모델이 학습 자체를 거부하는 경우가 많습니다.

---

## 2. 결측치 탐지 방법

### 2.1 `isnull()` / `notnull()`

```python
import pandas as pd

# 전체 DataFrame의 결측치 여부 확인 (True/False 행렬)
df.isnull()

# 컬럼별 결측치 개수
df.isnull().sum()

# 컬럼별 결측치 비율(%)
(df.isnull().mean() * 100).round(2)

# 결측치가 하나라도 있는 행 필터링
df[df.isnull().any(axis=1)]
```

### 2.2 `info()` 로 한눈에 파악

```python
df.info()
# Non-Null Count 컬럼에서 결측치 유무를 즉시 파악 가능
```

---

## 3. 결측치 처리 전략

### 전략 선택 가이드

```
결측치 비율 확인
  ├─ 5% 미만 → 삭제(dropna) 가능
  ├─ 5~30%  → 대치(fillna / interpolate) 권장
  └─ 30% 초과 → 컬럼 자체 제거 또는 도메인 전문가 상담
```

---

### 3.1 삭제 — `dropna()`

데이터가 충분히 크고 결측치 비율이 낮을 때 사용합니다.

```python
# 결측치가 하나라도 있는 행 삭제
df.dropna(how='any')

# 모든 값이 NaN인 행만 삭제
df.dropna(how='all')

# 특정 컬럼 기준 삭제
df.dropna(subset=['age', 'salary'])

# 최소 N개의 유효값이 있어야 보존
df.dropna(thresh=5)
```

| 매개변수 | 설명 |
|----------|------|
| `how='any'` | 하나라도 NaN이면 삭제 |
| `how='all'` | 모든 값이 NaN이어야 삭제 |
| `subset` | 지정된 컬럼에서만 NaN 검사 |
| `thresh` | 유효값이 N개 미만인 행 삭제 |

> **주의**: `dropna(how='any')` 는 NaN이 하나만 있어도 전체 행을 삭제하므로, 데이터 손실이 클 수 있습니다.

---

### 3.2 대치 — `fillna()`

결측치를 특정 값으로 채워 넣는 방법입니다.

```python
# 고정값 대치
df['score'].fillna(0)

# 평균값 대치 — 수치형에 적합
df['age'].fillna(df['age'].mean())

# 중앙값 대치 — 이상치에 강건
df['salary'].fillna(df['salary'].median())

# 최빈값 대치 — 범주형에 적합
df['department'].fillna(df['department'].mode()[0])

# 앞의 값으로 채우기 (Forward Fill) — 시계열에 유용
df['score'].ffill()

# 뒤의 값으로 채우기 (Backward Fill)
df['score'].bfill()
```

| 전략 | 적합한 경우 |
|------|------------|
| 평균(mean) | 정규분포에 가까운 수치 데이터 |
| 중앙값(median) | 이상치가 존재하는 수치 데이터 |
| 최빈값(mode) | 범주형(카테고리) 데이터 |
| ffill / bfill | 시계열 데이터, 순서가 의미 있는 경우 |

---

### 3.3 보간법 — `interpolate()`

결측치 주변의 값을 이용하여 **수학적으로 추정**합니다.

```python
# 선형 보간 — 기본
df['score'].interpolate(method='linear')

# 다항식 보간
df['salary'].interpolate(method='polynomial', order=2)

# 시간 기반 보간 (DatetimeIndex 필요)
df['value'].interpolate(method='time')
```

> **선형 보간 vs 다항식 보간**  
> - **선형**: 빠르고 간단, 값의 변화가 완만할 때 적합  
> - **다항식**: 곡선 패턴의 데이터에 적합하나, 고차일수록 오버피팅 위험

---

## 4. 실습 코드 안내

`scripts/task1_missing_values.py` 에서 위 기법들을 순서대로 적용하며, 각 단계마다 **전·후 비교**(shape, NaN 수, info)를 출력합니다.

### 실행 방법

```bash
# base_stream 가상환경에서 실행
python scripts/task1_missing_values.py
```

### 실행 결과 요약

| 단계 | 처리 방법 | 전처리 전 NaN | 전처리 후 NaN |
|------|----------|:------------:|:------------:|
| STEP 2 | dropna(how='any') | 24 | 0 (22행 삭제) |
| STEP 3 | fillna(mean/median) | 24 | 0 (행 유지) |
| STEP 4 | interpolate(linear) | 24 | 0 (행 유지) |
| **STEP 5** | **종합 적용** | **24** | **0** |

---

## 5. 실무 팁

1. **탐색적 분석(EDA) 단계에서 결측치 비율부터 확인**하세요. `df.isnull().mean()` 한 줄이면 됩니다.
2. **삭제보다 대치를 선호**하세요. 데이터가 줄어들면 모델 성능에 직접 영향을 줍니다.
3. **중앙값 대치가 평균 대치보다 안전**합니다. 평균은 이상치에 민감하기 때문입니다.
4. **시계열 데이터라면 `interpolate()`가 가장 자연스러운 선택**입니다.
5. 결측치 처리 전에 **결측의 패턴 (MCAR / MAR / MNAR)** 을 파악하면 더 정교한 전략을 세울 수 있습니다.