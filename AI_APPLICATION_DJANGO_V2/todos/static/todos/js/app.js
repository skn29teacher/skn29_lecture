document.addEventListener('DOMContentLoaded', () => {
    const todoListContainer = document.getElementById('spa-todo-list');
    const todoForm = document.getElementById('spa-todo-form');
    const titleInput = document.getElementById('spa-title');
    const contentInput = document.getElementById('spa-content');
    const imageInput = document.getElementById('spa-image');

    // 할일 목록 로드 함수
    const loadTodos = async () => {
        console.log(`apiBaseUrl : ${apiBaseUrl}`);
        try {
            const response = await fetch(apiBaseUrl, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            });
            if (!response.ok) throw new Error('목록 조회 실패');
            
            const todos = await response.json();
            renderTodos(todos);
        } catch (error) {
            console.error(error);
            todoListContainer.innerHTML = `
                <div class="empty-state">
                    <p style="color: #ef4444;">데이터를 불러오는 중 오류가 발생했습니다.</p>
                </div>
            `;
        }
    };

    // 할일 목록 화면 렌더링
    const renderTodos = (todos) => {
        if (todos.length === 0) {
            todoListContainer.innerHTML = `
                <div class="empty-state">
                    <p>등록된 할일이 없습니다. 새 할일을 비동기로 추가해 보세요.</p>
                </div>
            `;
            return;
        }

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

    // 카드 내부 이벤트 리스너 바인딩
    const attachCardListeners = () => {
        // 삭제 버튼 처리
        document.querySelectorAll('.btn-delete-spa').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const todoId = e.target.getAttribute('data-id');
                if (!confirm('이 할일을 비동기로 삭제하시겠습니까?')) return;

                try {
                    const response = await fetch(`${apiBaseUrl}${todoId}/`, {
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': csrfToken
                        }
                    });
                    if (response.ok) {
                        loadTodos();
                    } else {
                        alert('삭제에 실패했습니다.');
                    }
                } catch (error) {
                    console.error(error);
                    alert('삭제 중 통신 에러 발생');
                }
            });
        });

        // 상태 토글 처리
        document.querySelectorAll('.btn-toggle').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const todoId = e.target.getAttribute('data-id');
                const isCompleted = e.target.getAttribute('data-completed') === 'true';

                try {
                    const response = await fetch(`${apiBaseUrl}${todoId}/`, {
                        method: 'PATCH', // 부분 수정을 위한 PATCH 메소드 활용
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken
                        },
                        body: JSON.stringify({ is_completed: !isCompleted })
                    });
                    if (response.ok) {
                        loadTodos();
                    } else {
                        alert('상태 갱신에 실패했습니다.');
                    }
                } catch (error) {
                    console.error(error);
                    alert('상태 갱신 중 통신 에러 발생');
                }
            });
        });
    };

    // 할일 비동기 등록 이벤트 처리
    todoForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = titleInput.value.trim();
        const content = contentInput.value.trim();
        const file = imageInput.files[0];

        if (!title) return;

        // multipart/form-data 처리를 위한 FormData 객체 사용
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
                    // FormData를 전송할 때는 브라우저가 Boundary를 자동 계산하도록 Content-Type 헤더를 작성하지 않습니다.
                    'X-CSRFToken': csrfToken
                },
                body: formData
            });

            if (response.ok) {
                // 폼 리셋 및 목록 다시 로드
                titleInput.value = '';
                contentInput.value = '';
                imageInput.value = ''; // 파일 인풋 리셋
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

    // 최초 진입 시 데이터 수집
    loadTodos();
});
