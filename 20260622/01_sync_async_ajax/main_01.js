/**
 * ==========================================================================
 * 3일차 1차시 실습: 동기 vs 비동기 및 AJAX 역사 (main_01.js)
 * 학습 주제: 동기/비동기 블로킹 체험, 이벤트 루프 스케줄링, XHR readyState 라이프사이클, 콜백 지옥 실태
 * ==========================================================================
 */

document.addEventListener("DOMContentLoaded", () => {
  console.log("[실습] 자바스크립트 가동 시작.");

  // --------------------------------------------------------------------------
  // 0. 2일차 연계: 다크모드 스위칭 시스템 탑재
  // --------------------------------------------------------------------------
  initDarkMode();

  // --------------------------------------------------------------------------
  // 1. 동기(Synchronous) vs 비동기(Asynchronous) 확인
  // --------------------------------------------------------------------------
  initSyncAsyncModule();

  // --------------------------------------------------------------------------
  // 2. 자바스크립트 엔진과 브라우저 이벤트 루프 (Event Loop) 순서 확인
  // --------------------------------------------------------------------------
  initEventLoopModule();

  // --------------------------------------------------------------------------
  // 3. XMLHttpRequest (XHR) readyState 및 통신 확인
  // --------------------------------------------------------------------------
  initXHRRequestModule();

  // --------------------------------------------------------------------------
  // 4. 콜백 지옥 (Callback Hell) 패턴 확인
  // --------------------------------------------------------------------------
  initCallbackHellModule();
});

/**
 * 2일차 테마 설정을 연계한 다크모드 모듈
 */
function initDarkMode() {
  const wrapper = document.getElementById("theme-control-wrapper");
  if (!wrapper) return;

  const modeBtn = document.createElement("button");
  modeBtn.id = "dark-mode-toggle";
  modeBtn.className = "btn-action btn-outline";
  modeBtn.style.padding = "6px 12px";
  modeBtn.style.fontSize = "0.85rem";
  modeBtn.style.border = "1px solid #ced4da";
  modeBtn.style.backgroundColor = "transparent";
  modeBtn.style.color = "#495057";
  modeBtn.textContent = "테마: 라이트모드";

  wrapper.appendChild(modeBtn);

  modeBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    const isDark = document.body.classList.contains("dark-mode");
    modeBtn.textContent = isDark ? "테마: 다크모드" : "테마: 라이트모드";
    modeBtn.style.borderColor = isDark ? "#adb5bd" : "#ced4da";
    modeBtn.style.color = isDark ? "#f8f9fa" : "#495057";
    console.log(`[DarkMode] 테마 스위칭 작동. 다크 상태: ${isDark}`);
  });
}

/**
 * 1. 동기 vs 비동기 블로킹/논블로킹 확인
 */
