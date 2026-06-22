/**
 * ==========================================================================
 * Async/Await를 통한 비동기 제어 고도화 (main_03.js)
 * 학습 주제: Battery API, try/catch/finally 결제, SNS 병렬 최적화, OAuth2 Retry 리팩터링
 * ==========================================================================
 */

document.addEventListener("DOMContentLoaded", () => {
  console.log("async/await 실무 시나리오 스크립트 가동.");

  // 0. 다크모드 시스템 활성화
  initDarkMode();

  // 1. Battery Status API 모듈 (async/await 기초)
  initBatteryModule();

  // 2. try/catch/finally 결제 모듈 (통합 에러 핸들링)
  initPayValidationModule();

  // 3. SNS 대시보드 모듈 (병렬 await 최적화)
  initSnsDashboardModule();

  // 4. OAuth2 토큰 갱신 모듈 (Retry 리팩터링 대조)
  initTokenRetryModule();
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
 * 1. Battery Status API 연동 (async/await 기초)
 */
function initBatteryModule() {
  const connectBtn = document.getElementById("btn-battery-connect");
  const term = document.getElementById("term-battery-status");
  const levelBar = document.getElementById("battery-level-bar");
  const percentText = document.getElementById("battery-percent-text");
  const chargingText = document.getElementById("battery-charging-text");
  const lightning = document.getElementById("charging-lightning");
  const chkDischarging = document.getElementById("chk-mock-discharging");
  const chkCharging = document.getElementById("chk-mock-charging");

  if (!connectBtn || !term || !levelBar || !percentText || !chargingText || !lightning || !chkDischarging || !chkCharging) return;

  // 실시간 방전/충전 감쇄/증가 테스트용 타이머 변수
  let batteryTimerInterval = null;

  // 두 스위치가 상호 배타적으로 작동하도록 처리 (스위치 교차 차단)
  chkDischarging.addEventListener("change", () => {
    if (chkDischarging.checked) chkCharging.checked = false;
  });
  chkCharging.addEventListener("change", () => {
    if (chkCharging.checked) chkDischarging.checked = false;
  });

  // 배터리 UI 갱신 함수
  const updateBatteryUI = (level, charging) => {
    const pct = Math.round(level * 100);
    percentText.textContent = `${pct}%`;
    levelBar.style.width = `${pct}%`;

    // 잔량에 따른 색상 분기 제어
    if (pct <= 20) {
      levelBar.style.backgroundColor = "#e63946"; // 빨강
    } else if (pct <= 50) {
      levelBar.style.backgroundColor = "#ffb703"; // 주황
    } else {
      levelBar.style.backgroundColor = "#2a9d8f"; // 초록
    }

    if (charging) {
      chargingText.textContent = "충전 중";
      chargingText.style.color = "#4361ee";
      lightning.style.display = "inline";
    } else {
      chargingText.textContent = "방전 중 (배터리 사용 중)";
      chargingText.style.color = "#6c757d";
      lightning.style.display = "none";
    }
  };

  // 비지원 브라우저 대응 가상 모의 배터리 Promise 획득
  const getMockBattery = (dischargingMock = false) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          level: 0.82,
          charging: !dischargingMock,
          addEventListener: () => {} // 이벤트 리스너 인터페이스 모사
        });
      }, 1000); // 1.0초 비동기 딜레이
    });
  };

  // async/await 기반 배터리 데이터 획득 구동기
  connectBtn.addEventListener("click", async () => {
    connectBtn.disabled = true;
    
    // 기존에 작동 중이던 실시간 가상 타이머가 있다면 클리어
    if (batteryTimerInterval) {
      clearInterval(batteryTimerInterval);
      batteryTimerInterval = null;
    }

    // 비동기 대기(Pending) 상태 UI 연출 개시
    levelBar.style.width = "10%";
    levelBar.style.backgroundColor = "#ffb703"; // 대기 상태 노란색 적용
    percentText.textContent = "조회 중...";
    chargingText.textContent = "장치 보안 터널 연결 중...";
    chargingText.style.color = "#ffb703";
    lightning.style.display = "none";
    
    term.textContent = "하드웨어 배터리 컨트롤러에 보안 터널 세션을 맺는 중...\n상태: await 키워드를 통해 배터리 핸들러 약속을 취득하는 중 (1.2초 지연 모사)...";

    const isForceDischarging = chkDischarging.checked;
    const isForceCharging = chkCharging.checked;

    try {
      // 1.2초간의 하드웨어 세션 보안 수립 대기 (Pending 상태 체험 보장)
      await new Promise(resolve => setTimeout(resolve, 1200));

      let battery = null;
      
      // 실제 API 지원 여부 확인
      if (navigator.getBattery) {
        term.textContent += "\n[감지] 표준 기기 배터리 API를 포착했습니다. 시스템 권한 요청 중...";
        battery = await navigator.getBattery(); // await로 배터리 객체 획득 대기
      } else {
        term.textContent += "\n[주의] 배터리 API가 미지원되거나 차단되었습니다. 가상 모의 장치를 await로 불러옵니다...";
        battery = await getMockBattery(isForceDischarging); // fallback 모사 await 호출
      }

      // 획득한 배터리 장치 데이터 UI 렌더링 (Fulfilled 성공)
      if (isForceDischarging) {
        // 가상 방전 모드 작동 (85%에서 시작해서 2초마다 15% 감쇄)
        let virtualLevel = 0.85;
        updateBatteryUI(virtualLevel, false);
        
        term.innerHTML = `
[가상 방전 시뮬레이션 작동]
- 상태: 방전 테스트 가동 완료.
- 설명: 85% 배터리 잔량에서 출발하여 2초마다 15%씩 실시간 방전 감쇄가 일어납니다.
- 잔량이 50% 이하(주황), 20% 이하(빨강)로 내려갈 때 경고 게이지가 전환되는지 관찰하십시오.
        `;

        batteryTimerInterval = setInterval(() => {
          virtualLevel = Math.max(0.05, virtualLevel - 0.15);
          updateBatteryUI(virtualLevel, false);
          
          const pct = Math.round(virtualLevel * 100);
          term.textContent = `[실시간 방전 루프 중] 배터리 에너지가 감쇄되고 있습니다.\n현재 잔량: ${pct}%\n`;
          
          if (pct <= 20) {
            term.innerHTML += `\n[위험] 배터리 잔량이 20% 이하입니다. 급속 방전 중이니 충전선을 즉시 결합하십시오.`;
          } else if (pct <= 50) {
            term.innerHTML += `\n[경고] 배터리 잔량이 절반 이하로 소모되었습니다. 절전 모드 가동을 추천합니다.`;
          }

          if (virtualLevel <= 0.05) {
            clearInterval(batteryTimerInterval);
            term.textContent += "\n\n[종료] 기기가 방전으로 완전 방전(임계점 5% 도달)되었습니다.";
          }
        }, 2000);

      } else if (isForceCharging) {
        // 가상 충전 모드 작동 (10% 빨간색에서 시작해서 2초마다 15%씩 서서히 완충 연출)
        let virtualLevel = 0.10;
        updateBatteryUI(virtualLevel, true);

        term.innerHTML = `
[가상 충전 시뮬레이션 작동]
- 상태: 충전 테스트 가동 완료.
- 설명: 10% 배터리 잔량(빨간색)에서 출발하여 2초마다 15%씩 실시간 충전 증가가 일어납니다.
- 잔량이 20% 초과(주황색 진입), 50% 초과(초록색 진입)로 늘어날 때 게이지 색상이 변경되는지 관찰하십시오.
        `;

        batteryTimerInterval = setInterval(() => {
          virtualLevel = Math.min(1.0, virtualLevel + 0.15);
          updateBatteryUI(virtualLevel, true);

          const pct = Math.round(virtualLevel * 100);
          term.textContent = `[실시간 충전 루프 중] 전원이 정상 연결되어 배터리가 서서히 충전되고 있습니다.\n현재 잔량: ${pct}%\n`;

          if (pct >= 100) {
            term.innerHTML += `\n[완료] 배터리가 100% 완전히 충전되었습니다. 케이블을 분리하셔도 안전합니다.`;
          } else if (pct > 50) {
            term.innerHTML += `\n[정보] 배터리가 절반 이상 충전되었습니다. 안정 영역으로 진입했습니다.`;
          } else if (pct > 20) {
            term.innerHTML += `\n[정보] 배터리가 급속 충전되는 중입니다. 주황색 경고 영역을 돌파했습니다.`;
          }

          if (virtualLevel >= 1.0) {
            clearInterval(batteryTimerInterval);
            term.textContent += "\n\n[종료] 기기 충전 프로세스가 완료되어 시뮬레이션을 중지합니다.";
          }
        }, 2000);

      } else {
        // 일반 상태 연동 시 실제 하드웨어 데이터 출력
        updateBatteryUI(battery.level, battery.charging);

        term.innerHTML = `
[장치 연동 성공]
- 배터리 잔량 정보 수신 완료.
- async 함수 내에서 await를 통해 배터리 정보를 획득할 때까지 자바스크립트가 비차단(Non-blocking) 대기하여 스레드를 점유하지 않았습니다.
- 충전 게이지가 실제 수치로 부드럽게 차오르며 동적 바인딩되었습니다.
        `;

        // 기기 배터리 변화 이벤트 리스너 바인딩
        battery.addEventListener("levelchange", () => {
          if (!chkDischarging.checked && !chkCharging.checked) {
            updateBatteryUI(battery.level, battery.charging);
            console.log(`[Battery Event] 배터리 잔량이 변경되었습니다: ${battery.level * 100}%`);
          }
        });

        battery.addEventListener("chargingchange", () => {
          if (!chkDischarging.checked && !chkCharging.checked) {
            updateBatteryUI(battery.level, battery.charging);
            console.log(`[Battery Event] 배터리 충전 결합 상태 변경: ${battery.charging}`);
          }
        });
      }

    } catch (error) {
      term.innerHTML = `\n[장치 연동 실패] 하드웨어 접근 에러: ${error.message}`;
    } finally {
      connectBtn.disabled = false;
    }
  });
}

