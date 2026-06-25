# 비동기 카드 UI 스타일 동적 배정

비동기 통신을 통해 클라이언트 사이드에서 데이터를 렌더링(CSR)할 때, 각 데이터의 순번(Index)을 판단하여 스타일을 교대로 배정하는 프론트엔드 제어 기법과 웹 애플리케이션의 세련미를 높여주는 정적 CSS 애니메이션 및 Hover 시각 효과 구축 방법을 학습합니다.

---

## 1. 클라이언트 사이드 렌더링(CSR)에서의 동적 스타일링

서버 사이드 렌더링(SSR) 환경에서는 DTL의 `{% cycle %}` 태그를 활용해 HTML을 구울 때 스타일 클래스를 교대로 지정해 줄 수 있었습니다. 하지만 데이터를 API로 비동기 수신하여 자바스크립트로 화면을 갱신하는 CSR 환경에서는 브라우저의 DOM 생성 사이클에 직접 개입하여 동적으로 연산하여 클래스를 추가해 주어야 합니다.

- **인덱스 활용**: `Array.prototype.forEach` 루프 등에서 현재 순회 중인 객체의 인덱스(Index) 매개변수를 활용합니다.
- **조건부 삼항 연산자**: `index % 2 === 0` 조건을 판별하여 짝수(even) 행과 홀수(odd) 행에 각각 매칭될 전용 스타일 클래스를 자바스크립트 템플릿 리터럴 내에 할당합니다.

---

## 2. 세련된 인터랙션을 위한 정적 CSS 정의

카드를 터치하거나 마우스 호버할 때 입체적인 들림 효과와 부드러운 섀도우 전환을 연출하기 위해 CSS 트랜지션을 조율합니다.

- **`transition`**: 애니메이션 대상을 특정하고 완급 조절 곡선(`cubic-bezier`)을 선언하여 끊김 없는 자연스러운 프레임 변화를 보장합니다.
- **`transform: translateY()`**: 요소를 Y축 방향으로 수직 이동시켜 가상으로 카드가 떠오르는 시각적 깊이를 부여합니다.
- **`box-shadow`**: 호버 시 그림자의 반경과 확산 정도를 확장하여 부양 효과의 설득력을 높여줍니다.

---

## 3. 코드 구성 분석

### 1단계: 동적 카드 렌더링 자바스크립트 구현
파일명: `todos/static/todos/js/app.js`
```javascript
const renderTodos = (todos) => {
    // ... (중략)
    todoListContainer.innerHTML = '';
    
    // 1. forEach 루프에 index 인자를 공급받아 순서 식별
    todos.forEach((todo, index) => {
        const card = document.createElement('div');
        
        // 2. 인덱스 번호를 바탕으로 card-even 또는 card-odd 클래스 결정
        const rowClass = index % 2 === 0 ? 'card-even' : 'card-odd';
        
        // 3. 동적 계산된 클래스를 카드 엘리먼트 클래스 리스트에 주입
        card.className = `todo-card ${todo.is_completed ? 'completed' : ''} ${rowClass}`;
        
        const createdDate = new Date(todo.created_at);
        const dateString = `${createdDate.getFullYear()}-${String(createdDate.getMonth()+1).padStart(2, '0')}-${String(createdDate.getDate()).padStart(2, '0')} ${String(createdDate.getHours()).padStart(2, '0')}:${String(createdDate.getMinutes()).padStart(2, '0')}`;

        card.innerHTML = `
            <div class="todo-card-header">
                <button class="status-badge btn-toggle" data-id="${todo.id}" data-completed="${todo.is_completed}" style="border: none; cursor: pointer;">
                    ${todo.is_completed ? '완료' : '대기중'}
                </button>
                <span class="todo-date">${dateString}</span>
            </div>
            <h3 class="todo-title">${todo.title}</h3>
            ${todo.content ? `<p class="todo-body">${todo.content}</p>` : ''}
            ${todo.image ? `<div class="todo-image" style="margin-top: 10px;"><img src="${todo.image}" alt="${todo.title}" style="width: 100%; max-height: 150px; object-fit: cover; border-radius: 6px;"></div>` : ''}
            <div class="todo-actions">
                <button class="btn-text btn-delete-spa" data-id="${todo.id}" style="color: #ef4444;">삭제</button>
            </div>
        `;
        todoListContainer.appendChild(card);
    });
    attachCardListeners();
};
```

### 2단계: 스타일시트 작성
파일명: `todos/static/todos/css/style.css`
```css
/* 비동기 렌더링 카드 스타일 고도화 */

/* 4. 짝수 인덱스 카드: 기본 화이트 배경에 브랜드 테마 주컬러 좌측 보더 설정 */
.card-even {
    background-color: #ffffff;
    border-left: 4px solid var(--primary-color);
}

/* 5. 홀수 인덱스 카드: 미세한 연회색 배경에 세컨더리 퍼플 컬러 좌측 보더 설정 */
.card-odd {
    background-color: #fafbfc;
    border-left: 4px solid #818cf8;
}

/* 6. 호버 시 3D 팝업 인터랙션 및 부드러운 곡선 효과 지정 */
.todo-card {
    transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
}

.todo-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.08) !important;
}
```

이 조합을 통해 사용자는 새로운 할 일을 등록하거나 정렬 순서를 바꿀 때마다 화면 전체를 새로 그리는 불쾌감 없이, 물 흐르듯 교차 배정되는 파스텔 톤의 카드와 고급스럽게 부상하는 모던 호버 피드백을 실시간으로 감상하게 됩니다.