function initSyncAsyncModule() {
  const btnSync = document.getElementById("btn-sync-blocking");
  const btnAsync = document.getElementById("btn-async-nonblocking");
  const term = document.getElementById("term-sync-async");
  
  // UI 반응성 테스트용 요소들
  const btnInteract = document.getElementById("btn-interactive-click");
  const inputInteract = document.getElementById("input-interactive-text");
  const chkStopPropagation = document.getElementById("chk-stop-propagation");

  if (!btnSync || !btnAsync || !term || !btnInteract || !inputInteract || !chkStopPropagation) return;

  // 카운터 변수
  let clickCount = 0;

  // 카운트 버튼 클릭 이벤트 (반응성 체크용 + 2일차 버블링 제어 복습)
  btnInteract.addEventListener("click", (e) => {
    clickCount++;
    btnInteract.textContent = `이 버튼을 클릭해 보세요 (클릭 횟수: ${clickCount})`;
    
    term.textContent = `[Target Clicked] 버튼 이벤트 발생. e.target.id: ${e.target.id}\n`;
    
    // 체크박스 유무에 따른 버블링(전파) 차단 여부 결정
    if (chkStopPropagation.checked) {
      e.stopPropagation();
      term.textContent += `-> [e.stopPropagation() 실행] 이벤트 전파를 차단하여 부모 카드로 올라가지 않습니다.`;
    } else {
      term.textContent += `-> 이벤트 버블링 발생 대기 중...`;
    }
  });

  // 부모 카드 엘리먼트에 버블링 리스너를 달아 전파 확인
  const parentCard = btnInteract.closest(".section-card");
  if (parentCard) {
    parentCard.addEventListener("click", (e) => {
      term.textContent += `\n[Bubbling Detected] 부모 카드가 이벤트를 수신했습니다! (e.currentTarget.className: ${e.currentTarget.className.split(" ")[0]}, e.target.id: ${e.target.id})`;
    });
  }

  // 동기식 강제 대기(Busy-Waiting) 함수
  // 지정된 밀리초(ms) 시간 동안 메인 스레드를 100% 잡아두어 완벽한 블로킹을 구현합니다.
  const syncDelay = (ms) => {
    const start = Date.now();
    while (Date.now() - start < ms) {
      // 지정 시간 동안 아무것도 하지 않고 루프를 돌며 호출 스택을 영구 독점
    }
  };

  // 동기 블로킹 연산 수행
  btnSync.addEventListener("click", (e) => {
    // 동기 버튼 자체의 클릭 이벤트가 부모로 버블링되는 것을 막아 터미널 혼선 방지
    e.stopPropagation();
    term.textContent = "동기식 데이터 대기(3초)를 시작합니다. 지금 즉시 위의 녹색 버튼을 마구 클릭하고 입력창에 글자를 쳐 보세요...";
    
    // 버튼 텍스트 변경이 화면에 반영될 수 있도록 짧은 지연시간(50ms) 후 동기 작업 시작
    setTimeout(() => {
      const startTime = performance.now();
      
      // 강제로 3초 동안 호출 스택을 100% 블로킹 상태로 점유
      syncDelay(3000);
      
      const endTime = performance.now();
      const duration = ((endTime - startTime) / 1000).toFixed(2);
      
      term.innerHTML = `
[동기 대기 종료 결과]
- 동기식 가상 딜레이 강제 점유 성공
- 총 블로킹 시간: ${duration}초
- 상태: 서버의 응답을 기다리는 동안 동기식으로 대기했습니다. 이 과정에서 브라우저 메인 스레드가 3초 동안 완전히 마비(프리징)되어, 녹색 카운트 버튼 클릭이나 키보드 입력이 일절 화면에 처리되지 못하고 얼어붙었습니다. (대기 해제 후 밀렸던 동작이 순식간에 반영됩니다.)
      `;
    }, 50);
  });

  // 비동기 논블로킹 연산 수행
  btnAsync.addEventListener("click", () => {
    term.innerHTML = `
[비동기 대기 시작]
- 3초 뒤에 완료되는 비동기 타이머(setTimeout)를 Web API에 요청했습니다.
- 상태: 현재 백그라운드에서 지연 대기 중이며, 메인 스레드가 즉시 풀려나 논블로킹 상태입니다. 지금 녹색 카운트 버튼을 누르거나 텍스트창에 타이핑을 해보세요. 화면 지연 없이 실시간으로 원활히 작동합니다.
    `;

    setTimeout(() => {
      term.innerHTML += `
\n[비동기 대기 종료 완료]
- 3초가 지난 뒤 Task Queue에 쌓였던 콜백 함수가 성공적으로 호출 스택에 올라와 수행되었습니다!
      `;
    }, 3000);
  });
}

/**
 * 2. 자바스크립트 엔진과 브라우저 이벤트 루프(Event Loop) 순서 확인
 */
