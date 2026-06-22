/**
 * ==========================================================================
 실습: Fetch API 기초 및 REST GET 요청 (main_04.js)
 * 학습 주제: Fetch API 기본 구조, response.json() 언박싱, 이벤트 위임 적용
 * ==========================================================================
 */

document.addEventListener("DOMContentLoaded", () => {
  console.log("[실습] Fetch API 기초 스크립트 가동.");

  // 0. 다크모드 시스템 활성화
  initDarkMode();

  // 1. Fetch API GET 조회 모듈 활성화 (이벤트 위임 기법 탑재)
  initFetchGetModule();
});

/**
 * 0. 2일차 연계: 다크모드 컨트롤 시스템
 */
function initDarkMode() {
  const wrapper = document.getElementById("theme-control-wrapper");
  if (!wrapper) return;

  const modeBtn = document.createElement("button");
  modeBtn.id = "dark-mode-toggle";
  modeBtn.className = "btn-action btn-secondary";
  modeBtn.style.padding = "6px 12px";
  modeBtn.style.fontSize = "0.85rem";
  modeBtn.textContent = "테마: 라이트모드";

  wrapper.appendChild(modeBtn);

  modeBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    const isDark = document.body.classList.contains("dark-mode");
    modeBtn.textContent = isDark ? "테마: 다크모드" : "테마: 라이트모드";
    console.log(`[DarkMode] 테마 전환 완료. 다크 상태 활성화: ${isDark}`);
  });
}

/**
 * 1. Fetch API GET 조회 모듈 (이벤트 위임 및 로컬 FastAPI 연동)
 */
function initFetchGetModule() {
  const listContainer = document.getElementById("user-list-container");
  const resetBtn = document.getElementById("btn-reset-card");
  const overlay = document.getElementById("loading-overlay");
  const term = document.getElementById("term-raw-json");

  // 카드 UI 요소들
  const avatar = document.getElementById("user-avatar");
  const name = document.getElementById("user-name");
  const username = document.getElementById("user-username");
  const email = document.getElementById("user-email");
  const phone = document.getElementById("user-phone");
  const company = document.getElementById("user-company");
  const website = document.getElementById("user-website");

  if (!listContainer || !resetBtn || !overlay || !term || !avatar || !name || !username || !email || !phone || !company || !website) return;

  // 카드 UI 초기화 함수
  const resetProfileCard = () => {
    avatar.textContent = "?";
    name.textContent = "조회 전";
    username.textContent = "username: N/A";
    email.textContent = "조회되지 않음";
    phone.textContent = "조회되지 않음";
    company.textContent = "조회되지 않음";
    website.textContent = "조회되지 않음";
    term.textContent = "서버가 응답한 배달 상자(Raw JSON)의 원시 텍스트가 여기에 개봉 정렬되어 표시됩니다.";
    console.log("[Fetch API] 프로필 카드가 기본 상태로 초기화되었습니다.");
  };

  resetBtn.addEventListener("click", resetProfileCard);

  // 단일 사용자 정보를 비동기 조회해오는 핵심 비동기 함수 (Fetch API)
  const fetchSingleUser = (userId) => {
    // 1. UI 대기 상태 및 오버레이 스피너 켜기 (비동기 지연 대기 연출)
    overlay.classList.add("active");
    term.textContent = `1. 배달원(Fetch)이 로컬 백엔드 서버(port 8000)로 ${userId}번 사용자 조회를 요청하러 출발했습니다...`;

    console.log("==================================================");
    console.log(`Fetch API GET 요청 시작: /users/${userId}`);
    console.log("==================================================");

    // SQLite3 DB 백엔드 서버의 GET 엔드포인트 호출
    fetch(`http://127.0.0.1:8000/api/users/${userId}`)
      .then((response) => {
        // 2. 서버 응답 수신 완료 (배달 박스 도달)
        term.textContent += "\n2. 배달원이 주방(FastAPI)에서 밀봉된 배달 상자(Response)를 가지고 브라우저에 도착했습니다.";
        console.log("Fetch Step 1: 서버로부터 HTTP 응답 헤더 수신 완료. Status:", response.status);

        if (!response.ok) {
          throw new Error(`서버 응답 오류 (HTTP Status: ${response.status})`);
        }

        // 3. JSON 규격으로 밀봉된 텍스트 상자를 자바스크립트 객체로 개봉 요청
        term.textContent += "\n3. 밀봉된 JSON 배달 상자를 객체로 개봉(response.json())하여 데이터를 획득 중입니다...";
        return response.json();
      })
      .then((user) => {
        // 4. 개봉이 완료되어 실물 데이터를 획득한 시점
        term.textContent += "\n4. 개봉 완료! 원시 JSON 텍스트와 가공된 자바스크립트 객체를 렌더링합니다.\n\n[수신된 배달 상자 원본 (Raw JSON)]\n";
        
        // 날것의 JSON 문자열 정렬하여 터미널에 출력
        term.textContent += JSON.stringify(user, null, 2);
        

        // 5. 단일 유저 데이터를 프로필 카드의 각 영역에 정직하게 일대일 대입
        avatar.textContent = user.name[0]; // 이름의 첫 글자
        name.textContent = user.name;
        username.textContent = `username: ${user.username}`;
        email.textContent = user.email;
        phone.textContent = user.phone;
        company.textContent = user.company.name;
        website.textContent = user.website;

        console.log(`Fetch Step 2: ${userId}번 사용자 카드 바인딩 성공.`);
      })
      .catch((error) => {
        // 네트워크 연결 두절 등 예외 발생 시 포착
        term.innerHTML = `\n[배달 사고 발생] 통신에 실패했습니다.\n오류 원인: ${error.message}`;
        console.error("Fetch Error:", error.message);
      })
      .finally(() => {
        // 성공하든 실패하든 상관없이 비동기 오버레이 스피너 제거
        overlay.classList.remove("active");
        term.textContent += "\n\n5. [.finally()] 배달 프로세스가 종료되어 대기 화면이 해제되었습니다.";
      });
  };

  // 2일차 복습: 부모 컨테이너에 단 하나의 리스너를 장착하여 자식 클릭을 처리하는 이벤트 위임(Event Delegation) 기법 적용
  listContainer.addEventListener("click", (e) => {
    // 클릭된 타겟이 'user-item-btn' 클래스를 포함하는지 검출
    const targetBtn = e.target.closest(".user-item-btn");
    if (!targetBtn) return;

    // 해당 버튼의 HTML data-id 속성 값을 추출
    const userId = targetBtn.getAttribute("data-id");
    if (userId) {
      fetchSingleUser(userId);
    }
  });
}
