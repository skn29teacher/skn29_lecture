# 이벤트 전파(버블링)와 이벤트 위임

## 1. 학습 목표
* HTML 트리 구조에서 자식 노드에 발생한 이벤트가 상위 부모 노드들로 꼬리를 물고 연쇄 전파되는 이벤트 버블링(Event Bubbling)의 개념을 파악합니다.
* 이벤트 전파를 인위적으로 중단시키는 `event.stopPropagation()`의 문법적 역할과 이를 실무에서 오남용할 시 발생하는 부작용을 이해합니다.
* 다수의 동일 유형 요소에 개별 이벤트 리스너를 바인딩하지 않고, 공통 상위 부모 1곳에만 리스너를 결합해 이벤트를 병합 처리하는 실무 최적화 아키텍처인 **이벤트 위임(Event Delegation)** 을 마스터합니다.

---

## 2. 이벤트 버블링 (Event Bubbling) 이란?
HTML의 특정 태그(예: `<span>`)를 클릭하면, 이벤트는 단순히 그 태그에만 머무르지 않고 부모(`<li>`) -> 상위 부모(`<nav>`) -> 더 상위 부모(`<body>`) 순으로 거슬러 올라가며 전파됩니다. 마치 물속의 거품(Bubble)이 위로 둥둥 떠오르는 모습과 흡사하여 **버블링** 이라 명명되었습니다.

```
[HTML 트리 구조]
   document  (최상위 조상)
      ▲
     body
      ▲
    section
      ▲
     div  (.gallery)          <-- 부모 컨테이너
      ▲
   article  (.gallery-item)   <-- 중간 자식
      ▲
     img  [실제 클릭 target]   <-- 마우스가 물리적으로 가리킨 표적 노드
```

> [!NOTE]
> 대부분의 웹 브라우저 이벤트(click, keydown 등)는 기본 설정이 버블링입니다. (단, focus, blur, mouseenter, mouseleave 등은 전파되지 않는 특수 이벤트입니다.)

---

## 3. 이벤트 전파 차단: `event.stopPropagation()`
* **역할**: 핸들러 함수 내부에서 이 메서드를 호출하면, 현재 노드 이후로 이벤트가 상위 부모로 거슬러 올라가지 않도록 물리적인 흐름을 강제 중단시킵니다.
* **실무적 주의사항**: 버블링을 강제로 막아버리면 문서 전체 영역에서 글로벌 이벤트를 감지(예: 바깥쪽 아무 데나 누르면 팝업창 닫히는 기능 등)할 때 버블링이 끊겨 오작동하게 됩니다. 따라서 특수한 팝업 버튼 등 예외적인 겹침 처리 상황을 제외하고는 **가급적 `stopPropagation()`의 무분별한 사용은 강하게 지양**해야 합니다.

---

## 4. 실무 성능의 핵심: 이벤트 위임 (Event Delegation)

만약 갤러리 썸네일 이미지가 1,000장 존재할 때 이미지 클릭 시 확대 팝업을 띄우고자 한다면, 1,000개의 `img` 마다 일일이 리스너를 다는 행위는 **메모리를 엄청나게 낭비** 하고 브라우저 성능을 바닥으로 끌어내립니다.

또한, 자바스크립트로 신규 이미지를 동적으로 1장 추가할 때마다 리스너 등록 코드를 매번 다시 실행해주어야 하는 지옥 같은 유지보수 장벽이 발생합니다.

### 해결책: 이벤트 위임 (Event Delegation)
자식들의 이벤트가 어차피 부모로 버블링되는 성격을 역이용하여, **부모 컨테이너 1곳에만 단 하나의 `addEventListener`를 등록** 해 놓습니다. 그리고 클릭된 대상(`event.target`)이 우리가 목표한 자식 요소를 가리키고 있는지 `closest()`로 필터링하여 총괄 수거하는 기법입니다.

```javascript
// 이벤트 위임 모범 예제
const galleryContainer = document.querySelector(".gallery-grid");

galleryContainer.addEventListener("click", (event) => {
  // 클릭된 대상(event.target)에서 가장 가까운 .gallery-item 조상을 역추적
  const clickedCard = event.target.closest(".gallery-item");
  
  // 1. 갤러리 카드 밖(빈 틈 등)을 누른 경우 즉각 스킵 처리 (방어 코드)
  if (!clickedCard) return;
  
  // 2. 갤러리 카드 내부인 경우 정상 구동
  const imgTitle = clickedCard.dataset.title;
  console.log("선택한 작품 정보:", imgTitle);
});
```

---

## 5. 실습 미션 적용 (이론 적용 코드)
대화형 FAQ 아코디언 컴포넌트의 부모 목록 컨테이너(`.faq-container`)에 단 하나의 클릭 이벤트 리스너를 위임 부착하고, 질문 제목 클릭 시 본문 내용(`.faq-answer`)을 펼치는 로직을 매핑합니다.

* **적용 파일**: `day02_javascript/06_event_delegation/main_06.js`
* **적용 대상**: FAQ 아코디언 목록
```javascript
const faqContainer = document.querySelector(".faq-container");

// 부모 컨테이너에 단 하나의 리스너만 매핑하여 위임 처리
faqContainer.addEventListener("click", (event) => {
  // closest를 이용해 클릭된 대상이 FAQ 아이템 조상인지 확인
  const faqItem = event.target.closest(".faq-item");
  if (!faqItem) return; // 빈 여백 클릭 방어

  // 질문 헤더 영역(.faq-question)을 정확히 지향하여 클릭했는지 확인
  const isQuestion = event.target.closest(".faq-question");
  if (isQuestion) {
    faqItem.classList.toggle("active");
  }
});
```

---

## 6. 학습 정리 체크리스트
- [ ] 자식 요소를 클릭했는데 부모 요소에 걸어놓은 클릭 이벤트 리스너가 호출되는 웹 브라우저의 전파 현상을 무엇이라 하는가?
- [ ] `event.stopPropagation()`을 실무 프로젝트에서 무분별하게 남발하면 어떤 부작용(예: 팝업 닫기 실패 등)이 발생할 수 있는가?
- [ ] 이벤트 위임을 적용했을 때, 개별 동적 요소에 리스너를 매번 재등록하지 않아도 무리 없이 감지할 수 있는 구동 원리를 버블링과 연계해 설명할 수 있는가?
- [ ] `closest(".gallery-item")`를 필터 방어 조건문(`if (!item) return;`)과 함께 결합하여 클릭 대상 오인식 에러를 회피할 수 있는가?