function initEventLoopModule() {
  const btnLoopSync = document.getElementById("btn-loop-sync");
  const btnLoopAsync = document.getElementById("btn-loop-async");
  const term = document.getElementById("term-event-loop");
  const progressBar = document.getElementById("loop-progress-bar");

  if (!btnLoopSync || !btnLoopAsync || !term || !progressBar) return;

  // 가상의 대용량 연산 횟수 (3천만 번)
  const totalIterations = 30000000;

  // 동기식 일괄 연산 처리
  btnLoopSync.addEventListener("click", () => {
    btnLoopSync.disabled = true;
    btnLoopAsync.disabled = true;
    progressBar.style.width = "0%";
    progressBar.textContent = "0%";
    term.textContent = "동기식 대용량 일괄 처리를 수행 중입니다. 화면 게이지가 멈춰 있는 동안 다크모드를 눌러 화면 반응성을 테스트해 보세요...";

    // 버튼 눌림 피드백이 화면에 렌더링되도록 50ms 후 연산 작동
    setTimeout(() => {
      const startTime = performance.now();
      let sum = 0;

      // 3천만 번의 삼각함수 루프 연산을 호출 스택에 한 번에 몰아서 실행
      for (let i = 0; i < totalIterations; i++) {
        sum += Math.sin(i) * Math.cos(i);

        // 연산 도중에 게이지의 DOM 변경을 시도하지만,
        // 동기식 스레드가 독점되어 화면 갱신(렌더링) 처리가 차단당합니다.
        if (i % 3000000 === 0) {
          const pct = Math.floor((i / totalIterations) * 100);
          progressBar.style.width = `${pct}%`;
          progressBar.textContent = `${pct}%`;
        }
      }

      progressBar.style.width = "100%";
      progressBar.textContent = "100%";

      const endTime = performance.now();
      const duration = ((endTime - startTime) / 1000).toFixed(2);

      term.innerHTML = `
[동기식 일괄 연산 종료 결과]
- 총 연산 소요 시간: ${duration}초
- 상태: 동일한 3천만 번 연산을 호출 스택(Call Stack)에 한 방에 쌓아 실행했기 때문에, 연산 도중에 발생한 게이지 갱신 렌더링 요청들이 모두 블로킹되었습니다. 이에 따라 0%에서 게이지가 멈춰 있다가 연산이 다 끝난 뒤에야 갑자기 100%로 순간이동하듯 표기되었습니다.
      `;

      btnLoopSync.disabled = false;
      btnLoopAsync.disabled = false;
    }, 50);
  });

  // 이벤트 루프 활용 분할 연산 처리 (Chunking 기법)
  btnLoopAsync.addEventListener("click", () => {
    btnLoopSync.disabled = true;
    btnLoopAsync.disabled = true;
    progressBar.style.width = "0%";
    progressBar.textContent = "0%";
    term.textContent = "이벤트 루프 분할 처리를 시작합니다. 로딩 게이지가 실시간으로 부드럽게 상승합니다...";

    const startTime = performance.now();
    const chunkSize = 1000000; // 3천만 번 연산을 100만 번씩 30조각으로 분할
    let currentIteration = 0;
    let sum = 0;

    const processChunk = () => {
      const limit = Math.min(currentIteration + chunkSize, totalIterations);
      
      // 100만 번의 연산 조각 수행
      for (let i = currentIteration; i < limit; i++) {
        sum += Math.sin(i) * Math.cos(i);
      }
      
      currentIteration = limit;

      // 100만 번 끝날 때마다 진행도 화면 렌더링 요청
      const pct = Math.floor((currentIteration / totalIterations) * 100);
      progressBar.style.width = `${pct}%`;
      progressBar.textContent = `${pct}%`;

      if (currentIteration < totalIterations) {
        // 남은 작업을 setTimeout(..., 0)을 통해 이벤트 루프의 Task Queue 뒤로 양보!
        // 이로 인해 호출 스택이 비워지는 짧은 찰나에 브라우저는 게이지바의 렌더링을 성공시키고
        // 사용자의 클릭이나 다크모드 입력을 처리해 렉을 없앱니다.
        setTimeout(processChunk, 0);
      } else {
        const endTime = performance.now();
        const duration = ((endTime - startTime) / 1000).toFixed(2);

        term.innerHTML = `
[이벤트 루프 분할 연산 종료 결과]
- 총 연산 소요 시간: ${duration}초
- 상태: 동일한 3천만 번 연산이지만, 100만 번씩 잘게 쪼개어 다음 연산 조각을 setTimeout(..., 0)으로 루프 뒤에 안착시켰습니다. 덕분에 엔진이 100만 번 계산을 완료하는 즉시 스레드 사용권을 브라우저에 양보하여, 게이지가 실시간으로 부드럽게 차오르고 화면 테마 버튼도 딜레이 없이 완전 정상 작동했습니다.
        `;

        btnLoopSync.disabled = false;
        btnLoopAsync.disabled = false;
      }
    };

    // 첫 번째 조각 실행 시작
    processChunk();
  });
}

/**
 * 3. XMLHttpRequest (XHR) readyState 및 통신 확인
 */
