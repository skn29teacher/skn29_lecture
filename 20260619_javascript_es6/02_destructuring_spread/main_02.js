/**
 * ==========================================================================
 * 구조분해 할당 및 전개/나머지 연산자 (main_02.js) - 심화 코드
 * 학습 주제: 중첩 객체 분해, 얕은 복사 오염과 structuredClone, 나머지 매개변수 가변 연산
 * ==========================================================================
 */

document.addEventListener("DOMContentLoaded", () => {
  // DOM 출력 타깃 캐싱
  const termDestruct = document.getElementById("term-destruct");
  const termCopy = document.getElementById("term-copy");
  const termRest = document.getElementById("term-rest");
  const productContainer = document.getElementById("product-card-container");

  // --------------------------------------------------------------------------
  // [1] 구조분해 할당: Swap 및 중첩 객체와 함수 매개변수 분해
  // --------------------------------------------------------------------------

  // 1-A. 변수 값 맞교환 (Swap)
  document.getElementById("btn-destruct-swap")?.addEventListener("click", () => {
    let activeColor = "블루";
    let standbyColor = "레드";
    
    let beforeSwap = `교환 전 -> 활성색상: ${activeColor}, 대기색상: ${standbyColor}\n`;
    
    // 구조분해 할당 문법을 통한 임시 변수 없는 변수 스왑
    [activeColor, standbyColor] = [standbyColor, activeColor];
    
    let afterSwap = `교환 후 -> 활성색상: ${activeColor}, 대기색상: ${standbyColor}`;
    
    termDestruct.textContent = beforeSwap + afterSwap;
  });

  // 1-B. 중첩 객체 분해 및 함수 매개변수 분해 패턴
  document.getElementById("btn-destruct-nested")?.addEventListener("click", () => {
    const memberData = {
      username: "김철수",
      rank: "골드회원",
      contact: {
        email: "cheolsoo@mail.com",
        phone: "010-1234-5678"
      }
    };

    // 1단계: 중첩 구조분해 할당을 통해 contact 하위의 email 값을 단일 변수로 획득
    const { username, contact: { email } } = memberData;

    // 2단계: 함수 매개변수단에서 직접 구조분해를 수행하는 함수 정의
    const renderSummary = ({ rank, contact: { phone } }) => {
      return `회원등급: ${rank}, 연락처: ${phone}`;
    };

    const summaryText = renderSummary(memberData);

    termDestruct.textContent = `중첩 분해로 추출한 이름: ${username}\n중첩 분해로 추출한 이메일: ${email}\n\n매개변수 분해 함수 호출 결과:\n-> ${summaryText}`;
  });

  // --------------------------------------------------------------------------
  // [2] 전개 연산자 얕은 복사(Shallow Copy) 오염 vs structuredClone 깊은 복사(Deep Copy)
  // --------------------------------------------------------------------------

  // 공통 검증 데이터 원본 객체 정의
  const getOriginalProduct = () => ({
    title: "가죽 숄더백",
    price: 89000,
    specs: {
      color: "브라운",
      material: "천연가죽"
    }
  });

  // 2-A. 전개 연산자 얕은 복사 사본 수정으로 원본 오염 발생 유도
  document.getElementById("btn-shallow-dirty")?.addEventListener("click", () => {
    const original = getOriginalProduct();
    
    // 전개 연산자(...)를 통한 얕은 복사 실행 (specs 하위 객체는 주소 복사됨)
    const shallowCopy = { ...original };
    
    // 사본의 중첩 객체 속성 수정
    shallowCopy.specs.color = "블랙";
    shallowCopy.price = 99000; // 1단계 값은 독립 수정되어 원본에 영향 없음

    termCopy.textContent = `[얕은 복사 오염 검증]\n` +
      `사본의 specs.color를 "블랙"으로 수정하고 price를 99000으로 수정했습니다.\n\n` +
      `원본 객체 상세 (오염 발생):\n` +
      `- 원본 가격: ${original.price}원 (1단계 변조 없음 - 안전)\n` +
      `- 원본 색상: ${original.specs.color} (2단계 오염됨 - 버그 발생)\n\n` +
      `사본 객체 상세:\n` +
      `- 사본 가격: ${shallowCopy.price}원\n` +
      `- 사본 색상: ${shallowCopy.specs.color}`;
  });

  // 2-B. structuredClone을 통한 깊은 복사 완벽 방어 실증
  document.getElementById("btn-deep-safe")?.addEventListener("click", () => {
    const original = getOriginalProduct();
    
    // structuredClone API를 이용한 깊은 복사 실행 (중첩 구조까지 완전 격리)
    const deepCopy = structuredClone(original);
    
    // 사본의 중첩 객체 속성 수정
    deepCopy.specs.color = "화이트";
    deepCopy.price = 120000;

    termCopy.textContent = `[깊은 복사 안전 검증]\n` +
      `structuredClone 사본의 specs.color를 "화이트"로 수정하고 price를 120000으로 수정했습니다.\n\n` +
      `원본 객체 상세 (오염 차단):\n` +
      `- 원본 가격: ${original.price}원 (보존)\n` +
      `- 원본 색상: ${original.specs.color} (브라운 원본값 유지 - 안전)\n\n` +
      `사본 객체 상세:\n` +
      `- 사본 가격: ${deepCopy.price}원\n` +
      `- 사본 색상: ${deepCopy.specs.color}`;
  });

  // --------------------------------------------------------------------------
  // [3] 나머지 매개변수(...rest)와 전개 연산자 결합 가변 인자 연산
  // --------------------------------------------------------------------------
  document.getElementById("btn-rest-calc")?.addEventListener("click", () => {
    const rawValue = document.getElementById("input-numbers").value;
    
    // 입력된 쉼표 문자열을 분할하여 정밀한 숫자 배열로 파싱
    const parsedNumbers = rawValue.split(",")
      .map(str => Number(str.trim()))
      .filter(num => !isNaN(num));

    // 나머지 매개변수를 사용하여 임의 개수의 인자들을 배열로 수거하는 함수 정의
    const calculateSum = (...args) => {
      // args는 수거된 모든 실인자들의 순수 배열입니다.
      return args.reduce((accumulator, current) => accumulator + current, 0);
    };

    // 파싱된 배열을 전개 연산자(...)로 풀어서 실인자로 전달하여 호출
    const totalSum = calculateSum(...parsedNumbers);

    termRest.textContent = `파싱된 배열 데이터: [${parsedNumbers.join(", ")}]\n` +
      `전개 연산자로 전달 및 나머지 매개변수로 수합 후 reduce 합계 연산 결과:\n` +
      `-> 합계: ${totalSum}`;
  });

  // --------------------------------------------------------------------------
  // [4] 종합 실습: 전개 연산자 데이터 병합 및 구조분해 할당 렌더링
  // --------------------------------------------------------------------------
  const baseProducts = [
    { id: "p-001", title: "어반 데일리 백팩", price: 68000, specs: { color: "그레이", brand: "Urban" } },
    { id: "p-002", title: "슬림 미니 가죽 지갑", price: 42000, specs: { color: "블랙", brand: "Classic" } }
  ];

  document.getElementById("btn-render-products")?.addEventListener("click", () => {
    productContainer.innerHTML = "";

    // 1단계: 전개 연산자(...)를 이용해 불변성을 유지하며 신규 상품 객체 목록 병합
    const mergedList = [
      ...baseProducts,
      { id: "p-003", title: "초경량 패킹 우산", price: 24000, specs: { color: "네이비", brand: "WeatherGo" } }
    ];

    // 2단계: 배열 요소를 순회하며 객체 구조분해 할당 및 나머지 매개변수(...meta) 결합 수행
    const cardsMarkup = mergedList.map(product => {
      // specs 속성은 중첩 구조분해로 바로 꺼내고, id 등의 남은 속성은 meta 객체로 안전하게 수합
      const { title, price, specs: { color, brand }, ...meta } = product;
      
      // 3단계: 템플릿 리터럴 멀티라인을 통해 가독성 높은 HTML 조립 후 반환
      return `
        <div class="product-card">
          <h3 class="product-title">${title}</h3>
          <div class="product-price">${price.toLocaleString()}원</div>
          <div class="product-meta">
            색상: ${color}<br>
            브랜드: ${brand}<br>
            고유식별키: ${meta.id} (나머지 매개변수 수거 객체로 렌더링)
          </div>
        </div>
      `;
    }).join("");

    productContainer.innerHTML = cardsMarkup;
    console.log("종합 실습: 전개 연산자 및 구조분해 할당을 이용한 상품 카드 리스트 빌드가 정상 작동했습니다.");
  });
});
