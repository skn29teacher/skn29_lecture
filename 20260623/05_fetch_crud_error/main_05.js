/**
 * ==========================================================================
 * Fetch API 심화 - CRUD 및 예외 처리 (main_05.js)
 * 학습 주제: Fetch API의 POST/PUT/DELETE 옵션 설정, response.ok 예외 처리, 이벤트 위임 및 전파 방지 복습
 * ==========================================================================
 */

document.addEventListener("DOMContentLoaded", () => {
  console.log("[실습] Fetch API CRUD 및 에러 처리 스크립트 가동.");

  // 0. 다크모드 시스템 활성화
  initDarkMode();

  // 1. Fetch CRUD 및 에러 처리 모듈 활성화
  initFetchCrudModule();
});

/**
 * 0. 다크모드 컨트롤 시스템
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
 * 1. Fetch CRUD 및 에러 처리 모듈
 */
function initFetchCrudModule() {
  const guestbookForm = document.getElementById("guestbook-form");
  const guestbookList = document.getElementById("guestbook-list");
  const nameInput = document.getElementById("txt-guest-name");
  const contentInput = document.getElementById("txt-guest-content");
  const spinner = document.getElementById("crud-loading-spinner");
  const alertBanner = document.getElementById("error-alert-banner");
  const termResult = document.getElementById("term-crud-result");

  const btn404 = document.getElementById("btn-err-404");
  const btn500 = document.getElementById("btn-err-500");

  if (!guestbookForm || !guestbookList || !nameInput || !contentInput || !spinner || !alertBanner || !termResult || !btn404 || !btn500) {
    console.warn("[경고] 필요한 HTML 요소를 찾을 수 없습니다.");
    return;
  }

  // API 서버 베이스 URL
  const API_URL = "http://127.0.0.1:8000/api/posts";

  // 로딩 인디케이터 스위치
  const setRunning = (isRunning) => {
    if (isRunning) {
      spinner.style.display = "inline-block";
      alertBanner.style.display = "none";
    } else {
      spinner.style.display = "none";
    }
  };

  // 에러 리포팅 헬퍼
  const handleError = (error, context) => {
    alertBanner.style.display = "block";
    alertBanner.textContent = `[에러 발생 - ${context}] ${error.message}`;
    termResult.textContent = `[실패 로그 - ${context}]\n- 에러 메시지: ${error.message}\n- 상세: API 요청 중 오류가 검출되었습니다.`;
  };

  // ==========================================================================
  // [조회: GET] 방명록 전체 리스트 로드
  // ==========================================================================
  const loadGuestbook = () => {
    setRunning(true);
    fetch(API_URL)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`목록 조회 실패 (HTTP 상태코드: ${response.status})`);
        }
        return response.json();
      })
      .then((posts) => {
        guestbookList.innerHTML = "";

        if (posts.length === 0) {
          guestbookList.innerHTML = `<li style="text-align: center; padding: 20px; color: #868e96; font-size: 0.9rem;">등록된 방명록 글이 없습니다. 첫 글을 작성해 보세요.</li>`;
          return;
        }

        posts.forEach((post) => {
          const li = document.createElement("li");
          li.className = "guest-item";
          li.setAttribute("data-id", post.id);
          // 텍스트 수정을 용이하게 하기 위한 data 속성 보관
          li.setAttribute("data-title", post.title);
          li.setAttribute("data-body", post.body);

          li.innerHTML = `
            <div class="guest-content-wrapper">
              <div class="guest-text">${escapeHtml(post.body)}</div>
              <div class="guest-author">작성자: ${escapeHtml(post.title)}</div>
            </div>
            <div class="guest-actions">
              <button class="btn-sm btn-warning btn-edit-toggle">수정</button>
              <button class="btn-sm btn-danger btn-delete">삭제</button>
            </div>
          `;
          guestbookList.appendChild(li);
        });

        termResult.textContent = `[GET 요청 성공] 방명록 목록(${posts.length}건) 로드 완료.\n- 주소: ${API_URL}`;
      })
      .catch((error) => handleError(error, "GET"))
      .finally(() => setRunning(false));
  };

  // HTML 이스케이프 유틸리티 (XSS 방지)
  const escapeHtml = (text) => {
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  };

  // ==========================================================================
  // [등록: POST] 방명록 글쓰기
  // ==========================================================================
  guestbookForm.addEventListener("submit", (e) => {
    e.preventDefault(); // 2일차 복습: 폼 제출 시 새로고침 방지

    const nameValue = nameInput.value.trim();
    const contentValue = contentInput.value.trim();

    if (!nameValue || !contentValue) {
      alert("작성자와 내용을 모두 입력해주세요.");
      return;
    }

    setRunning(true);

    fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        title: nameValue,
        body: contentValue
      })
    })
      .then((response) => {
        if (!response.ok) {
          // FastAPI에서 400 에러 등을 반환할 때의 세부 메시지를 받기 위해 처리
          return response.json().then((errData) => {
            throw new Error(errData.detail || `방명록 등록 실패 (HTTP ${response.status})`);
          });
        }
        return response.json();
      })
      .then((newPost) => {
        termResult.textContent = `[POST 요청 성공] 신규 방명록이 등록되었습니다.\n` +
          `- ID: ${newPost.id}\n` +
          `- 작성자: ${newPost.title}\n` +
          `- 내용: ${newPost.body}`;
        
        // 입력 필드 초기화
        contentInput.value = "";
        
        // 리스트 새로고침
        loadGuestbook();
      })
      .catch((error) => handleError(error, "POST"))
      .finally(() => setRunning(false));
  });

  // ==========================================================================
  // [이벤트 위임 & 수정/삭제 & 버블링 제어]
  // ==========================================================================
  guestbookList.addEventListener("click", (e) => {
    const target = e.target;
    const li = target.closest(".guest-item");
    if (!li) return;

    const postId = li.getAttribute("data-id");
    const origTitle = li.getAttribute("data-title");
    const origBody = li.getAttribute("data-body");

    // 1) 삭제 버튼 클릭 시 (DELETE)
    if (target.classList.contains("btn-delete")) {
      e.stopPropagation(); // 2일차 복습: 부모 li 클릭(아이템 선택) 버블링 전파 차단

      if (!confirm(`정말 ${origTitle}님의 글을 삭제하시겠습니까?`)) return;

      setRunning(true);
      fetch(`${API_URL}/${postId}`, {
        method: "DELETE"
      })
        .then((response) => {
          if (!response.ok) {
            return response.json().then((errData) => {
              throw new Error(errData.detail || `삭제 실패 (HTTP ${response.status})`);
            });
          }
          return response.json();
        })
        .then((data) => {
          termResult.textContent = `[DELETE 요청 성공] 방명록 글이 삭제되었습니다.\n- 삭제된 ID: ${postId}`;
          loadGuestbook();
        })
        .catch((error) => handleError(error, "DELETE"))
        .finally(() => setRunning(false));
      return;
    }

    // 2) 수정 모드 토글 클릭 시
    if (target.classList.contains("btn-edit-toggle")) {
      e.stopPropagation(); // 2일차 복습: 행 선택 버블링 차단

      // 인라인 수정 입력 폼으로 치환
      const wrapper = li.querySelector(".guest-content-wrapper");
      const actions = li.querySelector(".guest-actions");

      wrapper.innerHTML = `
        <input type="text" class="inline-edit-input edit-title" value="${escapeHtml(origTitle)}" placeholder="작성자명">
        <input type="text" class="inline-edit-input edit-body" value="${escapeHtml(origBody)}" placeholder="내용">
      `;

      actions.innerHTML = `
        <button class="btn-sm btn-success btn-edit-save">저장</button>
        <button class="btn-sm btn-secondary btn-edit-cancel">취소</button>
      `;
      return;
    }

    // 3) 수정 취소 클릭 시
    if (target.classList.contains("btn-edit-cancel")) {
      e.stopPropagation(); // 2일차 복습: 행 선택 버블링 차단
      // 리스트를 다시 그려서 복원
      loadGuestbook();
      return;
    }

    // 4) 수정 저장 클릭 시 (PUT)
    if (target.classList.contains("btn-edit-save")) {
      e.stopPropagation(); // 2일차 복습: 행 선택 버블링 차단

      const editTitle = li.querySelector(".edit-title").value.trim();
      const editBody = li.querySelector(".edit-body").value.trim();

      if (!editTitle || !editBody) {
        alert("수정할 이름과 내용을 모두 채워주세요.");
        return;
      }

      setRunning(true);
      fetch(`${API_URL}/${postId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          title: editTitle,
          body: editBody
        })
      })
        .then((response) => {
          if (!response.ok) {
            return response.json().then((errData) => {
              throw new Error(errData.detail || `수정 실패 (HTTP ${response.status})`);
            });
          }
          return response.json();
        })
        .then((updatedPost) => {
          termResult.textContent = `[PUT 요청 성공] 방명록 글이 수정되었습니다.\n` +
            `- ID: ${updatedPost.id}\n` +
            `- 수정 작성자: ${updatedPost.title}\n` +
            `- 수정 내용: ${updatedPost.body}`;
          loadGuestbook();
        })
        .catch((error) => handleError(error, "PUT"))
        .finally(() => setRunning(false));
      return;
    }

    // 5) 아이템(li) 자체 클릭 시 -> 행 선택 스타일 토글 (2일차 버블링 활용 복습)
    // 버튼들이 아닌 빈 li 영역을 클릭하면 정상적으로 이곳으로 도달합니다.
    const isSelected = li.classList.contains("selected");
    
    // 다른 모든 리스트 아이템의 선택 상태를 걷어냄
    const allItems = guestbookList.querySelectorAll(".guest-item");
    allItems.forEach(item => item.classList.remove("selected"));

    if (!isSelected) {
      li.classList.add("selected");
      termResult.textContent = `[이벤트 버블링 수신] 리스트 행 클릭 감지.\n- 선택된 ID: ${postId}\n- 작성자: ${origTitle}\n- 내용: ${origBody}`;
    } else {
      termResult.textContent = "리스트 행 선택 해제.";
    }
  });

  // ==========================================================================
  // 404 & 500 강제 에러 테스트
  // ==========================================================================
  btn404.addEventListener("click", () => {
    setRunning(true);
    fetch("http://127.0.0.1:8000/api/invalid-route-for-testing-404")
      .then((response) => {
        if (!response.ok) {
          throw new Error(`요청 리소스를 찾을 수 없습니다. (HTTP 상태코드: ${response.status})`);
        }
        return response.json();
      })
      .then((data) => {
        termResult.textContent = JSON.stringify(data);
      })
      .catch((error) => handleError(error, "404 TEST"))
      .finally(() => setRunning(false));
  });

  btn500.addEventListener("click", () => {
    setRunning(true);
    fetch("http://127.0.0.1:8000/api/error/500")
      .then((response) => {
        if (!response.ok) {
          throw new Error(`서버 내부 치명적인 오류가 강제되었습니다. (HTTP 상태코드: ${response.status})`);
        }
        return response.json();
      })
      .then((data) => {
        termResult.textContent = JSON.stringify(data);
      })
      .catch((error) => handleError(error, "500 TEST"))
      .finally(() => setRunning(false));
  });

  // 최초 구동 시 방명록 데이터 로딩
  loadGuestbook();
}