function initXHRRequestModule() {
  const btnXHR = document.getElementById("btn-xhr-request");
  const term = document.getElementById("term-xhr");

  if (!btnXHR || !term) return;

  const getReadyStateName = (state) => {
    switch (state) {
      case 0: return "0: UNSENT (편지 작성 준비 단계 - XHR 객체만 생성된 상태)";
      case 1: return "1: OPENED (우체국 접수 단계 - open() 호출로 서버 연결 정보가 설정된 상태)";
      case 2: return "2: HEADERS_RECEIVED (상대방 도착 및 영수증 회신 단계 - 서버가 요청 접수 신호를 돌려준 상태)";
      case 3: return "3: LOADING (짐 내리기 단계 - 본문 데이터를 실제로 패킷 단위 다운로드하는 상태)";
      case 4: return "4: DONE (편지 개봉 단계 - 다운로드가 안전하게 완료되어 자바스크립트로 가공 가능한 상태)";
      default: return `${state}: UNKNOWN`;
    }
  };

  // LED 스타일 램프 초기화 및 업데이트 함수
  const updateLEDs = (state, isFinished = false) => {
    for (let i = 0; i <= 4; i++) {
      const led = document.getElementById(`xhr-led-${i}`);
      if (!led) continue;
      
      led.classList.remove("active", "success");
      
      if (i === state) {
        if (isFinished) {
          led.classList.add("success");
        } else {
          led.classList.add("active");
        }
      }
    }
  };

  btnXHR.addEventListener("click", () => {
    term.textContent = "[XHR 통신 시작]\n";
    btnXHR.disabled = true;
    
    // LED 램프 전부 대기 상태로 초기화
    for (let i = 0; i <= 4; i++) {
      document.getElementById(`xhr-led-${i}`)?.classList.remove("active", "success");
    }

    // readyState 수집을 위한 가상 시각화 큐
    const visualQueue = [];

    const pushToVisualQueue = (state, statusText = "-") => {
      // 큐 내부에 중복된 readyState 정보가 쌓이지 않도록 단일 적재 제어
      if (!visualQueue.some(item => item.state === state)) {
        visualQueue.push({ state, statusText });
      }
    };

    // [1단계: 0번 상태 유발] XHR 인스턴스 생성 (우편 배달 비유: 편지 작성 준비)
    const xhr = new XMLHttpRequest();
    pushToVisualQueue(0);

    // [2단계: 1번 상태 유발] open() 호출 (우편 배달 비유: 우체국에 발송 접수)
    // 로컬 백엔드 서버(FastAPI) 포트 8000번 호출
    xhr.open("GET", "http://127.0.0.1:8000/api/users/1", true);
    pushToVisualQueue(1);

    // [3단계] 상태 변화 감지 리스너 바인딩 (이 리스너 안에서 readyState 2, 3, 4가 비동기적으로 잡힙니다)
    xhr.onreadystatechange = () => {
      const state = xhr.readyState;
      const statusText = xhr.status || "-";
      
      // readyState 2, 3, 4 상태를 수집 큐에 차례대로 푸시
      pushToVisualQueue(state, statusText);

      // 통신 최종 완료 시점에 모아진 모든 과정(0~4)을 0.8초 간격으로 시각 재생 시뮬레이션
      if (state === 4) {
        playVisualQueue(visualQueue, xhr);
      }
    };

    // [4단계: 발송 트리거] send() 호출하여 실제 네트워크 전송 시작
    xhr.send();

    // [5단계: 비동기성 즉시 확인]
    term.textContent += "[호출 스택 완료] xhr.send() 발송 즉시 제어권이 반환되었습니다. 이 아래의 동기 코드가 먼저 실행됩니다!\n";
    console.log("[XHR 비동기 확인] send() 호출 직후 제어권 반환 완료.");
  });

  // 수집된 라이프사이클을 0.8초 간격으로 천천히 재생하여 눈으로 확인하게 하는 핵심 엔진
  const playVisualQueue = (queue, xhrInstance) => {
    let index = 0;

    const renderNextState = () => {
      if (index >= queue.length) {
        btnXHR.disabled = false;
        
        if (xhrInstance.status === 200) {
          try {
            const data = JSON.parse(xhrInstance.responseText);
            term.textContent += `
\n[수신 성공 및 JSON 파싱 결과]
- 이름: ${data.name}
- 이메일: ${data.email}
- 소속 회사: ${data.company.name}
- 결론: XHR 통신은 이처럼 readyState 변화를 직접 관리해야 하여 코드가 장황하고 복잡합니다.
            `;
          } catch (e) {
            term.textContent += `\n[에러] JSON 파싱 중 문제 발생: ${e.message}`;
          }
        } else {
          term.textContent += `\n[오류] HTTP 통신 상태 코드가 에러를 지칭합니다: ${xhrInstance.status}`;
        }
        return;
      }

      const { state, statusText } = queue[index];
      const isLast = (state === 4 && xhrInstance.status === 200);

      // LED 램프 업데이트 및 터미널 한 줄씩 누적 출력
      updateLEDs(state, isLast);
      term.textContent += `[State] ${getReadyStateName(state)} (HTTP Status: ${statusText})\n`;

      index++;
      setTimeout(renderNextState, 800);
    };

    renderNextState();
  };
}

