#  구조분해 할당 및 전개/나머지 연산자

## 1. 학습 목표
* 객체(Object)와 배열(Array)에 저장된 복잡한 요소를 단 한 줄의 선언식으로 분해하여 개별 변수에 효율적으로 바인딩하는 구조분해 할당(Destructuring Assignment)의 고급 용법을 습득합니다.
* 중첩 구조분해 할당 및 함수의 매개변수 구조분해 할당 패턴을 이해하여 코드 가독성을 극대화합니다.
* 전개 연산자(Spread Operator, `...`)의 메모리 얕은 복사(Shallow Copy) 동작으로 발생하는 데이터 동시 오염 버그를 분석하고, 이를 완전히 차단하는 깊은 복사(Deep Copy) 구현 기법을 학습합니다.
* 가변 매개변수를 수거하는 나머지 매개변수(Rest Parameter, `...rest`)를 활용해 매개변수의 유연성을 확보하고 배열 고차 함수와 연계하는 실무 기법을 파악합니다.

---

## 2. 구조분해 할당 (Destructuring Assignment) 고도화

### 1) 객체 구조분해 할당의 실무적 응용
* **기본값과 변수명 우회 변경**:
  ```javascript
  const member = { id: "user01", nick: "초보개발자" };
  // nick 속성을 새로운 변수명 userNick으로 꺼내고, 누락된 role 속성에는 기본값 'guest'를 할당합니다.
  const { nick: userNick, role = "guest" } = member;
  ```
* **중첩 객체(Nested Object) 분해**:
  객체 내부에 또 다른 객체가 존재하는 경우, 하위 깊이까지 단 한 번의 구조분해 선언으로 도달할 수 있습니다.
  ```javascript
  const client = { name: "최영희", info: { email: "young@mail.com", addr: "서울" } };
  const { info: { email } } = client; // client.info.email 값이 바로 email 변수에 바인딩됩니다.
  ```
* **함수 매개변수 구조분해**:
  함수의 인자로 객체를 넘길 때 매개변수 정의단에서 즉시 분해하여 활용하면 함수 내부의 임시 참조 과정을 대폭 줄일 수 있습니다.
  ```javascript
  const printProfile = ({ name, info: { email } }) => {
    console.log(`이름: ${name}, 이메일: ${email}`);
  };
  ```

### 2) 배열 구조분해 할당의 응용
* **변수 값 맞교환 (Swap)**: 임시 변수(`temp`)를 생성하지 않고 단 한 줄로 두 변수의 값을 서로 스왑할 수 있습니다.
  ```javascript
  let valueA = 10;
  let valueB = 20;
  [valueA, valueB] = [valueB, valueA]; // valueA는 20, valueB는 10이 됨
  ```
* **건너뛰기 및 나머지 수거**: 콤마를 통해 필요 없는 자리는 뛰어넘고, 남은 원소는 나머지 기호(`...rest`)로 배열 수거가 가능합니다.
  ```javascript
  const numbers = [1, 2, 3, 4, 5];
  const [first, , third, ...rest] = numbers; // first = 1, third = 3, rest = [4, 5]
  ```

---

## 3. 전개 연산자 (Spread Operator)와 데이터 얕은 복사 오염 실증

### 1) 얕은 복사 (Shallow Copy)의 동작과 버그
전개 연산자(`...`)로 배열이나 객체를 복사하면 1단계 깊이에 있는 원소들은 온전하게 복사되지만, 2단계 이상의 깊이에 포함된 중첩 객체나 배열은 메모리상의 주소(Reference)를 복사 사본과 공유하게 됩니다.
이로 인해 복사된 사본의 내부 중첩 속성을 수정하면 **원본 객체의 내부 속성까지 함께 변경되어 버리는 연쇄 오염 버그**가 생깁니다.

### 2) 깊은 복사 (Deep Copy)를 통한 안전 지대 확보
중첩된 구조의 데이터도 오염 없이 완전히 분리하기 위해 깊은 복사를 수행해야 합니다.
* **수동 중첩 복사**: 전개 연산자를 여러 깊이에서 재귀적으로 중첩해서 사용하는 방식입니다.
  ```javascript
  const copied = { ...original, detail: { ...original.detail } };
  ```
* **structuredClone API**: 최신 브라우저 표준 내장 API로, 복잡한 객체와 배열의 중첩 참조를 완벽하게 분리하여 완벽한 사본(Deep Copy)을 만들어 줍니다.
  ```javascript
  const deepCopied = structuredClone(original);
  ```

---

## 4. 나머지 매개변수 (Rest Parameter)

함수 시그니처의 마지막 매개변수로 작성하면, 지정된 매개변수들을 넘어서서 전달된 남은 모든 인수(Arguments)를 하나의 순수 배열로 수집합니다.
* **배열 API와 즉각 결합**: 가변 개수의 인수들이 배열 타입으로 바인딩되므로 `reduce`, `map`, `filter` 등의 고차 함수를 루프 없이 바로 얹어서 연산할 수 있습니다.
  ```javascript
  const filterEvens = (...numbers) => numbers.filter(n => n % 2 === 0);
  ```

---

## 5. 실습 미션 적용 (이론 적용 코드)
기본 쇼핑몰 상품 목록에 신규 상품을 병합하는 과정에서 얕은 복사 오염이 왜 생기는지 실증하고, `structuredClone` 및 매개변수 구조분해 할당을 적용하여 오염 없이 안전하게 대량의 카드 목록을 출력하는 환경을 빌드합니다.