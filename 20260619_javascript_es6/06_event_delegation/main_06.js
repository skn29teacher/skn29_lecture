/**
 * ==========================================================================
 * 이벤트 전파와 이벤트 위임 (main_06.js)
 * 학습 주제: 버블링 전파 시각화, stopPropagation 차단, 이벤트 위임 및 closest 필터링
 * ==========================================================================
 */

document.addEventListener("DOMContentLoaded", () => {
  // DOM 타깃 캐싱
  const termBubble = document.getElementById("term-bubble");
  const termDelegation = document.getElementById("term-delegation");
  const delegatedParent = document.getElementById("delegated-parent-list");

  // --------------------------------------------------------------------------
  // [1] 이벤트 버블링(전파) 시각화 vs stopPropagation() 차단 대조
  // --------------------------------------------------------------------------

  // 공통 초기화 헬퍼 함수
  const clearBubbleClasses = () => {
    document.querySelectorAll(".grandparent-box, .parent-box, .child-box").forEach(box => {
      box.classList.remove("triggered");
    });
  };

  // A. 좌측: 기본 버블링 전파 실험 구역
  const bGp = document.getElementById("b-gp");
  const bP = document.getElementById("b-p");
  const bC = document.getElementById("b-c");

  bGp?.addEventListener("click", (event) => {
    bGp.classList.add("triggered");
    termBubble.textContent += `-> [조상 박스 리스너 감지] target: ${event.target.id}, currentTarget: ${event.currentTarget.id}\n`;
  });

  bP?.addEventListener("click", (event) => {
    bP.classList.add("triggered");
    termBubble.textContent += `-> [부모 박스 리스너 감지] target: ${event.target.id}, currentTarget: ${event.currentTarget.id}\n`;
  });

  bC?.addEventListener("click", (event) => {
    clearBubbleClasses();
    termBubble.textContent = "[기본 버블링 전파 개시]\n";
    bC.classList.add("triggered");
    termBubble.textContent += `-> [자식 박스 리스너 감지] target: ${event.target.id}, currentTarget: ${event.currentTarget.id}\n`;
  });

  // B. 우측: stopPropagation() 전파 차단 실험 구역
  const sGp = document.getElementById("s-gp");
  const sP = document.getElementById("s-p");
  const sC = document.getElementById("s-c");

  sGp?.addEventListener("click", (event) => {
    sGp.classList.add("triggered");
    termBubble.textContent += `-> [조상 박스 리스너 감지] target: ${event.target.id}, currentTarget: ${event.currentTarget.id}\n`;
  });

  sP?.addEventListener("click", (event) => {
    sP.classList.add("triggered");
    termBubble.textContent += `-> [부모 박스 리스너 감지] target: ${event.target.id}, currentTarget: ${event.currentTarget.id}\n`;
  });

  sC?.addEventListener("click", (event) => {
    clearBubbleClasses();
    termBubble.textContent = "[전파 차단 stopPropagation 실행]\n";
    sC.classList.add("triggered");
    termBubble.textContent += `-> [자식 박스 리스너 감지] target: ${event.target.id}, currentTarget: ${event.currentTarget.id}\n`;
    
    // 상위 부모로 이벤트가 올라가지 않도록 버블링 전파 가로막기
    event.stopPropagation();
    
    termBubble.textContent += `[전파 완전 차단] event.stopPropagation()이 호출되어 부모/조상 리스너 작동이 억제되었습니다.\n`;
  });

  // 하이라이트 지우개
  document.getElementById("btn-clear-bubble")?.addEventListener("click", () => {
    clearBubbleClasses();
    termBubble.textContent = "보드 하이라이트가 청소되었습니다.";
  });

  // --------------------------------------------------------------------------
  // [2] 이벤트 위임 (Event Delegation) 및 closest()
  // --------------------------------------------------------------------------
  let listCount = 2; // 기본 마크업에 2개 존재함

  // 2-A. 동적 아이템 추가 버튼 (개별 리스너를 결합하지 않고 돔만 추가)
  document.getElementById("btn-add-item")?.addEventListener("click", () => {
    listCount++;
    
    // 메모리에 새 <li> 생성
    const newItem = document.createElement("li");
    newItem.className = "delegated-item";
    newItem.setAttribute("data-id", `item-${listCount}`);
    
    newItem.innerHTML = `
      <span class="item-text">신규 추가 상품 ${listCount}</span>
      <button class="btn-delete-item">삭제</button>
    `;
    
    // 부모 컨테이너에 추가 (새 아이템에 addEventListener는 전혀 걸지 않음)
    delegatedParent?.appendChild(newItem);
    termDelegation.textContent = `신규 상품 ${listCount}을 목록 맨 뒤에 동적으로 부착했습니다. (이벤트 리스너 등록 횟수: 여전히 부모 1개로 유지)`;
  });

  // 2-B. 부모 목록 컨테이너 단 1곳에만 클릭 위임 이벤트 바인딩
  delegatedParent?.addEventListener("click", (event) => {
    // 1단계: 클릭된 대상(event.target)에서 가장 가까운 .btn-delete-item 탐색
    const deleteBtn = event.target.closest(".btn-delete-item");
    
    // 2단계: 만약 삭제 버튼 클릭이 감지되었다면
    if (deleteBtn) {
      // 삭제 버튼이 들어있는 부모 <li> 요소를 closest로 역추적
      const targetItem = deleteBtn.closest(".delegated-item");
      if (targetItem) {
        const itemId = targetItem.getAttribute("data-id");
        const itemText = targetItem.querySelector(".item-text")?.textContent ?? "";
        
        // 화면에서 노드 제거
        targetItem.remove();
        termDelegation.textContent = `[위임 삭제 처리 완료] ID: ${itemId} | "${itemText}" 요소를 리스트에서 성공적으로 삭제했습니다.`;
      }
      return; // 삭제 로직 종료 후 탈출
    }

    // 3단계: 삭제 버튼 외의 일반 텍스트나 빈 영역 클릭 시
    const targetItem = event.target.closest(".delegated-item");
    
    // 목록 빈 틈(마진 등)을 눌렀을 때 오류 방지
    if (!targetItem) return;

    // 정상 클릭 영역인 경우 상품 고유 속성 데이터 추출
    const itemId = targetItem.getAttribute("data-id");
    const itemText = targetItem.querySelector(".item-text")?.textContent ?? "";

    termDelegation.textContent = `[위임 선택 감지]\n` +
      `- 선택한 상품 식별자(data-id): ${itemId}\n` +
      `- 선택한 상품 텍스트: ${itemText}`;
  });

  // 목록 전체 비우기
  document.getElementById("btn-clear-list")?.addEventListener("click", () => {
    if (delegatedParent) delegatedParent.innerHTML = "";
    listCount = 0;
    termDelegation.textContent = "상품 목록을 전체 비웠습니다.";
  });
});
