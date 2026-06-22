# Async/Await: Promise를 동기식 코드처럼 쉽게

## 학습 목표
*   async/await의 탄생 배경과 문법 규칙을 브라우저 내장 Battery Status API 실무 응용을 통해 이해합니다.
*   비동기 에러를 동기식 스타일로 포착하는 try/catch/finally 제어의 편의성을 가상 카드 승인 및 네트워크 장애 관리 폼 코드로 학습합니다.
*   직렬 await로 일어나는 심각한 비동기 병목을 Promise.all과 await의 조합으로 타파하는 병렬 최적화 코드를 마스터합니다.
*   프론트엔드 핵심 실무인 OAuth2 토큰 만료 자동 갱신 및 API 재시도(Retry) 파이프라인을 async/await 코드로 리팩터링하여 가독성 혁신을 체험합니다.

---

## 1. async/await의 탄생 배경과 기본 규칙 (실무 사례: 기기 배터리 모니터링 API)

### 1) 왜 async/await가 등장했는가
*   Promise는 콜백 지옥을 해결하고 코드를 평평하게 만들었지만, 여전히 `.then()` 메서드 체인이 늘어날 때마다 가독성이 떨어지고 스코프(변수 유효범위) 관리와 예외 처리가 복잡해지는 단점을 지니고 있었습니다.
*   ES8(ECMAScript 2017)에서 도입된 async/await는 비동기 코드를 **마치 위에서 아래로 실행되는 일반적인 동기식(Synchronous) 코드의 가독성 그대로** 작성할 수 있게 해주는 문법적 설탕(Syntactic Sugar)입니다.

### 2) 핵심 문법 규칙
*   **async 키워드**: 비동기 처리를 수행할 함수 정의부 앞에 반드시 `async`를 붙여야 합니다. 이 지시어가 붙은 함수는 **항상 Promise 객체를 반환**하도록 강제됩니다.
*   **await 키워드**: `async` 함수 내부에서만 사용할 수 있습니다. Promise 앞에 `await`를 붙이면, 해당 **Promise가 완료(Settled)될 때까지 함수의 실행을 일시적으로 중단하고 대기**했다가 결과값을 정직하게 반환합니다.

### 3) 기기 배터리 모니터링 (Battery Status API)
브라우저 표준 기기 모니터링 API인 `navigator.getBattery()`는 Promise를 반환합니다. 이를 async/await 문법으로 감싸 기기 배터리 정보 카드를 그리는 로직을 매칭합니다.

```javascript
// async/await를 적용한 배터리 정보 조회 함수
async function displayBatteryStatus() {
  // await는 navigator.getBattery() 약속이 이행될 때까지 대기한 후 결과(battery 객체)를 반환합니다.
  const battery = await navigator.getBattery();
  
  console.log("배터리 잔량:", battery.level * 100 + "%");
  console.log("충전 여부:", battery.charging ? "충전 중" : "방전 중");
}
```

*   **적용 실습**: practice_03.html -> 1번 섹션

---

## 2. try/catch/finally 비동기 예외 처리 (실무 사례: 카드 승인 요청 및 폼 제출 차단)

### 1) 복습: form submit 이벤트와 preventDefault
*   비동기 결제 트랜잭션 요청을 보낼 때, 기존의 단순 버튼 click 이벤트 대신 실제 문서 구조 규격에 맞게 `<form>` 요소의 **`submit` 이벤트**를 낚아채어 처리합니다.
*   폼 제출 시 브라우저가 자동으로 주소를 새로고침(Reload)하여 페이지를 초기 상태로 돌려놓는 기본 동작을 **`e.preventDefault()`**를 활용해 강제로 차단합니다.
*   새로고침을 차단한 상태에서 비동기 `async/await` 함수를 차례대로 기동시켜, 페이지 깜빡임 없이 비동기 결제 및 장애 처리 로그를 터미널에 주입할 수 있습니다.

