# SPA 멀티파트 파일 비동기 전송

Single Page Application(SPA) 환경에서 웹 브라우저 새로고침 없이 비동기 방식(Fetch API)으로 데이터를 서버에 전송할 때, 이미지와 같은 바이너리 파일 데이터를 텍스트 데이터와 함께 묶어 안전하게 보내는 기법을 학습합니다. 

---

## 1. 비동기 파일 전송의 한계와 FormData API

기존의 단순 JSON 비동기 전송 방식은 텍스트 형태의 구조화된 데이터 송수신에 특화되어 있어 이미지나 문서 같은 이진(Binary) 데이터를 직접 담아 전송할 수 없습니다. 비동기 환경에서 파일을 전달하기 위해 자바스크립트의 **`FormData`** 표준 객체를 사용합니다.

### FormData 객체
- **정의**: HTML `<form>` 태그의 폼 전송 데이터를 동일하게 자바스크립트 객체 형태로 캡슐화해 주는 가상의 데이터 바구니입니다.
- **문법**: `const formData = new FormData(); formData.append('key', value);`
- **특징**: 단순 문자열뿐만 아니라, `<input type="file">`에서 획득한 파일 객체(`File`)를 그대로 추가하여 통째로 쏠 수 있습니다.

---

## 2. HTTP 요청 헤더 Content-Type 유의점

일반적인 비동기 POST 전송 시에는 서버가 데이터 형식을 인지할 수 있도록 요청 헤더에 `'Content-Type': 'application/json'` 등을 개발자가 명시적으로 작성합니다. 그러나 `FormData` 객체를 바디에 실어 보낼 때는 **`Content-Type` 헤더를 절대로 작성하지 말아야 합니다.**

- 헤더를 비워두면 웹 브라우저가 전송 데이터가 `FormData`임을 감지하고 자동으로 HTTP 요청 헤더에 `multipart/form-data; boundary=----WebKitFormBoundary...`와 같은 규격을 바운더리 해시값과 함께 정교하게 추가해 줍니다.
- 개발자가 수동으로 `'Content-Type': 'multipart/form-data'`로 작성해 버리면 필수적인 바운더리 정보가 누락되어 서버가 바이너리 데이터를 올바르게 파싱하지 못하고 업로드 실패 오류를 반환하게 됩니다.

---

## 3. 프론트엔드 비동기 연동 구현

비동기로 이미지 파일을 넘기고, 수신된 응답의 이미지 경로 주소를 바탕으로 DOM을 동적으로 조립하는 클라이언트 코드를 작성합니다.

### 1단계: HTML 폼 요소 추가
파일명: `todos/templates/todos/spa.html`
```html
<!-- 새 할일 추가 폼 내에 이미지 첨부 필드 배치 -->
<div class="form-group" style="gap: 6px;">
    <label class="form-label" style="font-size: 13px;">첨부 이미지</label>
    <input type="file" id="spa-image" class="form-input" accept="image/*">
</div>
```

### 2단계: Javascript 이벤트 핸들러 및 렌더링 구현
파일명: `todos/static/todos/js/app.js`
```javascript
document.addEventListener('DOMContentLoaded', () => {
    const todoListContainer = document.getElementById('spa-todo-list');
    const todoForm = document.getElementById('spa-todo-form');
    const titleInput = document.getElementById('spa-title');
    const contentInput = document.getElementById('spa-content');
    // 1. 파일 첨부 입력 요소 가져오기
    const imageInput = document.getElementById('spa-image');

    // 리스트 렌더링 함수 내 이미지 추가 로직
    const renderTodos = (todos) => {
        // ... (생략)
        todos.forEach(todo => {
            const card = document.createElement('div');
            card.className = `todo-card ${todo.is_completed ? 'completed' : ''}`;
            
            // 날짜 포맷팅 등 처리 생략
            
            // 2. 응답 데이터 내에 이미지 주소(todo.image)가 존재하는 경우 img 태그를 동적 주입
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

    // 폼 전송 비동기 이벤트 핸들러
    todoForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = titleInput.value.trim();
        const content = contentInput.value.trim();
        // 3. 첨부된 파일 객체 꺼내기
        const file = imageInput.files[0];

        if (!title) return;

        // 4. FormData 객체 생성 및 바이너리/텍스트 데이터 적재
        const formData = new FormData();
        formData.append('title', title);
        formData.append('content', content);
        if (file) {
            formData.append('image', file);
        }

        try {
            const response = await fetch(apiBaseUrl, {
                method: 'POST',
                headers: {
                    // Content-Type 헤더를 명시하지 않고 비워둡니다.
                    'X-CSRFToken': csrfToken
                },
                body: formData // Body에 FormData 전달
            });

            if (response.ok) {
                titleInput.value = '';
                contentInput.value = '';
                imageInput.value = ''; // 5. 파일 필드 리셋 처리
                loadTodos();
            } else {
                const errors = await response.json();
                alert(`저장 실패: ${JSON.stringify(errors)}`);
            }
        } catch (error) {
            console.error(error);
            alert('저장 중 통신 에러 발생');
        }
    });
});
```

- **`todo.image`**: DRF Serializer가 반환해 주는 완전한 URL(예: `/media/todos/images/example.png`)이 바인딩되므로, 클라이언트는 이 문자열을 `<img src="${todo.image}">`에 바로 전달하여 브라우저 화면상에 첨부 이미지를 성공적으로 렌더링할 수 있습니다.
