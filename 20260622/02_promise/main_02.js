/**
 * ==========================================================================
 *  Promise 실무 중심 비동기 흐름 제어 (main_02.js)
 * 학습 주제: Geolocation API, 프로필 업로드 폼, 주문 결제 체이닝, 대시보드 병렬 최적화
 * ==========================================================================
 */

document.addEventListener("DOMContentLoaded", () => {
  console.log("[실습] 실무 시나리오 기반 스크립트 가동.");

  // 0. 다크모드 시스템 활성화
  initDarkMode();

  // 1. Geolocation 위치 정보 요청 모듈 (3가지 상태 확인)
  initGeolocationModule();

  // 2. 프로필 이미지 업로드 모듈 (then/catch/finally 흐름 제어)
  initProfileUploadModule();

  // 3. 쇼핑몰 결제 주문 파이프라인 (Promise 체이닝)
  initPaymentPipelineModule();

  // 4. 대시보드 위젯 API (Promise.all 병렬 최적화)
  initDashboardModule();
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
 * 1. 사용자 위치 권한 요청 (Geolocation API - Promise 3가지 상태)
 */
function initGeolocationModule() {
  const triggerBtn = document.getElementById("btn-geolocation-trigger");
  const term = document.getElementById("term-promise-state");
  const ledPending = document.getElementById("led-pending");
  const ledFulfilled = document.getElementById("led-fulfilled");
  const ledRejected = document.getElementById("led-rejected");

  if (!triggerBtn || !term || !ledPending || !ledFulfilled || !ledRejected) return;

  const resetLEDs = () => {
    ledPending.className = "promise-state-indicator";
    ledFulfilled.className = "promise-state-indicator";
    ledRejected.className = "promise-state-indicator";
  };

  triggerBtn.addEventListener("click", () => {
    resetLEDs();
    ledPending.classList.add("pending-active");
    triggerBtn.disabled = true;
    term.textContent = "Geolocation API를 통해 브라우저 기기 위치 정보를 요청 중입니다.\n상태: Pending (사용자 권한 승인 대기 중)...";

    // navigator.geolocation 호출을 Promise화하여 감싸기 (실무 래핑 패턴)
    const getPositionPromise = () => {
      return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
          reject(new Error("이 브라우저는 위치 정보를 지원하지 않습니다."));
          return;
        }
        
        // 실제 브라우저 API 호출
        navigator.geolocation.getCurrentPosition(
          (position) => {
            resolve(position); // 승인 시
          },
          (error) => {
            reject(error); // 거부 또는 장치 에러 시
          },
          { timeout: 10000 }
        );
      });
    };

    // Promise 실행 및 상태 추적
    getPositionPromise()
      .then((position) => {
        resetLEDs();
        ledFulfilled.classList.add("fulfilled-active");
        
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        const acc = position.coords.accuracy;

        term.innerHTML = `
[Promise 상태 전환 결과]
- 최종 상태: Fulfilled (이행 완료)
- 수신 데이터 (위치 정보):
  * 위도 (Latitude): ${lat.toFixed(6)}
  * 경도 (Longitude): ${lon.toFixed(6)}
  * 정확도 (Accuracy): ${acc.toFixed(1)} 미터
- 설명: 사용자가 권한을 허용하여 비동기 데이터 획득에 성공했습니다.
        `;
      })
      .catch((error) => {
        resetLEDs();
        ledRejected.classList.add("rejected-active");

        let errorMsg = "알 수 없는 에러가 발생했습니다.";
        if (error.code === 1) {
          errorMsg = "사용자가 위치 권한 요청을 거부(차단)했습니다. (PERMISSION_DENIED)";
        } else if (error.code === 2) {
          errorMsg = "네트워크 문제나 GPS 신호 불량으로 위치를 찾을 수 없습니다. (POSITION_UNAVAILABLE)";
        } else if (error.code === 3) {
          errorMsg = "위치 정보를 가져오는 데 시간이 초과되었습니다. (TIMEOUT)";
        } else {
          errorMsg = error.message;
        }

        term.innerHTML = `
[Promise 상태 전환 결과]
- 최종 상태: Rejected (거부 완료)
- 오류 원인: ${errorMsg}
- 설명: 사용자가 거부를 눌렀거나 기기 환경 결함으로 인해 약속이 취소되었습니다.
        `;
      })
      .finally(() => {
        triggerBtn.disabled = false;
      });
  });
}

