/**
 * ==========================================================================
 *  DOM 조작 (main_04.js)
 * 학습 주제: textContent vs innerHTML XSS 방어, 동적 createElement 제어, DocumentFragment 최적화
 * ==========================================================================
 */

document.addEventListener("DOMContentLoaded", () => {
  // DOM 타깃 캐싱
  const xssInput = document.getElementById("input-xss");
  const xssRenderBox = document.getElementById("xss-render-box");
  const termXss = document.getElementById("term-xss");
  const noticeContainer = document.getElementById("notice-board-container");
  const fragmentContainer = document.getElementById("fragment-grid-container");

  // --------------------------------------------------------------------------
  // [1] textContent vs innerHTML XSS 보안성 비교 실증
  // --------------------------------------------------------------------------

  // 1-A. textContent 주입 (안전 이스케이프)
  document.getElementById("btn-inject-text")?.addEventListener("click", () => {
    const rawValue = xssInput.value;
    
    // textContent는 값을 단순 평문 텍스트로 처리하므로 꺾쇠가 파싱되지 않아 안전함
    xssRenderBox.textContent = rawValue;
    
    termXss.textContent = `[textContent 안전 주입 완료]\n` +
      `입력 문자열이 HTML로 파싱되지 않고 안전하게 문자 자체로 치환되었습니다.\n` +
      `콘솔에 XSS 스크립트 실행 공격이 절대 구동되지 않습니다.`;
  });

  // 1-B. innerHTML 주입 (XSS 위험 노출)
  document.getElementById("btn-inject-html")?.addEventListener("click", () => {
    const rawValue = xssInput.value;
    
    termXss.textContent = `[innerHTML 주입 진행 - XSS 유도]\n` +
      `입력값 내부의 HTML 꺾쇠가 실시간 파싱되어 렌더링을 시작합니다.\n` +
      `만약 스크립트(onerror 속성 등)가 내장되어 있었다면 즉시 코드가 실행됩니다.\n` +
      `보안 콘솔 및 상단 팝업 경고 상태를 확인해 보세요.`;
      
    // innerHTML은 HTML 코드를 직접 DOM 트리 객체로 해석하므로 위험도가 극도로 높음
    xssRenderBox.innerHTML = rawValue;
  });

  // --------------------------------------------------------------------------
  // [2] 알림 센터 노드 제어 (생성, prepend, append, remove)
  // --------------------------------------------------------------------------
  let noticeCount = 0;

  // 동적 알림 엘리먼트를 구성하는 공통 헬퍼 함수
  const createNoticeElement = (titleText, descText) => {
    // 1단계: 메모리 상에 div 요소 생성
    const noticeItem = document.createElement("div");
    noticeItem.className = "notice-item";
    noticeItem.id = `notice-${Date.now()}`;

    // 2단계: 내부 구조 조립 (데이터 바인딩)
    const contentWrap = document.createElement("div");
    contentWrap.className = "notice-content";
    
    const title = document.createElement("p");
    title.className = "notice-title";
    title.textContent = titleText;
    
    const desc = document.createElement("p");
    desc.className = "notice-text";
    desc.textContent = descText;
    
    contentWrap.appendChild(title);
    contentWrap.appendChild(desc);

    // 3단계: 개별 삭제 버튼 동적 생성 및 이벤트 연결
    const deleteBtn = document.createElement("button");
    deleteBtn.className = "btn-delete-item";
    deleteBtn.textContent = "지우기";
    
    // 버튼 클릭 시 돔 탐색 없이 생성된 클로저를 활용해 자기 자신 노드를 즉시 소멸(remove)
    deleteBtn.addEventListener("click", () => {
      noticeItem.remove();
      console.log(`[알림 소멸] ID: ${noticeItem.id}가 물리적으로 화면에서 완전 제거되었습니다.`);
    });

    noticeItem.appendChild(contentWrap);
    noticeItem.appendChild(deleteBtn);

    return noticeItem;
  };

  // 2-A. 상단 최신 알림 추가 (prepend)
  document.getElementById("btn-prepend-notice")?.addEventListener("click", () => {
    noticeCount++;
    const newAlert = createNoticeElement(
      `[최신 공지] 중요 시스템 알림 (${noticeCount}호)`,
      `실시간 동적 prepend API 작동 검증 완료 (맨 위에 끼워 넣습니다.)`
    );
    
    // prepend를 사용하여 최신 공지를 컨테이너의 가장 맨 앞 노드로 주입
    noticeContainer.prepend(newAlert);
  });

  // 2-B. 하단 이전 알림 추가 (append/appendChild)
  document.getElementById("btn-append-notice")?.addEventListener("click", () => {
    noticeCount++;
    const oldAlert = createNoticeElement(
      `[이전 이력] 과거 로그 데이터 (${noticeCount}호)`,
      `실시간 동적 append API 작동 검증 완료 (맨 마지막 자식으로 덧붙입니다.)`
    );
    
    // append를 사용하여 맨 마지막 하단 자식 노드로 주입
    noticeContainer.append(oldAlert);
  });

  // 2-C. 모든 알림 일괄 소멸
  document.getElementById("btn-clear-notice")?.addEventListener("click", () => {
    noticeContainer.innerHTML = "";
    noticeCount = 0;
    console.log("알림 센터의 모든 노드가 소멸되었습니다.");
  });

  // --------------------------------------------------------------------------
  // [3] DocumentFragment 성능 최적화
  // --------------------------------------------------------------------------
  const dummyProductData = [
    { title: "에스테틱 재킷", brand: "ClassicFit" },
    { title: "슬림 코튼 카고", brand: "UrbanLook" },
    { title: "오버핏 맨투맨", brand: "DailyBasic" },
    { title: "레더 첼시 부츠", brand: "ClassicFit" },
    { title: "데일리 에코백", brand: "DailyBasic" }
  ];

  // 3-A. 최적화 버퍼(DocumentFragment)를 이용한 대량 렌더링
  document.getElementById("btn-render-fragment")?.addEventListener("click", () => {
    fragmentContainer.innerHTML = "";

    // 1단계: 브라우저 돔 외부 메모리에 존재하는 가상 경량 버퍼 보관함 생성
    const bufferFragment = document.createDocumentFragment();

    // 2단계: 다량의 루프를 돌며 카드를 버퍼에 축적 (리플로우 발생 0회)
    dummyProductData.forEach(({ title, brand }) => {
      const card = document.createElement("div");
      card.className = "fragment-card";
      
      const cardTitle = document.createElement("h4");
      cardTitle.style.margin = "0 0 5px 0";
      cardTitle.textContent = title;
      
      const cardBrand = document.createElement("small");
      cardBrand.style.color = "#4361ee";
      cardBrand.textContent = brand;
      
      card.appendChild(cardTitle);
      card.appendChild(cardBrand);

      // 브라우저 DOM이 아닌 가상의 fragment 보관함에 주입
      bufferFragment.appendChild(card);
    });

    // 3단계: 단 1회의 appendChild 호출로 버퍼 내부의 모든 노드 다발을 실 돔에 장착 (리플로우 단 1회 발생)
    fragmentContainer.appendChild(bufferFragment);
    console.log("DocumentFragment 버퍼를 활용해 리플로우 부하를 1회로 제한하여 안전하게 카드 렌더링을 마쳤습니다.");
  });

  // 3-B. 그리드 초기화
  document.getElementById("btn-clear-grid")?.addEventListener("click", () => {
    fragmentContainer.innerHTML = "";
  });
});