/**
 * 2. try/catch/finally 결제 모듈 (통합 에러 핸들링)
 */
function initPayValidationModule() {
  const paymentForm = document.getElementById("payment-form");
  const submitBtn = document.getElementById("btn-pay-submit");
  const spinner = document.getElementById("pay-loading-spinner");
  const alertBanner = document.getElementById("pay-alert-banner");
  const term = document.getElementById("term-pay-control");

  const chkNetDown = document.getElementById("chk-network-down");
  const chkLimitFail = document.getElementById("chk-limit-exceeded");

  if (!paymentForm || !submitBtn || !spinner || !alertBanner || !term || !chkNetDown || !chkLimitFail) return;

  // 가상 카드 대행사 결제 승인 API
  const fakeCardAuthorizeAPI = (netDown, limitFail) => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if (netDown) {
          reject(new Error("네트워크 연결 실패: 인터넷 망 통신이 원활하지 않습니다. (503 Service Unavailable)"));
        } else if (limitFail) {
          reject(new Error("한도 초과 에러: 입력하신 카드의 결제 한도가 초과되었습니다. (402 Payment Required)"));
        } else {
          resolve("CARD_AUTH_SUCCESS_9281");
        }
      }, 1500); // 1.5초간 승인 딜레이
    });
  };

  // async/await + try/catch/finally 결제 트랜잭션 처리기
  paymentForm.addEventListener("submit", async (e) => {
    e.preventDefault(); // 2일차 복습: 서브밋 기본 이벤트 전송 차단
    // 1. UI 초기화 및 전송 상태 돌입
    submitBtn.disabled = true;
    spinner.style.display = "inline-block";
    alertBanner.style.display = "none";
    term.textContent = "PG 카드 게이트웨이 보안 인증 토큰 대기 중...\n상태: await executeCardPayment() 연산 대기 시작...";

    // 시뮬레이션 옵션 확인
    const isNetDown = chkNetDown.checked;
    const isLimitFail = chkLimitFail.checked;

    try {
      // 2. 비동기 결제 요청을 await로 동기식 코드 스타일처럼 호출
      const authCode = await fakeCardAuthorizeAPI(isNetDown, isLimitFail);
      
      // 결제 성공 시 분기 처리 (authCode 수신 후 순차 실행)
      term.innerHTML = `
[결제 트랜잭션 완료]
- 상태: try 블록 정상 종료 (Fulfilled)
- 카드사 승인 코드: ${authCode}
- 설명: 비동기 데이터 획득에 성공하여 아래의 다음 실행줄로 안전하게 제어권이 이행되었습니다.
      `;
    } catch (error) {
      // 3. 비동기 오류(네트워크 단절, 한도 초과 등)를 try에서 포착해 catch로 자동 이송
      alertBanner.textContent = `결제 실패: ${error.message}`;
      alertBanner.style.display = "block";
      
      term.innerHTML = `
[결제 트랜잭션 오류]
- 상태: catch 블록 긴급 점프 작동 (Rejected)
- 감지 에러: ${error.message}
- 설명: 비동기 함수에서 거부(reject)된 예외가 동기식 에러와 완전히 동일한 catch 채널로 흡수되었습니다.
      `;
    } finally {
      // 4. 성공하든 오류가 나든 리소스 뒷정리를 위해 100% 실행되는 마무리 블록
      spinner.style.display = "none";
      submitBtn.disabled = false;
      term.textContent += "\n\n[finally] 결제 스피너 세션을 해제하고 결제 요청 전송 폼을 원복 조치했습니다.";
    }
  });
}

