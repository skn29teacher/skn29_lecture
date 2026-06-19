/**
 * ==========================================================================
 * ES6 기초 문법 (main_01.js) - 풍부화 및 심화 검증 코드
 * 학습 주제: var vs let/const, 화살표 함수 this 해결책, 삼항 연산 결합 템플릿 리터럴
 * ==========================================================================
 */

document.addEventListener("DOMContentLoaded", () => {
  // DOM 출력용 터미널 및 컨테이너 선택
  const termScope = document.getElementById("term-scope");
  const termConst = document.getElementById("term-const");
  const termThis = document.getElementById("term-this");
  const profileContainer = document.getElementById("profile-card-container");

  // --------------------------------------------------------------------------
  // [1] var vs let/const 블록 스코프 및 TDZ, 루프 오염 실증
  // --------------------------------------------------------------------------

  // 1-A. var 변수 블록 탈출 실증
  document.getElementById("btn-var-scope")?.addEventListener("click", () => {
    if (true) {
      var escapedVar = "var는 함수 스코프라 블록 외부로 유출됩니다.";
    }
    termScope.textContent = `블록 내부에서 var로 선언한 변수 호출 성공:\n-> "${escapedVar}"\n\n이처럼 var는 if나 for 블록 밖에서도 살아남아 전역 오염을 유발합니다.`;
  });

  // 1-B. let/const 블록 격리 및 TDZ 오류 실무 재현
  document.getElementById("btn-let-scope")?.addEventListener("click", () => {
    let errorMessage = "";
    
    // 블록 스코프 테스트
    try {
      if (true) {
        let isolatedLet = "let은 블록 내부에 격리됩니다.";
      }
      // 블록 밖에서 isolatedLet 호출 시도 (ReferenceError 발생 기대)
      console.log(isolatedLet);
    } catch (e) {
      errorMessage += `[블록 외부 참조 에러] let/const는 블록 밖에서 읽을 수 없습니다.\n오류메시지: ${e.message}\n\n`;
    }

    // TDZ (Temporal Dead Zone) 선언 전 호출 테스트
    try {
      // 선언 전 변수 호출 시도
      console.log(tdzVariable);
      let tdzVariable = "나중에 선언된 let 변수";
    } catch (e) {
      errorMessage += `[TDZ 참조 에러] let/const는 호이스팅은 되지만 초기화 전에 참조 불가 영역(TDZ)에 묶여 에러를 냅니다.\n오류메시지: ${e.message}`;
    }

    termScope.textContent = errorMessage;
  });

  // 1-C. for 루프 var 클로저 오염 현상 실증
  document.getElementById("btn-loop-var")?.addEventListener("click", () => {
    termScope.textContent = "var 루프 비동기 출력 작동 중... (콘솔 로그 및 아래 결과 확인)\n";
    
    // var로 선언한 인덱스는 루프 완료 시점에 3으로 전역 수렴합니다.
    for (var i = 0; i < 3; i++) {
      // 100ms 뒤 작동하는 비동기 함수 실행
      setTimeout(() => {
        termScope.textContent += `[var 출력] 비동기 콜백 시점의 인덱스 i 값: ${i}\n`;
        console.log(`[var 오염 로그] 인덱스 i: ${i}`);
      }, 100);
    }
    // 이 현상은 모든 콜백 함수가 하나의 공유된 i 변수를 참조하기 때문에 발생합니다.
  });

  // 1-D. for 루프 let 개별 격리로 문제 해결 실증
  document.getElementById("btn-loop-let")?.addEventListener("click", () => {
    termScope.textContent = "let 루프 비동기 출력 작동 중... (정상 출력 확인)\n";
    
    // let으로 선언한 인덱스는 루프의 회차마다 독립적인 블록 스코프 메모리를 격리 할당합니다.
    for (let k = 0; k < 3; k++) {
      setTimeout(() => {
        termScope.textContent += `[let 출력] 비동기 콜백 시점의 인덱스 k 값: ${k}\n`;
        console.log(`[let 안전 로그] 인덱스 k: ${k}`);
      }, 100);
    }
  });

  // --------------------------------------------------------------------------
  // [2] const 객체의 얕은 변경 제어 및 Object.freeze() 동결 실증
  // --------------------------------------------------------------------------

  // 2-A. const 객체 속성 수정
  document.getElementById("btn-const-modify")?.addEventListener("click", () => {
    // const는 객체의 참조 주소값의 재할당을 막을 뿐 내부 속성 조작은 차단하지 못합니다.
    const mutableUser = { name: "홍길동", level: "초급" };
    
    // 속성 수정 및 추가 시도
    mutableUser.level = "중급";
    mutableUser.newSkill = "JavaScript ES6";
    
    termConst.textContent = `const 객체 속성 수정 결과:\n${JSON.stringify(mutableUser, null, 2)}\n\n(참조 주소 자체를 바꾸는 mutableUser = {} 형태의 재할당만 불가능할 뿐 내부 프로퍼티 제어는 차단되지 않음을 증명합니다.)`;
  });

  // 2-B. Object.freeze() 동결 및 차단 검증
  document.getElementById("btn-const-freeze")?.addEventListener("click", () => {
    // strict mode를 활성화하여 동결된 객체 수정 시 에러가 나도록 유도
    "use strict";

    const frozenUser = { name: "이순신", role: "장군" };
    
    // 객체 물리적 동결
    Object.freeze(frozenUser);
    
    let freezeLog = `객체 동결 성공 여부: ${Object.isFrozen(frozenUser) ? "동결 완료" : "동결 실패"}\n`;
    
    try {
      // 동결된 객체의 프로퍼티 조작 시도 (에러 또는 변경 무시)
      frozenUser.role = "영웅";
      
      // non-strict mode에서는 에러가 안 날 수 있으므로 값의 변화가 없는지 이중 체크
      if (frozenUser.role !== "영웅") {
        freezeLog += `에러 없이 통과되었으나 수정 사항이 반영되지 않았습니다. 현재 role: ${frozenUser.role}`;
      }
    } catch (e) {
      freezeLog += `수정 에러 발생 (Strict 모드 감지): ${e.message}\n현재 값 보존 상태: role = ${frozenUser.role}`;
    }
    
    termConst.textContent = freezeLog;
  });

  // --------------------------------------------------------------------------
  // [3] 일반 함수 vs 화살표 함수 this 바인딩 격차 실증
  // --------------------------------------------------------------------------

  // 3-A. 일반 함수 비동기 setTimeout this 유실
  document.getElementById("btn-this-regular")?.addEventListener("click", () => {
    termThis.textContent = "일반 함수 비동기 호출 실행 중... 100ms 대기\n";
    
    const regularContextObj = {
      courseName: "모던 프론트엔드 실무과정",
      
      startCourse: function() {
        // 일반 함수는 메서드로 호출될 때 this가 regularContextObj를 가리킵니다.
        // 하지만 내부 비동기 콜백(일반 function)으로 감싸져 실행되면 호출 주체가 유실되어 전역 또는 undefined로 꼬입니다.
        setTimeout(function() {
          try {
            // this.courseName은 undefined가 되어 에러 상황을 유도합니다.
            const result = this.courseName ?? "this를 잃어버려 찾을 수 없습니다.";
            termThis.textContent += `일반 함수 내부의 this.courseName 결과: "${result}"\n`;
          } catch (e) {
            termThis.textContent += `에러 발생: ${e.message}\n`;
          }
        }, 100);
      }
    };
    
    regularContextObj.startCourse();
  });

  // 3-B. 화살표 함수 비동기 setTimeout this 자동 유지
  document.getElementById("btn-this-arrow")?.addEventListener("click", () => {
    termThis.textContent = "화살표 함수 비동기 호출 실행 중... 100ms 대기\n";
    
    const arrowContextObj = {
      courseName: "모던 프론트엔드 실무과정",
      
      startCourse: function() {
        // 화살표 함수는 스스로의 this를 갖지 않고 정의되는 시점의 상위 영역인 startCourse 메서드 스코프의 this(arrowContextObj)를 자동 상속합니다.
        setTimeout(() => {
          try {
            const result = this.courseName;
            termThis.textContent += `화살표 함수 내부의 this.courseName 결과: "${result}"\n(this 주소가 안전하게 전달되었습니다.)\n`;
          } catch (e) {
            termThis.textContent += `에러 발생: ${e.message}\n`;
          }
        }, 100);
      }
    };
    
    arrowContextObj.startCourse();
  });

  // --------------------------------------------------------------------------
  // [4] 종합 실습: 화살표 함수 + 템플릿 리터럴 + 고차함수를 조합한 카드 그리드 빌드
  // --------------------------------------------------------------------------

  // 가상의 다중 API 응답 회원 리스트
  const mockApiUsers = [
    { name: "김민수", role: "Frontend Developer", bio: "웹 환경에서 모던 디자인과 최적화를 고려하여 프론트엔드를 개발합니다.", isPremium: true },
    { name: "박영희", role: "UI/UX Designer", bio: "사용자 중심의 가동성과 프리미엄 스타일을 우선하여 설계합니다.", isPremium: false },
    { name: "최철수", role: "Product Manager", bio: "협업 도구와 일정 캡슐화를 통해 전체 프로젝트 마일스톤을 리드합니다.", isPremium: true }
  ];

  // 화살표 함수와 삼항 연산 결합 템플릿 리터럴을 활용한 HTML 단일 카드 템플릿 생성기
  // 1. 매개변수가 1개(user)이므로 소괄호 생략 가능
  // 2. 삼항 연산자를 내장하여 프리미엄 등급 여부에 따른 배지를 템플릿 내에 조건부로 바로 렌더링
  const generateUserCardHtml = user => `
    <div class="user-card">
      ${user.isPremium ? `<span class="badge-premium">Premium</span>` : ""}
      <h3 class="user-name">${user.name}</h3>
      <span class="user-role">${user.role}</span>
      <p class="user-bio">${user.bio}</p>
    </div>
  `;

  document.getElementById("btn-render-profiles")?.addEventListener("click", () => {
    // 기존에 컨테이너 내부에 있던 안내문구 청소
    profileContainer.innerHTML = "";
    
    // 고차배열 함수인 map을 호출하고 콜백에 화살표 함수 generateUserCardHtml를 연동하여 카드 조각 배열 완성
    // 이후 join("")을 통해 하나의 완성된 큰 문자열 조각으로 변환하여 innerHTML 주입
    const fullCardsMarkup = mockApiUsers.map(user => generateUserCardHtml(user)).join("");
    
    profileContainer.innerHTML = fullCardsMarkup;
    console.log("종합 실습: 다중 회원 데이터가 화살표 함수와 템플릿 리터럴 융합을 통해 화면에 렌더링되었습니다.");
  });
});