/**
 * 2. 프로필 이미지 업로드 모듈 (then/catch/finally 흐름 제어)
 */
function initProfileUploadModule() {
  const fileInput = document.getElementById("profile-file-input");
  const fileInfoSpan = document.getElementById("selected-file-info");
  const submitBtn = document.getElementById("btn-upload-submit");
  const failBtn = document.getElementById("btn-upload-fail-submit");
  const spinner = document.getElementById("upload-loading-spinner");
  const previewImg = document.getElementById("upload-preview-img");
  const alertBanner = document.getElementById("upload-alert-banner");
  const term = document.getElementById("term-then-catch");

  // 2일차 연계: 실시간 ID 비동기 검증을 위한 요소
  const inputCheckId = document.getElementById("input-check-id");
  const checkIdStatus = document.getElementById("check-id-status");

  if (!fileInput || !submitBtn || !failBtn || !spinner || !previewImg || !alertBanner || !term) return;

  let currentFile = null;

  // 2일차 복습: ID 실시간 비동기 검증 함수
  const checkUsernamePromise = (username) => {
    return new Promise((resolve, reject) => {
      // 0.8초 가상 네트워크 딜레이
      setTimeout(() => {
        const regex = /^[a-zA-Z0-9]+$/;
        if (!regex.test(username)) {
          reject(new Error("영문과 숫자만 사용할 수 있습니다."));
          return;
        }
        if (username.length < 4) {
          reject(new Error("아이디는 최소 4글자 이상이어야 합니다."));
          return;
        }
        // 예약어로 가상 중복 설정
        const duplicateUsers = ["admin", "root", "guest", "hong", "lee"];
        if (duplicateUsers.includes(username.toLowerCase())) {
          reject(new Error("이미 사용 중인 중복된 아이디입니다."));
        } else {
          resolve("사용 가능한 멋진 아이디입니다!");
        }
      }, 800);
    });
  };

  // 실시간 input 이벤트 바인딩
  if (inputCheckId && checkIdStatus) {
    let debounceTimer = null;

    inputCheckId.addEventListener("input", (e) => {
      const username = e.target.value.trim();

      checkIdStatus.style.color = "#6c757d";
      checkIdStatus.textContent = "검사 대기 중...";

      if (debounceTimer) clearTimeout(debounceTimer);

      if (!username) {
        checkIdStatus.textContent = "아이디를 입력해 주세요.";
        return;
      }

      // 입력 완료 후 0.5초 딜레이 검증 (디바운스 활용한 비동기 전송 시뮬레이션)
      debounceTimer = setTimeout(() => {
        checkIdStatus.textContent = "서버 조회 중...";
        term.textContent = `[ID 검증 시작] '${username}' 중복 조회를 시작합니다...\n`;

        checkUsernamePromise(username)
          .then((successMsg) => {
            checkIdStatus.style.color = "#2a9d8f";
            checkIdStatus.textContent = successMsg;
            term.textContent += `\n[Fulfilled] 중복 검증 통과: ${successMsg}`;
          })
          .catch((error) => {
            checkIdStatus.style.color = "#e63946";
            checkIdStatus.textContent = error.message;
            term.textContent += `\n[Rejected] 중복 검증 실패: ${error.message}`;
          });
      }, 500);
    });
  }

  // 가상의 로컬 파일 선택 처리
  fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) {
      currentFile = file;
      fileInfoSpan.textContent = `${file.name} (크기: ${(file.size / 1024 / 1024).toFixed(2)} MB)`;
      term.textContent = `파일 선택 완료: ${file.name}\n업로드를 하려면 버튼을 클릭하십시오.`;
      
      // 파일 크기가 5MB 초과하는 경우 경고 색상 처리
      if (file.size > 5 * 1024 * 1024) {
        fileInfoSpan.style.color = "#e63946";
        fileInfoSpan.textContent += " [용량 초과 - 업로드 시 거절됨]";
      } else {
        fileInfoSpan.style.color = "#212529";
      }
    }
  });

  // 실제 파일을 읽어서 업로드 모사하는 비동기 함수 (FileReader Promise)
  const uploadImagePromise = (file, forceError = false) => {
    return new Promise((resolve, reject) => {
      // 1.5초 대기 후 전송 시도
      setTimeout(() => {
        if (forceError) {
          reject(new Error("용량 제한 초과: 파일 크기(최대 5MB)를 초과했습니다."));
          return;
        }

        if (!file) {
          reject(new Error("선택된 파일이 없습니다. 먼저 이미지 파일을 선택해 주십시오."));
          return;
        }

        // 실제 파일 검증
        if (file.size > 5 * 1024 * 1024) {
          reject(new Error(`용량 제한 초과: 선택한 파일 크기(${(file.size / 1024 / 1024).toFixed(2)}MB)가 5MB 제한을 넘었습니다.`));
          return;
        }

        if (!file.type.startsWith("image/")) {
          reject(new Error(`형식 오류: 선택한 파일 형식(${file.type})은 지원하지 않습니다. 이미지 파일만 업로드 가능합니다.`));
          return;
        }

        // 실제 이미지 리더 구동 (Base64 변환)
        const reader = new FileReader();
        reader.onload = (event) => {
          resolve(event.target.result); // Base64 데이터 URL 전달
        };
        reader.onerror = () => {
          reject(new Error("파일 읽기 과정에서 내부 브라우저 오류가 발생했습니다."));
        };
        reader.readAsDataURL(file);
      }, 1500); // 1.5초간 비동기 통신 대기 연출
    });
  };

  // 성공 및 실물 이미지 업로드 전송 동작
  submitBtn.addEventListener("click", () => {
    submitBtn.disabled = true;
    failBtn.disabled = true;
    spinner.style.display = "inline-block";
    alertBanner.style.display = "none";
    previewImg.style.display = "none";
    term.textContent = "클라우드 스토리지 서버에 파일 전송 세션을 생성하는 중...\n상태: 업로드 데이터 스트리밍 중 (1.5초 대기)...";

    uploadImagePromise(currentFile, false)
      .then((dataUrl) => {
        // 성공 시 화면 처리
        previewImg.src = dataUrl;
        previewImg.style.display = "block";
        term.innerHTML = `
[업로드 결과]
- 최종 상태: Fulfilled (이행 완료)
- 설명: 선택하신 실제 이미지 데이터가 온전히 업로드되어 아래에 미리보기로 렌더링되었습니다.
- 이미지 파일명: ${currentFile ? currentFile.name : "N/A"}
        `;
      })
      .catch((error) => {
        // 실패 시 화면 처리
        alertBanner.textContent = `업로드 실패: ${error.message}`;
        alertBanner.style.display = "block";
        term.innerHTML = `
[업로드 결과]
- 최종 상태: Rejected (거부 완료)
- 에러 원인: ${error.message}
- 설명: 파일 크기나 형식 검증을 통과하지 못해 catch 파이프라인에서 오류가 포착되었습니다.
        `;
      })
      .finally(() => {
        // 공통 뒷정리: 성공하든 실패하든 무조건 실행되는 영역
        spinner.style.display = "none";
        submitBtn.disabled = false;
        failBtn.disabled = false;
        term.textContent += "\n\n[.finally()] 업로드 프로세스 소멸 및 로딩 인디케이터가 회수되었습니다. (폼 제어권 복구)";
      });
  });

  // 강제 실패 시나리오 동작 (실제 파일 유무와 상관없이 오류 발생 시뮬레이션)
  failBtn.addEventListener("click", () => {
    submitBtn.disabled = true;
    failBtn.disabled = true;
    spinner.style.display = "inline-block";
    alertBanner.style.display = "none";
    previewImg.style.display = "none";
    term.textContent = "클라우드 스토리지 서버에 파일 전송 세션을 생성하는 중...\n상태: 업로드 데이터 스트리밍 중 (1.5초 대기)...";

    uploadImagePromise(null, true)
      .then((dataUrl) => {
        // 에러가 강제 발생하므로 then 영역은 실행되지 않음
        previewImg.src = dataUrl;
        previewImg.style.display = "block";
      })
      .catch((error) => {
        // 실패 시 화면 처리
        alertBanner.textContent = `업로드 실패: ${error.message}`;
        alertBanner.style.display = "block";
        term.innerHTML = `
[업로드 결과]
- 최종 상태: Rejected (거부 완료)
- 에러 원인: ${error.message}
- 설명: 강제 오류 모듈이 동작하여 catch 파이프라인으로 제어권이 넘어갔습니다.
        `;
      })
      .finally(() => {
        // 공통 뒷정리: 실패하더라도 리소스 회수는 무조건 보장됩니다.
        spinner.style.display = "none";
        submitBtn.disabled = false;
        failBtn.disabled = false;
        term.textContent += "\n\n[.finally()] 업로드 프로세스 소멸 및 로딩 인디케이터가 회수되었습니다. (폼 제어권 복구)";
      });
  });
}

