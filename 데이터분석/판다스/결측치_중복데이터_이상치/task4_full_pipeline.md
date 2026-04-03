# 📘 Task 4 — 통합 파이프라인 (Full Pipeline)

## 1. 전처리 파이프라인(Pipeline)이란?

전처리 파이프라인은 원본 데이터(Raw Data)가 입력되었을 때, 여러 단계의 정제 작업을 거쳐 머신러닝이나 통계 분석에 즉시 사용할 수 있는 형태(Clean Data)로 변환해주는 **자동화된 흐름**을 말합니다.

## 2. 통합 전처리 순서

실무에서는 분석 목적에 따라 순서가 조금씩 달라질 수 있으나, 일반적으로 가장 권장되는 순서는 다음과 같습니다.

### 흐름: [ 누락된 데이터 복구 → 극단값 제어 → 불필요 데이터 삭제 ]

1. **결측치 대치 (Missing Values)**
   - 이상치를 탐지하기 위한 기술통계 연산 시 결측치가 오류를 낼 수 있으므로 먼저 처리합니다.
   - 단, 데이터 손실을 막기 위해 가급적 삭제(dropna)보다는 대치(fillna/interpolate)를 권장합니다.
2. **이상치 처리 (Outliers)**
   - 대치가 완료된 꽉 찬 데이터를 기반으로, 사분위수(IQR)나 분포(Z-score)를 계산하여 이상치를 제어합니다.
   - 특별한 이유가 없다면 값이 범위에 수렴하게 만드는 **Capping(클리핑)**을 사용합니다.
3. **중복 데이터 정제 (Duplicates)**
   - 마지막으로 완전히 동일한 행이나 고유ID가 같은 행이 있다면 삭제합니다(drop_duplicates).

---

## 3. 통합 파이프라인 실습 코드

해당 내용은 `scripts/task4_full_pipeline.py`에 작성되어 있으며, 아래의 흐름대로 동작합니다.

```python
def run_preprocessing_pipeline(file_path):
    df = pd.read_csv(file_path)

    # 1. 결측치(NaN) 처리
    df['age'] = df['age'].fillna(df['age'].median())
    df['salary'] = df['salary'].fillna(df['salary'].median())
    df['score'] = df['score'].interpolate(method='linear').bfill().ffill()

    # 2. 이상치(Outlier) 처리 (Capping)
    numeric_cols = ['age', 'salary', 'score']
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        df[col] = df[col].clip(lower=lower, upper=upper)

    # 3. 중복 데이터(Duplicates) 정제
    df = df.drop_duplicates(keep='first')

    return df
```

### 실행 결과 요약

- **입력**: `messy_data.csv` (112행, 24개 NaN, 극단값들, 12개 중복행 존재)
- **출력**: `final_clean_data.csv` (100행, NaN 없음, 깨끗하게 처리된 값들 보유)

---

## 4. 실무 팁 (파이프라인 구축 시)

- 머신러닝 라이브러리인 **Scikit-Learn의 `Pipeline`이나 `ColumnTransformer`**를 사용하면 이 과정을 훨씬 객체지향적이고 깔끔하게 모델의 일부분으로 묶을 수 있습니다.
- 특정 정제 룰은 시간이 지남에 따라 변할 수 있으므로, 하드코딩된 규칙(예: `df['age'] > 100`)보다 IQR같은 **상대적 통계 수치를 규칙으로 삼는 것**이 좋습니다.