### 2) Promise.catch 대비 try/catch의 이점
*   기존 Promise 체인에서는 `.catch(err => ...)`를 사용해 에러를 잡았으나, 여러 개의 비동기 함수가 중첩되거나 조건문/반복문이 섞이면 에러 처리가 파편화되었습니다.
*   async/await 환경에서는 자바스크립트의 표준 예외 처리 문법인 **`try/catch/finally`를 비동기 연산에도 100% 동일하게 적용**할 수 있습니다.
*   비동기 연산 중 발생하는 네트워크 에러나 서버 API 에러가 자바스크립트의 엔진 에러(예: undefined 참조 오류)와 동일한 통로인 `catch (error)` 블록에서 통합 감지되므로 코드 응집력이 극대화됩니다.

### 3) try/catch/finally 흐름 비교 아스키 다이어그램
```text
           [ try 블록 진입 ]
     (가상 카드 결제 API await 호출)
                 |
         +-------+-------+
         |               |
     (에러 없음)    (API/네트워크 에러 발생)
         |               |
         v               v
    [결제 성공]     [ catch 블록으로 즉시 점프 ]
         |          (한도 초과/네트워크 복구 안내)
         |               |
         +-------+-------+
                 |
                 v
         [ finally 블록 실행 ]
  (성공/실패 무관하게 로딩 제거 및 폼 원복)
```

*   **적용 실습**: practice_03.html -> 2번 섹션

---

## 3. async/await 병렬 처리 최적화 (실무 사례: 다중 SNS 피드 통합 대시보드)

### 1) 직렬 await의 덫 (비효율적 패턴)
*   async/await 문법을 무심코 사용하면, 서로 의존성이 없는 작업들조차 개별 `await` 지시어 때문에 한 단계씩 순차 실행되어 성능이 크게 정체될 수 있습니다.
*   인스타그램(0.8초), 트위터(1.2초), 유튜브(0.6초) 데이터를 긁어와 대시보드에 뿌리는 상황을 직렬 await로 구성하면 다음과 같습니다.

```javascript
// 직렬 await - 비효율적 방식 (대기 시간 누적: 총 2.6초)
const instaData = await fetchInstagram(); // 0.8초 대기 후 끝날 때까지 멈춤
const twitterData = await fetchTwitter(); // 그 다음 1.2초 대기 후 끝날 때까지 멈춤
const youtubeData = await fetchYoutube(); // 마지막 0.6초 대기
```

### 2) Promise.all과 await의 병렬 결합 패턴
*   이러한 병목을 방지하기 위해, 먼저 3개의 비동기 함수를 동시 시동(Promise.all)하고, 그 전체가 묶여 완료되는 단일 Promise에 대해서만 `await`를 걸어 대기 시간을 가장 긴 1.2초로 압축합니다.

```javascript
// 병렬 await - 고성능 방식 (대기 시간 압축: 최장 1.2초)
const [instaData, twitterData, youtubeData] = await Promise.all([
  fetchInstagram(),
  fetchTwitter(),
  fetchYoutube()
]);
```

### 3) [중요] Promise.all vs 3차시 병렬 await 차이점 분석

현업에서 병렬 처리를 위해 동일하게 `Promise.all`을 이용하지만, 2차시에서 학습한 순수 Promise 방식과 3차시에서 다루는 async/await 방식은 가독성과 문법적 설계에서 큰 차이를 갖습니다.

| 비교 항목 | 2차시: 순수 Promise.all 패턴 | 3차시: Promise.all + await 패턴 |
| :--- | :--- | :--- |
| **비동기 지향 문법** | `Promise.all().then(results => ...)` | `const [a, b, c] = await Promise.all()` |
| **코드 가독성** | `.then()` 콜백 함수 블록(들여쓰기 뎁스)이 발생함 | 비동기 콜백 블록이 완전히 소거되어 평탄함 |
| **결과 데이터 가공** | `results[0]`, `results[1]` 등 인덱스로 직접 해체해야 함 | **배열 구조 분해 할당**을 통해 선언 즉시 각 변수에 직관적 파싱 완료 |
| **핵심 학습 목표** | 순차 실행 대비 병렬 통신의 속도 향상 기본 원리 이해 | **"직렬 await의 함정"**(무심코 await를 나열해 다시 느려지는 현상) 예방 및 튜닝 |

