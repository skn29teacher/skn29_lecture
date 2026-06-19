/**
 * ==========================================================================
 * 이벤트 리스너 기초 (main_05.js) 
 * 학습 주제: 로딩 시점 대조, 복수 리스너 연쇄 구동, target vs currentTarget, 키보드 디코딩
 * ==========================================================================
 */

// 로딩 타임스탬프 기록 시작 (성능 측정을 위해 페이지 시작 즉시 구동)
const initialTime = performance.now();
let domReadyTime = 0;

// --------------------------------------------------------------------------
// [1] DOMContentLoaded 안전 로딩 보증 실증
// --------------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  domReadyTime = performance.now() - initialTime;
  
  // DOMContentLoaded 완료 후 이벤트 초기화 구동 시작
  initEvents();
});

// window.load는 이미지와 기타 하위 외부 자원 로드 완료 시 구동됩니다.
window.addEventListener("load", () => {
  const windowLoadTime = performance.now() - initialTime;
  const timingBox = document.getElementById("load-timing-box");
  if (timingBox) {
    timingBox.innerHTML = `[로딩 타이밍 정밀 대조 결과]<br>` +
      `- DOMContentLoaded 소요 시간: <strong>${domReadyTime.toFixed(1)}ms</strong> (HTML 구조 파싱 완료 즉시 작동)<br>` +
      `- window load 소요 시간: <strong>${windowLoadTime.toFixed(1)}ms</strong> (이미지 및 자원 로딩 최종 완료 시점)`;
  }
});

// 초기화 함수
function initEvents() {
  // DOM 타깃 캐싱
  const termMultiple = document.getElementById("term-multiple");
  const termTargetCompare = document.getElementById("term-target-compare");
  const termKeyboard = document.getElementById("term-keyboard");

  // --------------------------------------------------------------------------
  // [2] addEventListener 다중 리스너 등록 및 연쇄 구동
  // --------------------------------------------------------------------------
  const multiBtn = document.getElementById("btn-multiple-listeners");
  let runCount = 0;

  // 핸들러 A: 카운팅 로직
  const handleCounting = () => {
    runCount++;
    termMultiple.textContent = `[핸들러 A] 클릭 카운트 누적 작동: ${runCount}회\n`;
  };

  // 핸들러 B: 버튼 디자인 변형 (동적 시각 효과)
  const handleColorShift = (event) => {
    const randomHex = Math.floor(Math.random()*16777215).toString(16);
    event.currentTarget.style.borderColor = `#${randomHex}`;
    termMultiple.textContent += `[핸들러 B] 버튼 외곽선 색상을 #${randomHex}로 변조했습니다.\n`;
  };

  // 핸들러 C: 콘솔 로깅 분리
  const handleConsoleLog = () => {
    console.log(`[다중 리스너 연쇄 동작] ${runCount}회차 연쇄 핸들링 완료.`);
    termMultiple.textContent += `[핸들러 C] 브라우저 콘솔에 디버깅 정보 기록 완료.`;
  };

  if (multiBtn) {
    // 단일 버튼에 3개의 별개 리스너를 결합해도 덮어쓰지 않고 순차 구동됨
    multiBtn.addEventListener("click", handleCounting);
    multiBtn.addEventListener("click", handleColorShift);
    multiBtn.addEventListener("click", handleConsoleLog);
  }

  // --------------------------------------------------------------------------
  // [3] event.target vs event.currentTarget 시각 대조
  // --------------------------------------------------------------------------
  const nestedTrigger = document.getElementById("btn-nested-trigger");
  const parentContainer = document.getElementById("event-parent-container");

  // 공통 정보 출력 함수
  const logClickDetails = (event, listenerName) => {
    const targetInfo = `${event.target.tagName.toLowerCase()}${event.target.id ? '#' + event.target.id : ''}`;
    const currentTargetInfo = `${event.currentTarget.tagName.toLowerCase()}${event.currentTarget.id ? '#' + event.currentTarget.id : ''}`;
    
    return `[${listenerName} 감시 영역]\n` +
      `- 실제 마우스가 강타한 물리 타깃 (event.target): <span style="color:#ff4757; font-weight:bold;">${targetInfo}</span>\n` +
      `- 이벤트 감시 리스너가 걸린 대상 (event.currentTarget): <span style="color:#2ed573; font-weight:bold;">${currentTargetInfo}</span>\n\n`;
  };

  // A. 중첩 버튼 자체에 리스너 바인딩
  nestedTrigger?.addEventListener("click", (event) => {
    termTargetCompare.innerHTML = logClickDetails(event, "버튼 자체 리스너");
  });

  // B. 상위 부모 컨테이너(감시자 영역)에도 버블링 추적 리스너 바인딩
  parentContainer?.addEventListener("click", (event) => {
    // 버튼 클릭 시 이벤트가 위로 전파(버블링)되어 부모 리스너도 깨어납니다.
    termTargetCompare.innerHTML += logClickDetails(event, "부모 컨테이너 리스너");
    
    // 부모 컨테이너 외곽선에 실시간 하이라이트 효과 부여
    parentContainer.style.borderColor = "#4361ee";
    setTimeout(() => {
      parentContainer.style.borderColor = "#cbd5e1";
    }, 400);
  });

  // --------------------------------------------------------------------------
  // [4] 실시간 키보드 이벤트 메타데이터 디코더
  // --------------------------------------------------------------------------
  const kbMonitor = document.getElementById("input-keyboard-monitor");
  const kbKey = document.getElementById("kb-key");
  const kbCode = document.getElementById("kb-code");
  const kbMods = document.getElementById("kb-mods");

  kbMonitor?.addEventListener("keydown", (event) => {
    // 1단계: 주요 메타데이터 추출 및 대시보드 갱신
    kbKey.textContent = event.key === " " ? "Space" : event.key;
    kbCode.textContent = event.code;
    
    // 2단계: 조합 보조 키 상태 판별
    let modifiers = [];
    if (event.shiftKey) modifiers.push("Shift");
    if (event.ctrlKey) modifiers.push("Control");
    if (event.altKey) modifiers.push("Alt");
    kbMods.textContent = modifiers.length > 0 ? modifiers.join(" + ") : "없음";

    // 3단계: 이벤트 객체의 전체 가용한 메타 정보 텍스트 포맷팅 출력
    termKeyboard.textContent = `[Keyboard Event Details]\n` +
      `- event.key: "${event.key}" (문자열 값 형태)\n` +
      `- event.code: "${event.code}" (물리 키보드 자판 위치 코드)\n` +
      `- event.shiftKey: ${event.shiftKey}\n` +
      `- event.ctrlKey: ${event.ctrlKey}\n` +
      `- event.altKey: ${event.altKey}\n` +
      `- event.metaKey: ${event.metaKey} (OS 키)`;
  });
}
