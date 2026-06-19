# DOM 조작 (콘텐츠 생성/수정/삭제)

## 1. 학습 목표
* DOM 요소를 동적으로 변경할 때 사용되는 `textContent`와 `innerHTML`의 차이점 및 크로스 사이트 스크립팅(XSS) 공격에 대응하는 보안 가이드를 습득합니다.
* 메모리상에 새로운 HTML 노드를 동적으로 생성하는 `createElement`와 이를 문서 트리에 주입 및 삭제하는 노드 조작 API(`appendChild`, `prepend`, `remove`)의 사용법을 익힙니다.
* 백엔드에서 받은 데이터 배열 형식(JSON 형태 등)을 `forEach` 순회와 구조분해 할당을 통해 화면 요소를 생성하고 실시간으로 그려내는 반복 렌더링(Iterative Rendering)을 마스터합니다.

---

## 2. textContent vs innerHTML (보안 가이드)

JS로 기존 태그 내부의 내용을 바꿀 때 가장 빈번히 사용되는 두 속성입니다.

### 1) `textContent` (보안 안전)
* **특징**: 할당하는 값을 순수한 **"텍스트 문자열"**로만 해석하여 렌더링합니다. HTML 태그가 섞여 있어도 태그 기능을 잃고 일반 글자(예: `&lt;h1&gt;`)로 안전하게 화면에 출력됩니다.
* **보안성**: 외부 악성 사용자가 작성한 스크립트 코드(`"<script>stealCookie()</script>"`)가 주입되어 브라우저 내에서 즉각 샐행되는 **크로스 사이트 스크립팅(XSS, Cross-Site Scripting)** 해킹 공격을 원천적으로 차단합니다. 따라서 단순 글자 교체 시에는 무조건 `textContent` 사용이 철칙입니다.

### 2) `innerHTML` (주의해서 사용)
* **특징**: 할당하는 값에 포함된 HTML 코드를 브라우저가 직접 파싱하여 **실제 요소 노드로 변환**해 줍니다. 
* **위험성**: 신뢰할 수 없는 사용자의 인풋값(게시판 글 등)을 `innerHTML`로 여과 없이 렌더링하면 보안 취약점이 뚫립니다. 
* **실무 대책**: 개발자가 정적 데이터(자체 JSON 등)를 바탕으로 신뢰할 수 있는 마크업 덩어리를 그릴 때만 제한적으로 활용해야 합니다.

---

## 3. DOM 노드 동적 제어 (생성·주입·삭제)
화면에 없는 요소를 메모리 영역에 임시 생성하고 문서에 부착시키는 정교한 수명 주기 조작법입니다.

```
                  ┌──────────────────────┐
                  │    Parent Element    │
                  └──────────┬───────────┘
            ┌────────────────┴────────────────┐
            ▼ (prepend: 맨 앞에 주입)          ▼ (appendChild: 맨 뒤에 주입)
   ┌──────────────────┐               ┌──────────────────┐
   │ New Child Element│               │ New Child Element│
   └──────────────────┘               └──────────────────┘
```

### 1) `document.createElement("태그명")`
* 지정된 태그를 가지는 비어있는 요소 객체를 메모리상에 새로 생성합니다. 
* 예: `const card = document.createElement("article");`

### 2) 노드 부착 (주입)
* **`부모.appendChild(자식)`**: 지정한 자식 요소를 부모 컨테이너의 **맨 마지막 자식 노드**로 덧붙여 넣습니다.
* **`부모.prepend(자식)`**: 지정한 자식 요소를 부모 컨테이너의 **맨 첫 번째 자식 노드**로 끼워 넣습니다.

### 3) 노드 삭제
* **`요소.remove()`**: 문서상에서 해당 요소를 깨끗하게 즉각 삭제 처리합니다.

---

## 4. 데이터 기반 반복 렌더링 (Iterative Rendering)
실무에서 가장 많이 쓰이는 구조로, 정형화된 데이터 배열(JSON 모사)을 순회하며 요소를 동적으로 대량 생산해 내는 구조입니다.

```javascript
// 1. 백엔드에서 날아온 가상의 특징 데이터 배열
const features = [
  { icon: "[Fast]", title: "빠른 속도", desc: "최적화된 성능" },
  { icon: "[Secure]", title: "안전한 보안", desc: "데이터 암호화" }
];

const featuresContainer = document.querySelector(".features-grid");

// 2. 반복 루프와 구조분해 할당(Destructuring) 결합
features.forEach(({ icon, title, desc }) => {
  // 메모리에 비어있는 article 노드 조립
  const card = document.createElement("article");
  card.className = "feature-card";
  
  // 백틱 템플릿 리터럴로 내용 구조 형성 (신뢰할 수 있는 정적 데이터이므로 innerHTML 허용)
  card.innerHTML = `
    <span class="icon">${icon}</span>
    <h3>${title}</h3>
    <p>${desc}</p>
  `;
  
  // 컨테이너 맨 뒤에 조립 완료된 카드 차곡차곡 부착
  featuresContainer.appendChild(card);
});
```

---

## 5. 실습 
대시보드 알림 메시지 센터를 구현하여, 알림 수신 시 `document.createElement`로 요소를 동적 생성하고, `prepend()`로 최신 알림을 상단에 삽입합니다. 또한 대량의 초기 데이터를 렌더링할 때 성능을 비약적으로 개선해 주는 실무 표준 최적화 API인 **`DocumentFragment`**를 활용하는 성능 지향형 코드를 매핑합니다.

* **적용 파일**: `main_04.js`
* **적용 대상**: 대시보드 실시간 알림 목록
```javascript
const noticeContainer = document.querySelector("#dynamic-grid");
const noticesData = [
  { title: "시스템 업데이트", desc: "서버 점검이 완료되었습니다." },
  { title: "새 메시지", desc: "이영희 님이 답글을 남겼습니다." }
];

// 1. 메모리 상에 가상의 빈 보관함(DocumentFragment)을 생성
const fragment = document.createDocumentFragment();

noticesData.forEach(({ title, desc }) => {
  const noticeCard = document.createElement("article");
  noticeCard.className = "feature-card";
  noticeCard.innerHTML = `<h3>${title}</h3><p>${desc}</p>`;
  
  // 브라우저 돔에 직접 넣는 것이 아닌, 가상 보관함에 1차 누적 (Reflow 발생 0회)
  fragment.appendChild(noticeCard);
});

// 2. 단 1회의 리플로우(Reflow)로 대량의 카드를 화면에 즉시 장착
noticeContainer.appendChild(fragment);
```