/**
 * 3. 쇼핑몰 결제 주문 파이프라인 (Promise 체이닝)
 */
function initPaymentPipelineModule() {
  const btnSuccess = document.getElementById("btn-payment-success");
  const btnLimitFail = document.getElementById("btn-payment-limit-fail");
  const term = document.getElementById("term-promise-chain");

  const step1 = document.getElementById("payment-step-1");
  const step2 = document.getElementById("payment-step-2");
  const step3 = document.getElementById("payment-step-3");

  const detail1 = document.getElementById("payment-step-1-details");
  const detail2 = document.getElementById("payment-step-2-details");
  const detail3 = document.getElementById("payment-step-3-details");

  if (!btnSuccess || !btnLimitFail || !term || !step1 || !step2 || !step3) return;

  const resetPipelineUI = () => {
    const cards = [step1, step2, step3];
    cards.forEach(card => {
      card.className = "chain-step-card waiting";
      card.querySelector(".badge").className = "badge badge-waiting";
      card.querySelector(".badge").textContent = "대기 중";
    });
    detail1.textContent = "주문 등록 요청 전";
    detail2.textContent = "한도 잔액 조회 대기 중";
    detail3.textContent = "메시징 API 서버 대기 중";
  };

  const updateCard = (card, detail, status, text, detailText) => {
    card.className = `chain-step-card ${status}`;
    const badge = card.querySelector(".badge");
    badge.className = `badge badge-${status}`;
    badge.textContent = text;
    detail.textContent = detailText;
  };

  // 모의 통신 함수 1단계: 주문서 생성
  const fakeCreateOrder = () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const orderId = `ORD-${Date.now().toString().slice(-6)}`;
        resolve(orderId);
      }, 800);
    });
  };

  // 모의 통신 함수 2단계: PG 결제 처리
  const fakeProcessPayment = (orderId, triggerError = false) => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if (triggerError) {
          reject(new Error("PG사 승인 거절: 신용카드 한도 초과 오류 (결제 불가)"));
        } else {
          const paymentId = `PAY-${Math.random().toString(36).slice(2, 8).toUpperCase()}`;
          resolve({ orderId, paymentId });
        }
      }, 800);
    });
  };

  // 모의 통신 함수 3단계: 영수증 알림 전송
  const fakeSendReceipt = (paymentInfo) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(`[알림 발송 완료] 주문번호 ${paymentInfo.orderId}의 승인 내역(${paymentInfo.paymentId}) 발송 완료`);
      }, 800);
    });
  };

  // 결제 공통 연쇄 실행기
  const runPaymentChaining = (budgetFail = false) => {
    resetPipelineUI();
    btnSuccess.disabled = true;
    btnLimitFail.disabled = true;
    term.textContent = "쇼핑몰 결제 파이프라인 가동 개시...\n\n";

    console.log("==================================================");
    console.log("Promise Chaining 결제 파이프라인 시작 (F12 트리 로그)");
    console.log("==================================================");

    // 1단계 시작
    updateCard(step1, detail1, "processing", "진행 중", "서버 세션 생성 및 주문 아이템 검증 중...");

    fakeCreateOrder()
      .then((orderId) => {
        term.textContent += `[1단계 완료] 가상 주문 번호 생성: ${orderId}\n`;
        updateCard(step1, detail1, "completed", "완료", `주문번호 발급 완료: ${orderId}`);
        console.log(`Step 1 (주문): 성공 완료 (OrderId: ${orderId})`);

        // 2단계 시작 - PG사 전송을 위해 다음 Promise를 리턴하여 체인으로 엮음
        updateCard(step2, detail2, "processing", "진행 중", "PG 결제 게이트웨이 승인 요청 서명 검증 중...");
        return fakeProcessPayment(orderId, budgetFail);
      })
      .then((paymentInfo) => {
        // 결제가 성공한 경우 실행
        term.textContent += `├── [2단계 완료] 승인 승낙 획득: ${paymentInfo.paymentId}\n`;
        updateCard(step2, detail2, "completed", "완료", `결제 거래번호 발급 완료: ${paymentInfo.paymentId}`);
        console.log(`├── Step 2 (결제): 승인 성공 (PaymentId: ${paymentInfo.paymentId})`);

        // 3단계 시작 - 영수증 발송을 위해 다음 Promise를 리턴하여 체인으로 엮음
        updateCard(step3, detail3, "processing", "진행 중", "알림톡 카카오 API 게이트웨이 접수 시도...");
        return fakeSendReceipt(paymentInfo);
      })
      .then((deliveryResult) => {
        // 최종 3단계 성공 완료 시
        term.textContent += `└── [3단계 완료] ${deliveryResult}\n`;
        updateCard(step3, detail3, "completed", "완료", "알림톡 발송 완료 (최종 이행 완료)");
        console.log(`└── Step 3 (알림): 전송 완료 (${deliveryResult})`);
        
        term.innerHTML += `
\n[결제 최종 완료]
- 설명: 3단계의 순차 비동기 처리가 들여쓰기 꼬리물기 없이 일렬 체이닝으로 완벽하게 수렴되었습니다.
        `;
      })
      .catch((error) => {
        // 연쇄적인 then 작업 중 어느 한 군데라도 reject가 터지면 즉각 이쪽으로 굴러 떨어집니다. (에러 전파)
        term.textContent += `\n[파이프라인 폭발] 결제 오류 처리 포착: ${error.message}\n`;
        console.error(`└── [에러 전파 포착] 파이프라인 중단 원인: ${error.message}`);

        // 실패 단계에 따른 UI 피드백 부여
        if (step2.classList.contains("processing")) {
          updateCard(step2, detail2, "failed", "오류", error.message);
          updateCard(step3, detail3, "waiting", "중단됨", "이전 단계의 오류로 인해 작업이 강제 취소되었습니다.");
        } else if (step1.classList.contains("processing")) {
          updateCard(step1, detail1, "failed", "오류", error.message);
        }

        term.innerHTML += `
\n[에러 복구 가동]
- 설명: 개별 콜백 함수마다 지저분하게 if(error) 예외 대응을 수십 번 적을 필요 없이 하단의 단 하나의 .catch()로 통합 관리되어 디바이스 복원 조치가 단숨에 처리되었습니다.
        `;
      })
      .finally(() => {
        btnSuccess.disabled = false;
        btnLimitFail.disabled = false;
      });
  };

  btnSuccess.addEventListener("click", () => runPaymentChaining(false));
  btnLimitFail.addEventListener("click", () => runPaymentChaining(true));
}