/**
 * 4. 콜백 지옥 (Callback Hell) 패턴 확인
 */
function initCallbackHellModule() {
  const btnCallback = document.getElementById("btn-callback-hell");
  const term = document.getElementById("term-callback");

  // 시각화 카드 목록
  const card1 = document.getElementById("cb-card-1");
  const card2 = document.getElementById("cb-card-2");
  const card3 = document.getElementById("cb-card-3");

  if (!btnCallback || !term || !card1 || !card2 || !card3) return;

  const updateCardState = (card, state, text) => {
    card.className = "cb-step-card"; // 기본 클래스
    card.classList.add(state);
    const statusTextEl = card.querySelector(".cb-status-text");
    if (statusTextEl) statusTextEl.textContent = text;
  };

  btnCallback.addEventListener("click", () => {
    term.textContent = "[3단계 비동기 시나리오 작동 시작]\n";
    btnCallback.disabled = true;

    // 시각화 요소 초기 대기화
    updateCardState(card1, "waiting", "대기 중");
    updateCardState(card2, "waiting", "대기 중");
    updateCardState(card3, "waiting", "대기 중");

    // 1단계 사용자 로그인 시작
    updateCardState(card1, "processing", "진행 중");
    
    console.log("==================================================");
    console.log("콜백 지옥 실행 흐름 추적 (F12 콘솔 들여쓰기 시각화)");
    console.log("==================================================");

    fakeLogin("user@test.com", (userEmail) => {
      term.textContent += `\n[1단계 완료] 사용자 로그인 성공: ${userEmail}\n`;
      updateCardState(card1, "completed", "완료");
      
      console.log("1단계: 로그인 콜백 실행 완료 (user: " + userEmail + ")");

      // 2단계 프로필 조회 시작
      updateCardState(card2, "processing", "진행 중");

      fakeGetProfile(userEmail, (profileName) => {
        term.textContent += `├── [2단계 완료] 프로필 로드 성공: ${profileName}\n`;
        updateCardState(card2, "completed", "완료");
        
        console.log("  └── 2단계: 프로필 조회 콜백 실행 완료 (name: " + profileName + ")");

        // 3단계 알림 목록 다운로드 시작
        updateCardState(card3, "processing", "진행 중");

        fakeGetNotifications(profileName, (notifications) => {
          term.textContent += `└── [3단계 완료] 신규 알림 수신: ${notifications.join(", ")}\n`;
          updateCardState(card3, "completed", "완료");
          
          console.log("        └── 3단계: 알림함 로드 콜백 실행 완료 (data: [" + notifications.join(", ") + "])");
          console.log("              └── [최종] 모든 콜백 중첩 실행 완료. 코드가 오른쪽으로 심각하게 밀려났음을 확인하세요.");
          
          term.innerHTML += `
[동작은 순서대로 되지만, 소스코드는 아래처럼 지옥이 됩니다]
----------------------------------------------------------------------
fakeLogin(email, (user) => {
    fakeGetProfile(user, (profile) => {
        fakeGetNotifications(profile, (notifications) => {
            // 안쪽으로 계속 파고들어 화면 우측으로 밀려납니다 (피라미드 구조)
            console.log("최종 데이터 처리 완료");
        });
    });
});
----------------------------------------------------------------------
결론: 무한 루프가 아니라, 개발자가 소스코드를 읽고 유지보수하거나 각 중첩 함수 내부마다
에러 처리 분기를 덕지덕지 넣어야 하는 작업 환경이 지옥 같아지므로 '콜백 지옥'이라 일컬어집니다.
          `;
          
          btnCallback.disabled = false;
        });
      });
    });
  });
}

// 모의 비동기 API들
function fakeLogin(email, callback) {
  setTimeout(() => {
    callback(email);
  }, 1000);
}

function fakeGetProfile(email, callback) {
  setTimeout(() => {
    callback("홍길동");
  }, 1000);
}

function fakeGetNotifications(name, callback) {
  setTimeout(() => {
    callback(["출석 이벤트 당첨", "비동기 과제 완료 안내"]);
  }, 1000);
}
