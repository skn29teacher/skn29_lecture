# 폼 이벤트와 입력 유효성 검사

## 1. 학습 목표
* 폼 제출 시 웹 브라우저가 화면을 강제로 새로고침해 버리는 기본 빌트인 동작의 원리를 파악하고, 이를 방지하기 위한 `event.preventDefault()`의 용도를 이해합니다.
* 사용자가 자판을 입력하는 즉시 감지하여 실시간 유효성 피드백을 제공하는 `input` 이벤트 제어 기법을 습득합니다.
* 값이 비어있거나 특정 DOM 객체가 존재하지 않을 때 스크립트 실행 오류로 뻗어 버리는 버그를 예방하기 위한 **옵셔널 체이닝(`?.`)** 및 **널 병합 연산자(`??`)** 활용을 마스터합니다.

---

## 2. preventDefault() 와 submit 제어
HTML의 `<form>` 태그는 내부의 전송 버튼을 누르면 action 경로로 HTTP 패킷을 쏘고 화면 전체를 강제 새로고침하는 고유의 기본 동작을 내장하고 있습니다.

하지만 현대 싱글 페이지 애플리케이션(SPA)이나 모던 동적 웹 개발에서는 화면 깜빡임 없이 비동기 통신(Fetch API 등)으로 백엔드 데이터를 수신하므로, 이 구식 브라우저 화면 새로고침 동작을 묶어두어야만 합니다.

```javascript
const handleFormSubmit = (event) => {
  // 브라우저의 양식 전송 + 새로고침 기본 동작을 정지시킵니다.
  event.preventDefault();
  
  // 이후 안전하게 자바스크립트 유효성 검사와 비동기 전송 처리 진행
  console.log("새로고침 없이 안전하게 폼 제출 데이터를 수집했습니다.");
};

form.addEventListener("submit", handleFormSubmit);
```

---

## 3. 실시간 유효성 검사: `input` 이벤트
* **`change` 이벤트**: 포커스가 입력창 밖으로 완전히 빠져나가거나 엔터를 쳐서 입력이 '완료'된 시점에만 딱 한 번 실행됩니다.
* **`input` 이벤트**: 사용자가 키보드를 1글자 칠 때마다 즉각적으로 반응하여 실행됩니다. 비밀번호 보안 강도 실시간 바, 이메일 형식 적합성 검사 시 뛰어난 즉시 피드백 효과를 제공합니다.

---

## 4. 안전한 변수 처리: 옵셔널 체이닝(?.) & 널 병합(??)
2026년 기준 실무 스크립팅에서 **"절대 빼놓을 수 없는 예외 회피 표준 문법"**입니다.

### 1) 옵셔널 체이닝 (`?.`)
* **정의**: 참조한 대상이 `null` 또는 `undefined`이면 에러를 뿜지 않고 즉시 스크립트 실행을 우회하며 `undefined` 값을 안전하게 반환합니다.
* **용도**: 입력 폼에 특정 필드가 누락되었거나 동적 DOM이 임시 소멸하여 찾을 수 없는 상태에서 하위 `.value`나 속성을 건드렸을 때 스크립트 전체가 에러로 터지는 버그를 원천 봉쇄합니다.
* **비교**:
  ```javascript
  // 과거 구식
  const value = (emailInput !== null && emailInput !== undefined) ? emailInput.value : undefined;
  // 모던 사양
  const value = emailInput?.value;
  ```

### 2) 널 병합 연산자 (`??`)
* **정의**: 좌측 피연산자의 값이 오직 `null` 또는 `undefined`일 때만 우측의 대체 기본값을 반환합니다. (기존 단축 평가 `||`가 `0` 이나 빈 문자열 `""`까지 거짓으로 취급해 기본값으로 덮어써 버리던 논리 왜곡 문제를 완벽하게 수정)
* **결합**: 옵셔널 체이닝과 결합하여 안전한 대체 기본값 처리에 활용합니다.
  ```javascript
  // emailInput이 없거나 value가 null이면 빈 문자열("")을 안전하게 보장
  const email = emailInput?.value ?? "";
  ```

---

## 5. 실습 미션 적용 (이론 적용 코드)
회원가입 Form에 대해 양식 전송 시의 강제 새로고침을 차단하고, `input` 이벤트를 통해 실시간으로 검증하며, 유효성 검사 통과 시 입력받은 정보를 URL 파라미터로 붙여 가입 완료 페이지(`welcome_07.html`)로 안전하게 전달합니다. 가입 완료 페이지의 스크립트(`welcome_07.js`)는 `URLSearchParams` API를 사용하여 쿼리 스트링을 파싱하고, 수집된 데이터를 화면에 출력할 때 옵셔널 체이닝(`?.`) 및 널 병합(`??`)을 적용하여 예외 방어를 구현합니다.

* **적용 파일**: `day02_javascript/07_form_validation/main_07.js` & `welcome_07.js`
* **적용 대상**: 회원가입 완료 리다이렉션 및 가입자 정보 파싱 화면 출력
```javascript
// 1. main_07.js: 유효성 검사 성공 시 리다이렉션 전송
if (isFormValid) {
  // 안전하게 한글 및 특수문자를 인코딩하여 파라미터 조립
  const redirectUrl = `welcome_07.html?name=${encodeURIComponent(nameVal)}&email=${encodeURIComponent(emailVal)}&subject=${encodeURIComponent(subjectVal)}`;
  
  // 1초 후 가입 환영 페이지로 안전하게 정보 이동 처리
  setTimeout(() => {
    window.location.href = redirectUrl;
  }, 1000);
}

// 2. welcome_07.js: 가입 완료 페이지에서의 안전 데이터 수거 및 출력
const urlParams = new URLSearchParams(window.location.search);

// 옵셔널 체이닝(?.)과 널 병합(??)의 결합을 통해, 유실되거나 null인 정보에 대해 안전하게 기본값 대입 방어
const userName = urlParams?.get("name") ?? "익명 회원";
const userEmail = urlParams?.get("email") ?? "미등록 이메일";

// DOM 바인딩 처리
document.getElementById("welcome-name").textContent = userName;
document.getElementById("welcome-email").textContent = userEmail;
```

---

## 6. 학습 정리 체크리스트
- [ ] `form` 요소에 submit 동작이 가해질 때 브라우저 화면이 리로드되는 사유와 이를 차단하는 함수가 무엇인지 아는가?
- [ ] 입력값을 타이핑하는 족족 감지하는 `input` 이벤트와 포커스를 잃어야 가동되는 `change` 이벤트의 차이를 아는가?
- [ ] 옵셔널 체이닝(`?.`)을 거치지 않고 `null` 요소의 `.value`를 참조하려 할 때 콘솔에 발생하는 치명적 에러 유형은 무엇인가?
- [ ] 널 병합 연산자(`??`)가 기존의 `||` 논리 연산자 결합 구조보다 실무 폼 데이터 빈 문자열 감지 처리에서 탁월한 이유를 설명할 수 있는가?
