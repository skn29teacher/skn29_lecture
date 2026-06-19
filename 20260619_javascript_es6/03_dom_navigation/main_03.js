/**
 * ==========================================================================
 * DOM 선택과 탐색 (main_03.js)
 * 학습 주제: NodeList 순수 배열 변환, DOM 트리 경로 탐색, classList 상태 제어
 * ==========================================================================
 */

document.addEventListener("DOMContentLoaded", () => {
  // DOM 출력 캐싱
  const termNodelist = document.getElementById("term-nodelist");
  const termTree = document.getElementById("term-tree");
  const termClass = document.getElementById("term-class");
  const termComment = document.getElementById("term-comment");

  // --------------------------------------------------------------------------
  // [1] NodeList 유사 배열의 순수 배열 캐스팅 실증
  // --------------------------------------------------------------------------
  const dummyNodeList = document.querySelectorAll(".dummy-item");

  // 1-A. 유사 배열에 map 직접 실행 시도 (에러 유도)
  document.getElementById("btn-nodelist-error")?.addEventListener("click", () => {
    try {
      // NodeList 프로토타입에는 map 메서드가 존재하지 않으므로 TypeError 발생함
      const result = dummyNodeList.map(item => item.textContent);
      termNodelist.textContent = `성공: ${result.join(", ")}`;
    } catch (e) {
      termNodelist.textContent = `[유사 배열 직접 map 실행 실패]\n` +
        `오류메시지: ${e.message}\n` +
        `이유: querySelectorAll의 결과인 NodeList는 유사 배열이라 고차함수 map()을 쓸 수 없습니다.`;
    }
  });

  // 1-B. 전개 연산자 캐스팅 후 map 실행
  document.getElementById("btn-nodelist-success")?.addEventListener("click", () => {
    // 전개 연산자(...)를 사용해 NodeList의 알맹이들을 순수 배열 리터럴 속에 넣어 형변환 수행
    const pureArray = [...dummyNodeList];
    
    // 이제 순수 배열이 되었으므로 map, filter 등의 고차함수를 자유롭게 사용 가능
    const parsedTextArray = pureArray.map((item, index) => `[아이템 ${index + 1}] ${item.textContent}`);
    
    termNodelist.textContent = `[전개 연산자 배열 변환 성공]\n` +
      `캐스팅 적용 결과: [ ${parsedTextArray.join(", ")} ]`;
  });

  // --------------------------------------------------------------------------
  // [2] DOM 트리 상하좌우 네비게이션
  // --------------------------------------------------------------------------
  const childTwo = document.getElementById("child-two");
  const demoParent = document.getElementById("demo-parent");

  // 모든 active 하이라이트 클래스를 청소하는 헬퍼 함수
  const clearTreeHighlight = () => {
    demoParent?.classList.remove("active");
    const allChildren = demoParent?.querySelectorAll(".child-node") ?? [];
    allChildren.forEach(child => child.classList.remove("active"));
  };

  // 2-A. 기준(자식 2)에서 부모 탐색 (parentElement)
  document.getElementById("btn-find-parent")?.addEventListener("click", () => {
    clearTreeHighlight();
    const parent = childTwo?.parentElement;
    if (parent) {
      parent.classList.add("active");
      termTree.textContent = `기준(자식 2)의 직속 부모 탐색 성공: ID = "${parent.id}"`;
    }
  });

  // 2-B. 기준(자식 2)에서 왼쪽 형제 탐색 (previousElementSibling)
  document.getElementById("btn-find-left")?.addEventListener("click", () => {
    clearTreeHighlight();
    const leftSibling = childTwo?.previousElementSibling;
    if (leftSibling) {
      leftSibling.classList.add("active");
      termTree.textContent = `기준(자식 2)의 왼쪽 형제(previousElementSibling) 탐색 성공: ID = "${leftSibling.id}"`;
    } else {
      termTree.textContent = `왼쪽 형제 노드가 존재하지 않습니다.`;
    }
  });

  // 2-C. 기준(자식 2)에서 오른쪽 형제 탐색 (nextElementSibling)
  document.getElementById("btn-find-right")?.addEventListener("click", () => {
    clearTreeHighlight();
    const rightSibling = childTwo?.nextElementSibling;
    if (rightSibling) {
      rightSibling.classList.add("active");
      termTree.textContent = `기준(자식 2)의 오른쪽 형제(nextElementSibling) 탐색 성공: ID = "${rightSibling.id}"`;
    } else {
      termTree.textContent = `오른쪽 형제 노드가 존재하지 않습니다.`;
    }
  });

  // 2-D. 부모에서 모든 직속 자식 탐색 (children)
  document.getElementById("btn-find-children")?.addEventListener("click", () => {
    clearTreeHighlight();
    // parentElement.children은 HTMLCollection 유사배열을 반환합니다.
    const childrenList = demoParent?.children ?? [];
    
    // demoParent 하위에 children-list 박스가 있으므로 한 깊이 더 들어가 자식 노드들을 획득합니다.
    const innerContainer = demoParent?.querySelector(".children-list");
    const nodes = innerContainer?.children ?? [];
    
    // 유사 배열을 순회하여 모든 자식 노드에 하이라이트 클래스 부여
    let childrenIds = [];
    for (let i = 0; i < nodes.length; i++) {
      nodes[i].classList.add("active");
      childrenIds.push(nodes[i].id);
    }
    
    termTree.textContent = `부모 하위의 모든 직속 자식 노드(children) 수집 성공:\n-> [ ${childrenIds.join(", ")} ]`;
  });

  // 하이라이트 초기화 버튼
  document.getElementById("btn-clear-tree")?.addEventListener("click", () => {
    clearTreeHighlight();
    termTree.textContent = `트리 하이라이트가 초기화되었습니다.`;
  });

  // --------------------------------------------------------------------------
  // [3] classList API를 이용한 컴포넌트 상태 제어
  // --------------------------------------------------------------------------
  const toggleCard = document.getElementById("my-toggle-card");

  // 3-A. 다크 테마 클래스 추가 (add)
  document.getElementById("btn-class-add")?.addEventListener("click", () => {
    toggleCard?.classList.add("dark-theme");
    termClass.textContent = `classList.add("dark-theme") 실행 완료.`;
  });

  // 3-B. 다크 테마 클래스 제거 (remove)
  document.getElementById("btn-class-remove")?.addEventListener("click", () => {
    toggleCard?.classList.remove("dark-theme");
    termClass.textContent = `classList.remove("dark-theme") 실행 완료.`;
  });

  // 3-C. 축소 및 노출 토글 (toggle)
  document.getElementById("btn-class-toggle")?.addEventListener("click", () => {
    // toggle()은 클래스가 없으면 추가하고, 있으면 삭제하여 반환 상태를 Boolean으로 알려줍니다.
    const hasClassNow = toggleCard?.classList.toggle("collapsed");
    termClass.textContent = `classList.toggle("collapsed") 실행 완료.\n현재 축소 상태 여부: ${hasClassNow ? "축소됨" : "펼쳐짐"}`;
  });

  // 3-D. 다크 테마 유무 판별 (contains)
  document.getElementById("btn-class-contains")?.addEventListener("click", () => {
    // contains()는 특정 클래스가 포함되어 있는지 여부를 판별해 줍니다.
    const isDark = toggleCard?.classList.contains("dark-theme") ?? false;
    termClass.textContent = `classList.contains("dark-theme") 실행.\n현재 결과: ${isDark ? "다크 테마가 적용되어 있습니다." : "일반 밝은 테마 상태입니다."}`;
  });

  // --------------------------------------------------------------------------
  // [4] 종합 실습: closest와 계층 탐색을 활용한 댓글 컴포넌트 제어
  // --------------------------------------------------------------------------
  
  // 댓글 목록 내의 버튼들을 일괄 선택
  const highlightButtons = document.querySelectorAll(".btn-comment-highlight");
  const authorButtons = document.querySelectorAll(".btn-comment-author");

  // 각 댓글 카드 강조 토글 버튼 바인딩
  highlightButtons.forEach(button => {
    button.addEventListener("click", (event) => {
      // 클릭 대상 획득
      const clicked = event.target;
      
      // closest()를 사용해 상위 계층 중 가장 가까운 댓글 카드 .comment-card 역추적
      const card = clicked.closest(".comment-card");
      if (card) {
        // card의 classList를 토글하여 하이라이트 CSS 적용
        card.classList.toggle("highlighted");
        const isHighlighted = card.classList.contains("highlighted");
        termComment.textContent = `ID가 ${card.id}인 댓글 카드의 하이라이트 상태가 [${isHighlighted ? "활성" : "비활성"}] 상태로 토글되었습니다.`;
      }
    });
  });

  // 각 댓글 카드 작성자 명칭 수거 버튼 바인딩
  authorButtons.forEach(button => {
    button.addEventListener("click", (event) => {
      const clicked = event.target;
      
      // closest()로 부모 카드를 찾아낸 후 하위 자식 노드로 찾아 내려가서 텍스트 획득
      const card = clicked.closest(".comment-card");
      if (card) {
        const authorNode = card.querySelector(".comment-author");
        const authorName = authorNode?.textContent ?? "이름 없음";
        termComment.textContent = `댓글 카드(${card.id})에서 추출한 작성자 이름: ${authorName}`;
      }
    });
  });
});
