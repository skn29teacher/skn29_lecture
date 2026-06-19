/**
 * ==========================================================================
 * 가입 완료 데이터 처리 (welcome_07.js)
 * 학습 주제: URLSearchParams 파라미터 파싱, ?. & ?? 예외 방어 실무 활용
 * ==========================================================================
 */

document.addEventListener("DOMContentLoaded", () => {
  // 1. 현재 브라우저 URL의 쿼리 스트링(파라미터) 부분 수거
  const queryString = window.location.search;
  
  // URLSearchParams API를 이용하여 키-값 분석 인스턴스 생성
  const urlParams = new URLSearchParams(queryString);

  // 2. 쿼리 파라미터에서 각 정보 추출
  // - urlParams 객체 혹은 메서드가 유실되었을 때를 대비해 ?. 옵셔널 체이닝을 활용
  // - 파라미터가 존재하지 않거나 null인 경우를 대비해 ?? 널 병합 연산자로 기본값 대입 방어
  const userName = urlParams?.get("name") ?? "익명 회원";
  const userEmail = urlParams?.get("email") ?? "미등록 이메일";
  const userSubjectRaw = urlParams?.get("subject") ?? "";

  // 3. 문의 유형 영문 코드를 친절한 한글로 변환
  let userSubject = "기타 문의";
  if (userSubjectRaw === "course") {
    userSubject = "수강 신청 문의";
  } else if (userSubjectRaw === "schedule") {
    userSubject = "일정 관련 문의";
  } else if (userSubjectRaw === "tech") {
    userSubject = "기술 질문";
  }

  // 4. 화면 DOM 요소 선택
  const nameEl = document.getElementById("welcome-name");
  const emailEl = document.getElementById("welcome-email");
  const subjectEl = document.getElementById("welcome-subject");

  // 화면 바인딩 처리 (옵셔널 체이닝으로 돔 유실 시에도 안전 방어)
  if (nameEl) nameEl.textContent = userName;
  if (emailEl) emailEl.textContent = userEmail;
  if (subjectEl) subjectEl.textContent = userSubject;

  console.log("--- [가입 환영 페이지 데이터 파싱 완료] ---");
  console.log(`파싱 수집 결과 -> 이름: ${userName}, 이메일: ${userEmail}, 문의유형: ${userSubject}`);
});
