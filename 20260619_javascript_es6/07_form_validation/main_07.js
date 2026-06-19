/**
 * ==========================================================================
 * 폼 이벤트와 입력 유효성 검사 (main_07.js) - 확장형 검증 코드
 * 학습 주제: preventDefault, input vs change 타이밍 대조, ?. & ?? 예외 방어
 * ==========================================================================
 */

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("contact-form");
  const nameInput = document.getElementById("contact-name");
  const emailInput = document.getElementById("contact-email");
  const subjectSelect = document.getElementById("contact-subject");
  
  const successBanner = document.getElementById("success-banner");

  // ------------------------------------------------------------------------
  // [검증 1] input vs change 이벤트 렌더링 타이밍 대조 실증
  // ------------------------------------------------------------------------
  let inputCount = 0;
  let changeCount = 0;

  nameInput?.addEventListener("input", (event) => {
    inputCount++;
    console.log(`[이벤트 A: input] 글자를 칠 때마다 즉각 발동! (${inputCount}회) -> 입력 값: "${event.target.value}"`);
    
    // 실시간 글자수 유효성 간이 검증
    const nameError = document.getElementById("name-error");
    if (event.target.value.length > 0 && event.target.value.length < 2) {
      nameInput.classList.add("invalid");
      nameError.style.display = "block";
    } else {
      nameInput.classList.remove("invalid");
      nameError.style.display = "none";
    }
  });

  nameInput?.addEventListener("change", (event) => {
    changeCount++;
    console.log(`[이벤트 B: change] 포커스가 입력창을 빠져나가거나 엔터를 칠 때만 최종 발동! (${changeCount}회) -> 값: "${event.target.value}"`);
  });

  // ------------------------------------------------------------------------
  // [검증 2] 실시간 이메일 규칙 정합성 검증 (input 이벤트)
  // ------------------------------------------------------------------------
  emailInput?.addEventListener("input", (event) => {
    const value = event.target.value;
    const emailError = document.getElementById("email-error");

    if (value.length > 0 && !value.includes("@")) {
      emailInput.classList.add("invalid");
      emailError.style.display = "block";
    } else {
      emailInput.classList.remove("invalid");
      emailError.style.display = "none";
    }
  });

  // ------------------------------------------------------------------------
  // [검증 3] 옵셔널 체이닝(?.) 및 널 병합 연산자(??)의 예외 방어 실증
  // ------------------------------------------------------------------------
  console.log("\n--- [실증 3] 옵셔널 체이닝(?.) & 널 병합(??) 안전성 검증 ---");
  
  const nonexistentInput = document.getElementById("fake-input-id");
  
  try {
    const value = nonexistentInput.value; 
  } catch (e) {
    console.warn("구식 획득 실패 (null 객체 속성 참조 불가):", e.message);
  }

  const safeValue = nonexistentInput?.value ?? "기본값 (미입력)";
  console.log("옵셔널 체이닝 + 널 병합을 통한 안전 획득 값:", safeValue);

  // ------------------------------------------------------------------------
  // 4. 폼 전송 종합 벨리데이션
  // ------------------------------------------------------------------------
  form?.addEventListener("submit", (event) => {
    event.preventDefault();

    const nameVal = nameInput?.value ?? "";
    const emailVal = emailInput?.value ?? "";
    const subjectVal = subjectSelect?.value ?? "";

    let isFormValid = true;

    // 이름 검사
    const nameError = document.getElementById("name-error");
    if (nameVal.length < 2) {
      nameInput.classList.add("invalid");
      nameError.style.display = "block";
      isFormValid = false;
    }

    // 이메일 검사
    const emailError = document.getElementById("email-error");
    if (!emailVal.includes("@")) {
      emailInput.classList.add("invalid");
      emailError.style.display = "block";
      isFormValid = false;
    }

    // 유형 검사
    const subjectError = document.getElementById("subject-error");
    if (subjectVal === "") {
      subjectSelect.classList.add("invalid");
      subjectError.style.display = "block";
      isFormValid = false;
    } else {
      subjectSelect.classList.remove("invalid");
      subjectError.style.display = "none";
    }

    // 최종 결과 노출 및 페이지 리다이렉션 전송
    if (isFormValid) {
      successBanner.style.display = "block";
      console.log("--- [폼 검증 성공 데이터 수거] ---");
      console.log(`이름: ${nameVal}, 이메일: ${emailVal}, 유형: ${subjectVal}`);
      
      // 안전하게 한글 특수문자를 인코딩하여 가입 완료 페이지 파라미터 조립
      const redirectUrl = `welcome_07.html?name=${encodeURIComponent(nameVal)}&email=${encodeURIComponent(emailVal)}&subject=${encodeURIComponent(subjectVal)}`;
      
      // 1초 후 가입 환영 페이지로 안전하게 정보 이동 처리
      setTimeout(() => {
        window.location.href = redirectUrl;
      }, 1000);

      form.reset();
      inputCount = 0;
      changeCount = 0;
    } else {
      successBanner.style.display = "none";
      console.warn("폼 입력 항목 중 검증되지 않은 오류가 남아있습니다.");
    }
  });
});
