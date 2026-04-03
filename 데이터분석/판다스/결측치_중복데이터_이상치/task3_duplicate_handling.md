# 📘 Task 3 — 중복 데이터 탐지 및 정제

## 1. 중복 데이터란?

**중복 데이터(Duplicate Data)** 는 데이터 내에 완전히 동일하거나, 논리적으로 동일한 정보(행)가 중복해서 존재하는 경우를 의미합니다.

| 종류 | 설명 | 예시 |
|------|------|------|
| 완전 중복 | 모든 컬럼의 값이 완벽히 일치 | 시스템 상 데이터 이중 적재 |
| 부분 중복 | 특정 키값(예: ID)만 일치하고 일부 값이 다름 | 한 사용자가 두 번 가입/수정 시도 시 발생 |

>  **왜 중요한가?**  
> 데이터가 부풀려져 통계(Sum, Count 등) 오류를 발생시키고, 머신러닝의 경우 학습 시 가중치를 불필요하게 왜곡합니다. 또한 데이터베이스 크기를 커지게 하여 성능 저하를 일으킵니다.

---

## 2. 중복 데이터 탐지

### 2.1 `duplicated()`

`duplicated()` 함수는 행의 중복 여부를 `True` / `False`로 반환합니다. 기본적으로 첫 번째로 나타난 값은 `False`로, 이후 중복된 값은 `True`로 표시합니다.

```python
import pandas as pd

# 전체 컬럼을 기준으로 중복 여부 확인
df.duplicated()

# 전체 중복 행의 개수 확인
df.duplicated().sum()

# 중복된 행들의 실제 데이터 확인
# keep=False 를 주면 원본 데이터와 중복 데이터를 모두 표시합니다.
df[df.duplicated(keep=False)]
```

### 2.2 특정 컬럼(Subset) 기준 시

```python
# 'id' 컬럼만 같아도 중복으로 간주할 때
df.duplicated(subset=['id']).sum()

# 여러 컬럼('name', 'department')의 조합으로 중복 여부 확인
df.duplicated(subset=['name', 'department']).sum()
```

---

## 3. 중복 데이터 정제

### 3.1 `drop_duplicates()`

결측치나 이상치가 아닌 중복 데이터는 보통 삭제 처리합니다. 

```python
# 1. 첫 번째 항목을 유지하고 나머지 중복 삭제 (기본값)
df.drop_duplicates(keep='first')

# 2. 마지막 항목을 유지하고 이전 중복 삭제
df.drop_duplicates(keep='last')

# 3. 중복이 존재하는 행 전체 삭제 (고유한 값만 남김)
df.drop_duplicates(keep=False)

# 4. 특정 컬럼 기준 삭제
df.drop_duplicates(subset=['id'], keep='last')
```

| `keep` 속성 | 설명 |
|------------|------|
| `first` | 첫 번째로 나타나는 값은 보존 (디폴트) |
| `last` | 마지막으로 나타나는 값을 보존 (최신 데이터 갱신 시 유용) |
| `False` | 중복된 모든 데이터 삭제 |

---

## 4. 실습 코드 안내

`scripts/task3_duplicate_handling.py` 에서 중복 데이터를 처리하는 기법들을 실습합니다.

### 실행 방법

```bash
# base_stream 가상환경에서 실행
python scripts/task3_duplicate_handling.py
```

### 실행 결과 요약

| 단계 | 처리 방법 | Shape 변화 | 설명 |
|------|----------|:------------:|:---|
| **STEP 1** | `duplicated().sum()` | - | 원본 112행 중 **12개 행이 완전 중복**됨을 확인 |
| **STEP 3-1**| `drop_duplicates(keep='first')` | `(112, 6)` → `(100, 6)` | 12개 삭제 완료 |
| **STEP 3-2**| `drop_duplicates(keep='last')` | `(112, 6)` → `(100, 6)` | 12개 삭제 완료 |
| **STEP 3-3**| `drop_duplicates(keep=False)` | `(112, 6)` → `(88, 6)` | 원본 정보까지 모두 삭제되어 총 24행 삭제됨 |
| **STEP 4** | 최종 저장 | `(100, 6)` | `task3_deduped.csv` 생성 완료 |

---

## 5. 실무 팁

1. **로그 기반의 데이터** 에서 부분 중복이 발생한 경우, 보통 `시간(Timestamp)` 컬럼이 존재합니다. 이런 경우 데이터를 `sort_values`로 시간순으로 정렬한 뒤, 식별자 컬럼 기준으로 `drop_duplicates(keep='last')`를 적용하면 가장 최신 데이터만 깔끔하게 남길 수 있습니다.
2. 중복을 삭제하기 전에는 `df[df.duplicated(keep=False)]`를 사용하여 어떤 데이터가 중복되어 있는지 **눈으로 꼭 확인** 하는 습관을 들이세요.
3. 데이터 취합(Merge, Concat) 후에는 중복 발생 가능성이 높아지므로, 병합 후에는 항상 `duplicated` 연산을 수행하세요.
