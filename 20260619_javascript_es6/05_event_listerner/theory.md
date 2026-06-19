# 이벤트 리스너 기초

## 1. 학습 목표
* DOM 트리가 브라우저 메모리에 파싱 및 구축 완료되는 안전한 시작 시점을 잡아내는 `DOMContentLoaded` 이벤트의 중요성을 이해합니다.
* HTML 마크업 내부에 직접 자바스크립트를 섞어 적는 구식 인라인 이벤트 속성(`onclick`)의 심각한 단점을 파악하고, `addEventListener` 표준 등록 방식과 핸들러 함수 분리 아키텍처를 적용합니다.
* 이벤트가 발생했을 때 웹 브라우저가 콜백 인자로 자동 전달해 주는 이벤트 객체(`event`)의 중요 속성인 `target`과 `currentTarget`을 파악합니다.

---

## 2. 안전한 스크립트 실행의 보증수표: DOMContentLoaded
만약 HTML 파일 헤더 부분에서 스크립트를 로드했는데 스크립트 내부에 `document.querySelector(".hero")`와 같이 DOM을 탐색하는 코드가 들어있다면, 브라우저가 아직 바디의 해당 태그를 파싱하기도 전이므로 **`null` 참조 에러**가 발생합니다.

이를 근본적으로 안전하게 방어하기 위해 전체 스크립트를 감싸는 진입점 이벤트 리스너를 설계합니다.

```javascript
// DOM 파싱이 완전히 완료되어 태그 메모리 적재가 끝난 즉시 호출됩니다. (이미지 로딩 완료는 대기하지 않아 로딩이 빠름)
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM 트리가 준비되었습니다. 자바스크립트 초기화 로직을 구동합니다.");
  init(); // 전체 이벤트 바인딩 및 렌더링 구동 함수
});
```

---

## 3. onclick 속성 금지 vs addEventListener 권장

### 1) 구식 방식 (완전 금지)
`<button onclick="handleBtnClick()">제출</button>`
* **단점**: HTML 마크업과 JS 제어 로직이 더럽게 뒤섞여 협업이 불가능합니다. 또한 하나의 버튼에 단 하나의 동작만 바인딩할 수 있어 다른 개발자가 쓴 동작이 기존 스크립트를 덮어쓰는 대형 버그를 일으킵니다.

### 2) 모던 addEventListener 표준 (실무 표준)
* **장점**: HTML은 뼈대만 두고 JS 파일 내부에서 완벽하게 제어합니다(관심사 분리). 하나의 요소에 여러 개의 다른 리스너를 등록해 두어도 모두 정상적으로 동시 구동됩니다.
* **함수 분리 규칙**: 익명 함수(람다)를 직접 대입하기보다, **이름이 명확히 지어진 외부 핸들러 함수** 로 분리하여 바인딩하는 것이 메모리 최적화 및 유지보수, 이벤트 해제(`removeEventListener`)에 필수적입니다.

```javascript
// 핸들러 함수 분리 아키텍처
const handleMenuToggle = (event) => {
  const menu = document.querySelector(".nav-menu");
  menu.classList.toggle("open");
};

// 바인딩
menuBtn.addEventListener("click", handleMenuToggle);
```

---

## 4. 이벤트 객체 (Event Object) 와 event.target
사용자가 마우스를 클릭하거나 키보드를 입력하면, 브라우저는 발생한 이벤트에 대한 온갖 메타데이터(클릭 좌표, 입력된 키 값, 클릭된 요소 등)를 담은 **이벤트 객체(`e` 또는 `event`)**를 생성하여 핸들러 함수의 첫 번째 인자로 던져줍니다.

* **`event.target`**: 실제 물리적으로 **마우스 클릭 이벤트가 직접 일어난 최하단 요소 노드**를 가리킵니다. (예: 버튼 글씨를 감싸고 있는 `<span>` 태그를 클릭했다면 target은 `<span>`이 됨)
* **`event.currentTarget`**: 이벤트 리스너가 **실제로 바인딩되어 동작을 대기하고 있던 요소 노드**를 가리킵니다. (예: 버튼 자체에 addEventListener를 걸었다면 target이 span이더라도 currentTarget은 버튼 요소가 됨)

---

## 5. 실습 미션 적용 (이론 적용 코드)
대중적인 쇼핑몰의 "장바구니 담기" 시스템을 통해 복수 이벤트 등록과 타깃 노드 분석을 구현합니다.

* **적용 파일**: `main_05.js`
* **적용 대상**: 장바구니 추가 버튼 및 카운터
```javascript
// DOM 요소 선택
const addCartBtn = document.querySelector("#btn-add-cart");
const cartCountEl = document.querySelector("#cart-count");

// 기능 A: 장바구니 숫자 증가
const handleCartCount = () => {
  const currentCount = parseInt(cartCountEl.textContent ?? "0", 10);
  cartCountEl.textContent = currentCount + 1;
};

// 기능 B: 이벤트 객체 디버깅 로그 출력
const handleDebugLog = (event) => {
  console.log("실제 클릭한 지점 (event.target):", event.target);
  console.log("이벤트가 바인딩된 버튼 (event.currentTarget):", event.currentTarget);
};

// DOMContentLoaded 초기화 루프 안에서 안전하게 두 기능을 버튼 하나에 바인딩
document.addEventListener("DOMContentLoaded", () => {
  addCartBtn.addEventListener("click", handleCartCount);
  addCartBtn.addEventListener("click", handleDebugLog);
});
```

---

## 6. 학습 정리 체크리스트
- [ ] HTML 바디 하단에 스크립트를 로드하는 방식이 있어도 `DOMContentLoaded` 리스너를 명시적으로 쓰는 설계적 이유는 무엇인가?
- [ ] HTML 파일 안의 태그에 `onclick="..."` 속성을 사용하면 왜 유지보수가 파괴되는지 서술할 수 있는가?
- [ ] 이벤트 핸들러 함수에 매개변수로 명시하는 `event` 변수는 누가 채워서 넘겨주는가?
- [ ] 버튼 안의 폰트 아이콘(`<i>` 등)을 마우스로 조준하여 눌렀을 때 `event.target`과 `event.currentTarget`이 각각 지목하는 HTML 요소는 어떻게 다른가?