/**
 * 4. 대시보드 위젯 API (Promise.all 병렬 최적화)
 */
function initDashboardModule() {
  const btnSeq = document.getElementById("btn-all-sequence");
  const btnPar = document.getElementById("btn-all-parallel");
  const term = document.getElementById("term-promise-all");

  const barSync = document.getElementById("progress-all-sync");
  const barAsync = document.getElementById("progress-all-async");
  const textSync = document.getElementById("time-all-sync");
  const textAsync = document.getElementById("time-all-async");

  // 위젯 UI 요소들
  const wProfileVal = document.getElementById("widget-profile-val");
  const wProfileStatus = document.getElementById("widget-profile-status");
  const wProfile = document.getElementById("widget-profile");

  const wSalesVal = document.getElementById("widget-sales-val");
  const wSalesStatus = document.getElementById("widget-sales-status");
  const wSales = document.getElementById("widget-sales");

  const wNoticeVal = document.getElementById("widget-notice-val");
  const wNoticeStatus = document.getElementById("widget-notice-status");
  const wNotice = document.getElementById("widget-notice");

  if (!btnSeq || !btnPar || !term || !barSync || !barAsync || !textSync || !textAsync) return;

  const resetDashboardUI = () => {
    const widgets = [wProfile, wSales, wNotice];
    widgets.forEach(w => {
      w.className = "widget";
      w.querySelector(".widget-value").textContent = "--";
      w.querySelector(".widget-status").textContent = "대기 중";
      w.querySelector(".widget-status").style.color = "#6c757d";
    });
    barSync.style.width = "0%";
    barSync.textContent = "0%";
    textSync.textContent = "소요 시간: 0.0초";
    barAsync.style.width = "0%";
    barAsync.textContent = "0%";
    textAsync.textContent = "소요 시간: 0.0초";
  };

  // 모의 대시보드 API 3종 (독립 데이터)
  const fetchProfile = () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ name: "임꺽정", grade: "VIP 회원" });
      }, 800); // 0.8초 소요
    });
  };

  const fetchSales = () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ count: "1,240건", revenue: "4,820,000원" });
      }, 1200); // 1.2초 소요
    });
  };

  const fetchNotice = () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ title: "시스템 정기 검사 안내", date: "06-25" });
      }, 600); // 0.6초 소요
    });
  };

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

  // 방식 A: 순차 비동기 실행 (비효율적인 꼬리물기 대기)
  btnSeq.addEventListener("click", () => {
    resetDashboardUI();
    btnSeq.disabled = true;
    btnPar.disabled = true;
    term.textContent = "방식 A: 대시보드 위젯 데이터를 개별 순차적으로 요청합니다...\n";

    const visual = runTimerVisual(barSync, textSync, 2.6); // 0.8 + 1.2 + 0.6 = 2.6초 예상
    const startTime = performance.now();

    // 1. 프로필 위젯 호출 시작
    wProfile.className = "widget loading";
    wProfileStatus.textContent = "로딩 중...";
    wProfileStatus.style.color = "#ffb703";

    fetchProfile()
      .then((profileData) => {
        // 프로필 성공 반영
        wProfile.className = "widget loaded";
        wProfileVal.textContent = profileData.name;
        wProfileStatus.textContent = profileData.grade;
        wProfileStatus.style.color = "#2a9d8f";
        term.textContent += `- [완료] 사용자 정보 획득 (소요 시간 누적: 약 0.8초)\n`;

        // 2. 매출 통계 위젯 호출 개시 (이전 완료 후 대기 출발)
        wSales.className = "widget loading";
        wSalesStatus.textContent = "로딩 중...";
        wSalesStatus.style.color = "#ffb703";
        return fetchSales();
      })
      .then((salesData) => {
        // 매출 성공 반영
        wSales.className = "widget loaded";
        wSalesVal.textContent = salesData.revenue;
        wSalesStatus.textContent = `총 ${salesData.count}`;
        wSalesStatus.style.color = "#2a9d8f";
        term.textContent += `- [완료] 매출 통계 획득 (소요 시간 누적: 약 2.0초)\n`;

        // 3. 공지사항 위젯 호출 개시 (이전 완료 후 대기 출발)
        wNotice.className = "widget loading";
        wNoticeStatus.textContent = "로딩 중...";
        wNoticeStatus.style.color = "#ffb703";
        return fetchNotice();
      })
      .then((noticeData) => {
        // 공지 성공 반영
        wNotice.className = "widget loaded";
        wNoticeVal.textContent = noticeData.title;
        wNoticeStatus.textContent = noticeData.date;
        wNoticeStatus.style.color = "#2a9d8f";
        term.textContent += `- [완료] 공지사항 획득 (소요 시간 누적: 약 2.6초)\n`;

        const duration = ((performance.now() - startTime) / 1000).toFixed(2);
        visual.stop();

        term.innerHTML += `
\n[순차 요청 방식 결과]
- 3개 위젯 데이터 획득 최종 소요 시간: ${duration}초
- 상태: 각 비동기 연산들이 상호 연관이 전혀 없음에도 앞선 작업의 대기가 끝날 때까지 병목 대기하여 개별 통신 딜레이 시간이 누적(0.8 + 1.2 + 0.6 = 총 2.6초)되는 불합리한 로딩 현상이 관찰되었습니다.
        `;
      })
      .finally(() => {
        btnSeq.disabled = false;
        btnPar.disabled = false;
      });
  });

  // 방식 B: Promise.all 병렬 실행 (동시 연산 최적화)
  btnPar.addEventListener("click", () => {
    resetDashboardUI();
    btnSeq.disabled = true;
    btnPar.disabled = true;
    term.textContent = "방식 B: Promise.all을 가동하여 3개 위젯 데이터를 동시 병렬 요청합니다...\n";

    const visual = runTimerVisual(barAsync, textAsync, 1.2); // 최장 시간인 1.2초 예상
    const startTime = performance.now();

    // 3개 위젯 동시 로딩 상태 점등
    const widgets = [wProfile, wSales, wNotice];
    const statuses = [wProfileStatus, wSalesStatus, wNoticeStatus];
    widgets.forEach(w => w.className = "widget loading");
    statuses.forEach(s => {
      s.textContent = "로딩 중...";
      s.style.color = "#ffb703";
    });

    // 3개의 독립 약속들을 배열에 담아 동시에 출발!
    const profilePromise = fetchProfile();
    const salesPromise = fetchSales();
    const noticePromise = fetchNotice();

    Promise.all([profilePromise, salesPromise, noticePromise])
      .then(([profileData, salesData, noticeData]) => {
        // 모든 Promise가 완료되면 아래가 일괄 실행됩니다.
        wProfile.className = "widget loaded";
        wProfileVal.textContent = profileData.name;
        wProfileStatus.textContent = profileData.grade;
        wProfileStatus.style.color = "#2a9d8f";

        wSales.className = "widget loaded";
        wSalesVal.textContent = salesData.revenue;
        wSalesStatus.textContent = `총 ${salesData.count}`;
        wSalesStatus.style.color = "#2a9d8f";

        wNotice.className = "widget loaded";
        wNoticeVal.textContent = noticeData.title;
        wNoticeStatus.textContent = noticeData.date;
        wNoticeStatus.style.color = "#2a9d8f";

        term.textContent += `- [병렬 완료] 모든 위젯 리스폰스 수집 성공\n`;

        const duration = ((performance.now() - startTime) / 1000).toFixed(2);
        visual.stop();

        term.innerHTML += `
\n[Promise.all 병렬 요청 방식 결과]
- 3개 위젯 데이터 획득 최종 소요 시간: ${duration}초
- 상태: 3가지 비동기 요청을 동시에 전송하여 대기 시간을 병렬로 압축했습니다. 전체 소요 시간이 가장 오랫동안 걸린 단일 작업인 '매출 통계 그래프(1.2초)' 시간으로 전량 수렴하여 렌더링 성능이 약 2배 이상 혁신적으로 상승했습니다.
        `;
      })
      .catch((error) => {
        visual.stop();
        term.textContent += `\n[오류] 병렬 통신 처리 중 실패 발생: ${error.message}\n`;
      })
      .finally(() => {
        btnSeq.disabled = false;
        btnPar.disabled = false;
      });
  });
}