/**
 * 3. SNS 대시보드 모듈 (병렬 await 최적화)
 */
function initSnsDashboardModule() {
  const btnSeq = document.getElementById("btn-run-serial-await");
  const btnPar = document.getElementById("btn-run-parallel-await");
  const term = document.getElementById("term-sns-dashboard");

  const barSeq = document.getElementById("progress-serial-await");
  const barPar = document.getElementById("progress-parallel-await");
  const textSeq = document.getElementById("time-serial-await");
  const textPar = document.getElementById("time-parallel-await");

  // 위젯 요소들
  const wInstaVal = document.getElementById("widget-insta-val");
  const wInstaStatus = document.getElementById("widget-insta-status");
  const wInsta = document.getElementById("widget-insta");

  const wTwitterVal = document.getElementById("widget-twitter-val");
  const wTwitterStatus = document.getElementById("widget-twitter-status");
  const wTwitter = document.getElementById("widget-twitter");

  const wYoutubeVal = document.getElementById("widget-youtube-val");
  const wYoutubeStatus = document.getElementById("widget-youtube-status");
  const wYoutube = document.getElementById("widget-youtube");

  if (!btnSeq || !btnPar || !term || !barSeq || !barPar || !textSeq || !textPar) return;

  const resetDashboardUI = () => {
    const widgets = [wInsta, wTwitter, wYoutube];
    widgets.forEach(w => {
      w.className = "widget";
      w.querySelector(".widget-value").textContent = "--";
      w.querySelector(".widget-status").textContent = "대기 중";
      w.querySelector(".widget-status").style.color = "#6c757d";
    });
    barSeq.style.width = "0%";
    barSeq.textContent = "0%";
    textSeq.textContent = "소요 시간: 0.0초";
    barPar.style.width = "0%";
    barPar.textContent = "0%";
    textPar.textContent = "소요 시간: 0.0초";
  };

  // 모의 SNS API 데이터
  const fetchInstagram = () => new Promise(resolve => setTimeout(() => resolve("10.2k Likes"), 800));
  const fetchTwitter = () => new Promise(resolve => setTimeout(() => resolve("#JavaScript 트렌드 1위"), 1200));
  const fetchYoutube = () => new Promise(resolve => setTimeout(() => resolve("52,400 Views"), 600));

  // 정밀한 게이지바 카운터 타이머 가동 헬퍼
  const runTimerVisual = (bar, label, expectedTime) => {
    const startTime = Date.now();
    bar.style.width = "0%";
    bar.textContent = "0%";

    const interval = setInterval(() => {
      const elapsed = (Date.now() - startTime) / 1000;
      label.textContent = `소요 시간: ${elapsed.toFixed(1)}초`;
      
      const pct = Math.min(Math.floor((elapsed / expectedTime) * 100), 99);
      bar.style.width = `${pct}%`;
      bar.textContent = `${pct}%`;
    }, 50);

    return {
      stop: () => {
        clearInterval(interval);
        const finalElapsed = (Date.now() - startTime) / 1000;
        label.textContent = `소요 시간: ${finalElapsed.toFixed(1)}초`;
        bar.style.width = "100%";
        bar.textContent = "100%";
        return finalElapsed.toFixed(2);
      }
    };
  };

  // 방식 A: 직렬 await 연쇄 대기 호출
  btnSeq.addEventListener("click", async () => {
    resetDashboardUI();
    btnSeq.disabled = true;
    btnPar.disabled = true;
    term.textContent = "방식 A: 직렬 await로 3개 SNS 데이터를 하나씩 차례대로 호출합니다...\n";

    const visual = runTimerVisual(barSeq, textSeq, 2.6); // 0.8 + 1.2 + 0.6 = 2.6초 예상
    const startTime = performance.now();

    try {
      // 1. 인스타그램
      wInsta.className = "widget loading";
      wInstaStatus.textContent = "로딩 중...";
      wInstaStatus.style.color = "#ffb703";
      
      const instaData = await fetchInstagram(); // 완료할 때까지 스레드 제어권 반환 및 멈춤 대기
      wInsta.className = "widget loaded";
      wInstaVal.textContent = instaData;
      wInstaStatus.textContent = "완료";
      wInstaStatus.style.color = "#2a9d8f";
      term.textContent += `- [완료] Instagram 피드 획득 (소요 누적: 약 0.8초)\n`;

      // 2. 트위터
      wTwitter.className = "widget loading";
      wTwitterStatus.textContent = "로딩 중...";
      wTwitterStatus.style.color = "#ffb703";

      const twitterData = await fetchTwitter(); // 완료할 때까지 대기
      wTwitter.className = "widget loaded";
      wTwitterVal.textContent = twitterData;
      wTwitterStatus.textContent = "완료";
      wTwitterStatus.style.color = "#2a9d8f";
      term.textContent += `- [완료] Twitter 트렌드 획득 (소요 누적: 약 2.0초)\n`;

      // 3. 유튜브
      wYoutube.className = "widget loading";
      wYoutubeStatus.textContent = "로딩 중...";
      wYoutubeStatus.style.color = "#ffb703";

      const youtubeData = await fetchYoutube(); // 완료할 때까지 대기
      wYoutube.className = "widget loaded";
      wYoutubeVal.textContent = youtubeData;
      wYoutubeStatus.textContent = "완료";
      wYoutubeStatus.style.color = "#2a9d8f";
      term.textContent += `- [완료] YouTube 분석 획득 (소요 누적: 약 2.6초)\n`;

      const duration = ((performance.now() - startTime) / 1000).toFixed(2);
      visual.stop();

      term.innerHTML += `
\n[직렬 await 실행 결과]
- 3개 위젯 데이터 순차 획득 최종 소요 시간: ${duration}초
- 상태: 의존성 없는 SNS 데이터 호출들이 직렬 await 나열로 인하여 이전 API의 딜레이가 순차 합산(0.8 + 1.2 + 0.6 = 총 2.6초)되어 화면 로딩 정체 병목을 초래했습니다.
      `;

    } catch (error) {
      visual.stop();
      term.textContent += `\n[오류] 직렬 호출 도중 문제 발생: ${error.message}\n`;
    } finally {
      btnSeq.disabled = false;
      btnPar.disabled = false;
    }
  });

  // 방식 B: Promise.all + await 병렬 호출
  btnPar.addEventListener("click", async () => {
    resetDashboardUI();
    btnSeq.disabled = true;
    btnPar.disabled = true;
    term.textContent = "방식 B: Promise.all + await를 활용해 3개 SNS 데이터를 동시 요청합니다...\n";

    const visual = runTimerVisual(barPar, textPar, 1.2); // 최장 시간인 1.2초 예상
    const startTime = performance.now();

    // 3개 위젯 동시 로딩 점등
    const widgets = [wInsta, wTwitter, wYoutube];
    const statuses = [wInstaStatus, wTwitterStatus, wYoutubeStatus];
    widgets.forEach(w => w.className = "widget loading");
    statuses.forEach(s => {
      s.textContent = "로딩 중...";
      s.style.color = "#ffb703";
    });

    try {
      // 3개의 Promise를 동시에 발송하고, 전체가 한꺼번에 완료되길 await로 하나로 묶어 대기
      const [instaData, twitterData, youtubeData] = await Promise.all([
        fetchInstagram(),
        fetchTwitter(),
        fetchYoutube()
      ]);

      // 일괄 완료 데이터 UI 분배
      wInsta.className = "widget loaded";
      wInstaVal.textContent = instaData;
      wInstaStatus.textContent = "완료";
      wInstaStatus.style.color = "#2a9d8f";

      wTwitter.className = "widget loaded";
      wTwitterVal.textContent = twitterData;
      wTwitterStatus.textContent = "완료";
      wTwitterStatus.style.color = "#2a9d8f";

      wYoutube.className = "widget loaded";
      wYoutubeVal.textContent = youtubeData;
      wYoutubeStatus.textContent = "완료";
      wYoutubeStatus.style.color = "#2a9d8f";

      term.textContent += `- [병렬 완료] 모든 SNS 피드 응답 동시 수령 성공\n`;

      const duration = ((performance.now() - startTime) / 1000).toFixed(2);
      visual.stop();

      term.innerHTML += `
\n[병렬 await 실행 결과]
- 3개 위젯 데이터 동시 획득 최종 소요 시간: ${duration}초
- 상태: 3가지 비동기 요청을 동시 출발시켜 대기 시간이 최장 지연을 지닌 'Twitter API(1.2초)' 시간으로 전량 수렴되었습니다. 소요 시간이 2.6초에서 1.2초로 대폭 단축되어 병렬 최적화가 원활히 달성되었습니다.
      `;

    } catch (error) {
      visual.stop();
      term.textContent += `\n[오류] 병렬 호출 도중 문제 발생: ${error.message}\n`;
    } finally {
      btnSeq.disabled = false;
      btnPar.disabled = false;
    }
  });
}

