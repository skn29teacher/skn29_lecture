# DOM 선택과 탐색

## 1. 학습 목표
* 구식 DOM 선택 API(`getElementById`, `getElementsByClassName`)의 단점을 파악하고, 모던 표준 방식인 `querySelector`와 `querySelectorAll`의 셀렉터 조합 규칙을 습득합니다.
* 특정 요소를 기준으로 상위 부모, 하위 자식, 인접 형제 노드를 정밀하게 찾아 들어가는 DOM 탐색 API(`closest`, `children`, `parentElement`, `nextElementSibling`)를 이해합니다.
* 스타일을 직접 변경(`style.color = "red"`)하는 안 좋은 코드를 지양하고, CSS 클래스 규칙을 입혔다 떼어내는 `classList` 객체의 핵심 메서드(`add`, `remove`, `toggle`, `contains`)를 활용합니다.

---

## 2. 모던 DOM 선택 표준: querySelector / querySelectorAll
현대 JavaScript는 과거와 같이 ID용, 클래스용 선택 API를 구분하여 호출하지 않고, **CSS 선택자 문법 그대로** DOM을 지목합니다.

```javascript
// 1. 단일 요소 선택 (가장 먼저 만나는 1개의 노드만 반환)
const mainNav = document.querySelector("#main-nav");
const activeMenu = document.querySelector(".nav-list .active-item");

// 2. 다수 요소 선택 (매칭되는 모든 요소를 유사 배열 형태인 NodeList로 반환)
const cards = document.querySelectorAll(".feature-card");
const galleryImgs = document.querySelectorAll(".gallery img");
```

> [!IMPORTANT]
> `querySelectorAll`이 반환하는 **`NodeList`**는 순수 Array(배열)가 아닌 **유사 배열**입니다. 다행히 현대 브라우저 규격상 **`forEach`** 메서드는 기본 탑재되어 순회가 가능하지만, `map`, `filter`, `reduce` 등의 순수 배열 메서드는 직접 쓸 수 없습니다. 만약 순수 배열로 다루고 싶다면 전개 연산자를 사용하여 **`[...cards]`**로 배열 캐스팅 변환 과정을 거치는 것이 실무 관례입니다.

---

## 3. DOM 트리 상하좌우 탐색 (DOM Navigation)
원하는 요소를 한 번에 querySelector로 찾기 어려울 때, 또는 특정 이벤트가 일어난 타깃 요소를 기준으로 근처에 있는 다른 형제나 부모를 가리켜야 할 때 탐색 API를 동원합니다.

```
                  ┌─────────────────┐
                  │  parentElement  │  (상위 부모 노드 추적)
                  └────────┬────────┘
                           │ ▲
                           ▼ │
 ┌─────────────────────────┼─────────────────────────┐
 │ previousElementSibling  │  [ 기준 target 요소 ]   │  nextElementSibling
 └─────────────────────────┼─────────────────────────┘ (오른쪽 형제)
                           │ ▲
                           ▼ │
                  ┌────────┴────────┐
                  │    children     │  (하위 직속 자식 목록 NodeList)
                  └─────────────────┘
```

* **`parentElement`**: 기준 요소의 직속 상위 부모 요소를 참조합니다.
* **`children`**: 기준 요소의 하위 직속 자식 요소들을 HTMLCollection 형태로 반환합니다.
* **`closest("CSS선택자")` (매우 중요)**: 기준 요소 자신을 포함하여 **가장 가까운 상위 조상 요소 중 CSS선택자와 일치하는 대상**을 위로 거슬러 올라가며 찾아냅니다. 이벤트 위임 구현 시 타깃 카드를 역추적할 때 필수적으로 쓰입니다.
* **`nextElementSibling` / `previousElementSibling`**: 각각 오른쪽 인접 형제와 왼쪽 인접 형제 요소를 지목합니다.

---

## 4. 클래스 제어의 정석: classList
인라인 스타일(`el.style.backgroundColor = "black"`)을 JS에서 직접 다루면 디자인 변경 시 HTML/CSS/JS를 모두 뒤집어야 하므로 강하게 배제됩니다. 대신 CSS 파일에 디자인 클래스를 마련해두고, JS로는 클래스명만 삽입/삭제해 줍니다.

* **`classList.add("className")`**: 특정 클래스를 추가합니다. (기존 클래스 훼손 안 함)
* **`classList.remove("className")`**: 특정 클래스를 제거합니다.
* **`classList.toggle("className")`**: 특정 클래스가 있으면 제거하고, 없으면 넣어줍니다. (토글 스위치 기능)
* **`classList.contains("className")`**: 특정 클래스가 현재 포함되어 있는지 여부를 Boolean(`true`/`false`)으로 반환합니다.

---

## 5. 실습 
게시판의 댓글(Comment) 카드 컴포넌트 내부에서 '답글 달기' 또는 '댓글 내용 강조' 동작을 할 때, 클릭이 감지된 요소를 기준으로 가장 가까운 부모 댓글 카드(`.comment-card`)를 거슬러 올라가고(`closest`), 그 부모 밑에 위치한 댓글 본문 영역과 작성자 이름을 하향 탐색(`querySelector`)하여 클래스를 입히는 탐색 직입니다.