```javascript
// [소스코드 가독성 대조]

// A. 2차시 방식 (then 콜백과 인덱스 수동 분해)
Promise.all([fetchInsta(), fetchTwitter()])
  .then(results => {
    const insta = results[0];
    const twitter = results[1];
    console.log(insta, twitter); // then 콜백 내에 갇혀 있음
  });

// B. 3차시 방식 (await를 활용해 동기식 변수 대입처럼 평탄화)
const [insta, twitter] = await Promise.all([fetchInsta(), fetchTwitter()]);
console.log(insta, twitter); // 들여쓰기나 콜백 영역 없이 동기식처럼 사용 가능
```

*   **적용 실습**: practice_03.html -> 3번 섹션

---

## 4. 기존 Promise 체인의 async/await 리팩터링 (실무 사례: OAuth2 토큰 갱신 및 API 재요청)

### 1) 실무 상황: Access Token 만료 대응
*   웹 서비스에서 보안 API를 요청할 때 토큰이 만료되면 `401 Unauthorized` 에러를 응답받습니다.
*   이때 가동되어야 하는 복구 흐름은 다음과 같습니다:
    1. 보안 API 요청 시도 -> 401 권한 만료 감지 및 거절.
    2. Refresh Token으로 신규 Access Token 발급 요청 비동기 대기.
    3. 발급받은 신규 Access Token을 보안 헤더에 다시 실어, 원래 실패했던 보안 API를 재요청(Retry)하여 성공 처리.

### 2) Promise 체인 vs async/await 리팩터링 비교
이 흐름을 Promise 체인으로 짜면 에러를 잡은 catch 내부에서 다시 then/catch가 꼬리를 물게 되어 코드 분석이 무척 어렵습니다. 반면, async/await로 변환하면 동기식 순차 실행문처럼 아름답게 바뀝니다.

```javascript
// A. 기존 Promise 체인 방식 (복잡한 중첩 catch)
requestSecureData()
  .then(data => console.log("데이터 획득:", data))
  .catch(error => {
    if (error.status === 401) {
      return refreshAccessToken() // 리프레시 토큰 요청 리턴
        .then(newToken => requestSecureData(newToken)) // 재요청 리턴
        .then(retryData => console.log("갱신 후 재도전 데이터 획득:", retryData));
    }
    throw error;
  })
  .catch(finalErr => console.error("결국 최종 실패:", finalErr));

// B. async/await 리팩터링 방식 (동기식 일렬 구조)
async function handleSecureRequest() {
  try {
    const data = await requestSecureData();
    console.log("데이터 획득:", data);
  } catch (error) {
    if (error.status === 401) {
      console.log("토큰 만료 감증: 토큰 갱신 시도...");
      const newToken = await refreshAccessToken(); // await로 일렬 대기
      const retryData = await requestSecureData(newToken); // await로 일렬 대기
      console.log("갱신 후 재도전 데이터 획득:", retryData);
    } else {
      console.error("기타 보안 에러:", error.message);
    }
  }
}
```

*   **적용 실습**: practice_03.html -> 4번 섹션

---

## 학습 정리 체크리스트
- [ ] async 키워드가 선언된 함수가 리턴하는 결과는 일반 값인가, 아니면 항상 특정 비동기 객체인가?
- [ ] 신용카드 결제 유효성 검사 시 try/catch를 사용하여 네트워크 차단 에러와 유효성 검증 예외를 단일 catch 블록에서 동기식처럼 포착하는 문법 양식을 기술할 수 있는가?
- [ ] 세 개의 소셜 SNS 피드 로딩 비동기 연산을 직렬 await로 나열했을 때의 로딩 성능 문제를 방지하기 위해 Promise.all을 await와 결합하는 소스코드 구조를 작성할 수 있는가?
- [ ] OAuth2 인증 토큰 만료 및 자동 갱신(Refresh & Retry) 아키텍처를 기존 Promise 체인에서 async/await 구조로 전환했을 때 개발자가 체감하는 가독성과 유지보수성의 장점을 설명할 수 있는가?