/**
 * 4. OAuth2 인증 토큰 자동 갱신 및 API 재요청 (Retry 리팩터링)
 */
function initTokenRetryModule() {
  const btnPromise = document.getElementById("btn-promise-token-retry");
  const btnAsync = document.getElementById("btn-async-token-retry");
  const term = document.getElementById("term-token-retry");

  const step1 = document.getElementById("retry-step-1");
  const step2 = document.getElementById("retry-step-2");
  const step3 = document.getElementById("retry-step-3");

  const detail1 = document.getElementById("retry-step-1-details");
  const detail2 = document.getElementById("retry-step-2-details");
  const detail3 = document.getElementById("retry-step-3-details");

  if (!btnPromise || !btnAsync || !term || !step1 || !step2 || !step3) return;

  const resetRetryUI = () => {
    const cards = [step1, step2, step3];
    cards.forEach(card => {
      card.className = "chain-step-card waiting";
      card.querySelector(".badge").className = "badge badge-waiting";
      card.querySelector(".badge").textContent = "대기 중";
    });
    detail1.textContent = "API 서버 요청 대기 중";
    detail2.textContent = "신규 토큰 인증 대기 중";
    detail3.textContent = "보안 리트라이 세션 접수 대기 중";
  };

  const updateCard = (card, detail, status, text, detailText) => {
    card.className = `chain-step-card ${status}`;
    const badge = card.querySelector(".badge");
    badge.className = `badge badge-${status}`;
    badge.textContent = text;
    detail.textContent = detailText;
  };

  // 모의 1단계/3단계: 보안 데이터 요청 API
  const fakeSecureAPICall = (token) => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if (token === "EXPIRED_TOKEN") {
          reject({ status: 401, message: "토큰이 만료되었습니다. 인증 정보가 필요합니다." });
        } else if (token === "NEW_VALID_TOKEN") {
          resolve("대기 오염 물질 배출 동향 내부 기밀 보고서 문서 (보안 2등급)");
        } else {
          reject({ status: 403, message: "접근 권한 위반 에러" });
        }
      }, 800);
    });
  };

  // 모의 2단계: Refresh Token 토큰 발급 갱신 API
  const fakeRefreshTokenCall = () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve("NEW_VALID_TOKEN");
      }, 1000);
    });
  };

  // A. 기존 Promise 체인 시뮬레이션
  btnPromise.addEventListener("click", () => {
    resetRetryUI();
    btnPromise.disabled = true;
    btnAsync.disabled = true;
    term.textContent = "[A. Promise 체인 방식 토큰 리프레시 시연 시작]\n\n";

    console.log("==================================================");
    console.log("Promise.catch 기반 OAuth2 토큰 갱신 시뮬레이션");
    console.log("==================================================");

    // 1단계 시작
    updateCard(step1, detail1, "processing", "진행 중", "보안 헤더 [EXPIRED_TOKEN] 적재 후 API 통신 중...");
    
    // 만료된 토큰으로 API 호출
    fakeSecureAPICall("EXPIRED_TOKEN")
      .then((data) => {
        term.textContent += `[성공] 데이터 획득: ${data}\n`;
      })
      .catch((error) => {
        // 401 권한 에러 포착
        if (error.status === 401) {
          updateCard(step1, detail1, "failed", "오류", "401 토큰 만료 에러 접수");
          
          // 화면 터미널에 중첩 비동기 런타임 스택(디버깅 난해함) 즉시 로깅
          term.innerHTML = `
[1단계 에러 발생 - Promise.catch 감지]
- 통신 코드: 401 Unauthorized (인증 만료)
- 디버깅 스택 트레이스 (Call Stack Trace):
   at anonymous_then_callback_3 (main_03.js:630)
   at anonymous_then_callback_2 (main_03.js:623)
   at Promise.then (native_V8_engine)
   at anonymous_catch_handler_1 (main_03.js:615)
   at Promise.catch (native_V8_engine)
- 분석: 비동기 익명 콜백들이 꼬리를 물고 스택을 점유하여, 어느 then 줄에서 오류가 파생되었는지 최초 진원지 역추적이 매우 곤란합니다.

신규 토큰 갱신 요청을 전송합니다 (1.0초 대기)...
          `;

          // 2단계 시작 - 리프레시 토큰 전송 Promise 리턴
          updateCard(step2, detail2, "processing", "진행 중", "Refresh Token을 사용하여 토큰 재발급 요청 중...");
          return fakeRefreshTokenCall()
            .then((newToken) => {
              updateCard(step2, detail2, "completed", "완료", `액세스 토큰 갱신 완료: ${newToken}`);
              console.log(`├── Promise Step 2: 신규 토큰 발급 성공 (${newToken})`);

              // 3단계 시작 - 획득한 새 토큰을 싣고 동일 API 재요청(Retry) 리턴
              updateCard(step3, detail3, "processing", "진행 중", "신규 발급받은 보안 토큰 적재 후 API 재도전 요청 중...");
              return fakeSecureAPICall(newToken);
            })
            .then((secureData) => {
              // 재도전 결실 수령
              updateCard(step3, detail3, "completed", "완료", "보안 API 재시도 성공 완료 (이행)");
              console.log(`└── Promise Step 3: 재도전 성공. 데이터 취득 완료.`);

              // A 방식 최종 가독성 붕괴(들여쓰기 밀림) 시각화 출력
              term.innerHTML = `
[Promise 체인 완료 - 최종 결과 취득]
- 수신 보안 데이터: "${secureData}"

[A 방식 실제 소스코드 형태 (들여쓰기 우측 밀림 및 파멸의 피라미드)]
----------------------------------------------------------------------
requestSecure()
  .then(data => ...)
  .catch(err => {
    return refresh()
      .then(newToken => {               // <--- [들여쓰기 누적 1]
        return requestSecure(newToken)
          .then(retryData => {          // <--- [들여쓰기 누적 2]
            console.log(retryData);
          });
      });
  });
----------------------------------------------------------------------
결론: 비동기 제어를 위해 then 콜백을 꼬리물며 안으로 파고 들어가기 때문에, 
단계가 늘어날수록 화면 밖으로 코드가 밀려나 가독성이 심각하게 파괴됩니다.
              `;
            });
        } else {
          throw error; // 다른 에러는 다음 catch로 전파
        }
      })
      .catch((finalErr) => {
        term.textContent += `\n[결국 최종 거부] 복구 불가 보안 오류: ${finalErr.message}\n`;
      })
      .finally(() => {
        btnPromise.disabled = false;
        btnAsync.disabled = false;
      });
  });

  // B. Async/Await 리팩터링 시뮬레이션 (동기식 일렬 구조)
  btnAsync.addEventListener("click", async () => {
    resetRetryUI();
    btnPromise.disabled = true;
    btnAsync.disabled = true;
    term.textContent = "[B. Async/Await 리팩터링 방식 토큰 리프레시 시연 시작]\n\n";

    console.log("==================================================");
    console.log("async/await 기반 OAuth2 토큰 갱신 시뮬레이션 (평탄도 극대화)");
    console.log("==================================================");

    // 1단계 시작
    updateCard(step1, detail1, "processing", "진행 중", "보안 헤더 [EXPIRED_TOKEN] 적재 후 API 통신 중...");
    let token = "EXPIRED_TOKEN";

    try {
      // 1. 만료된 토큰으로 통신 시도 (첫 번째 await)
      const data = await fakeSecureAPICall(token);
      term.textContent += `[성공] 데이터 획득: ${data}\n`;
    } catch (error) {
      // 2. 만료 에러 검출 시 리프레시 및 재도전 로직 가동
      if (error.status === 401) {
        updateCard(step1, detail1, "failed", "오류", "401 토큰 만료 에러 접수");
        console.warn("async/await Step 1: 401 Unauthorized 감지. 동기식 try/catch 분기 진입.");

        // 화면 터미널에 평탄화된 비동기 런타임 스택(디버깅 대단히 수월함) 즉시 로깅
        term.innerHTML = `
[1단계 에러 발생 - try/catch 감지]
- 통신 코드: 401 Unauthorized (인증 만료)
- 디버깅 스택 트레이스 (Call Stack Trace):
   at executeSecureTokenRetry (main_03.js:685)
   at HTMLButtonElement.onclick (main_03.js:536)
- 분석: 무의미한 익명 콜백 꼬리(<anonymous>)가 원천 배제되고, 동기식 함수 흐름인 executeSecureTokenRetry의 단일 실행 라인이 명확하게 호출 스택에 기록되어 디버깅 추적성이 100% 보장됩니다.

신규 토큰 갱신 요청을 전송합니다 (1.0초 대기)...
        `;

        // 2단계 시작 (두 번째 await - 토큰 재발급 대기)
        updateCard(step2, detail2, "processing", "진행 중", "Refresh Token을 사용하여 토큰 재발급 요청 중...");
        await new Promise(resolve => setTimeout(resolve, 1000));
        const newToken = await fakeRefreshTokenCall();
        
        updateCard(step2, detail2, "completed", "완료", `액세스 토큰 갱신 완료: ${newToken}`);
        console.log(`├── async/await Step 2: 신규 토큰 발급 성공 (${newToken})`);

        // 3단계 시작 (세 번째 await - 재도전 요청 대기)
        updateCard(step3, detail3, "processing", "진행 중", "신규 발급받은 보안 토큰 적재 후 API 재도전 요청 중...");
        await new Promise(resolve => setTimeout(resolve, 800));
        const secureData = await fakeSecureAPICall(newToken);

        // 최종 성공 결과
        updateCard(step3, detail3, "completed", "완료", "보안 API 재시도 성공 완료 (이행)");
        console.log(`└── async/await Step 3: 재도전 성공. 데이터 취득 완료.`);

        // B 방식 최종 가독성 평탄화(일렬) 시각화 출력
        term.innerHTML = `
[Async/Await 완료 - 최종 결과 취득]
- 수신 보안 데이터: "${secureData}"

[B 방식 실제 소스코드 형태 (일렬 종대 및 깊이 1단계 고정 평탄 구조)]
----------------------------------------------------------------------
try {
  const data = await requestSecure();
} catch (err) {
  if (err.status === 401) {
    const newToken = await refresh();
    const retryData = await requestSecure(newToken);
    console.log(retryData);
  }
}
----------------------------------------------------------------------
결론: 콜백 체인을 전부 걷어내고 await 지시어로 일렬 정돈함으로써, 
단계가 아무리 많이 추가되어도 들여쓰기 깊이가 1단계로 납작하게 고정되어 
동기식 코드와 완전히 동등한 가독성과 유지보수 편의를 제공합니다.
        `;
      } else {
        term.textContent += `\n[오류] 기타 보안 에러 발생: ${error.message}\n`;
      }
    } finally {
      // 폼 제어권 원복
      btnPromise.disabled = false;
      btnAsync.disabled = false;
    }
  });
}
