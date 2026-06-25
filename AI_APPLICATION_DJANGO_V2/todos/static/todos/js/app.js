document.addEventListener('DOMContentLoaded', () => {
    const todoListContainer = document.getElementById('spa-todo-list');
    const todoForm = document.getElementById('spa-todo-form');
    const titleInput = document.getElementById('spa-title');
    const contentInput = document.getElementById('spa-content');

    // 1. 비동기 할일 목록 수집 함수
    const loadTodos = async () => {
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

    // 2. 수집된 JSON 리스트를 DOM 엘리먼트로 동적 생성 및 화면 가공 출력
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
        todos.forEach(todo => {
            const card = document.createElement('div');
            card.className = `todo-card ${todo.is_completed ? 'completed' : ''}`;
            
            const createdDate = new Date(todo.created_at);
            const dateString = `${createdDate.getFullYear()}-${String(createdDate.getMonth()+1).padStart(2, '0')}-${String(createdDate.getDate()).padStart(2, '0')} ${String(createdDate.getHours()).padStart(2, '0')}:${String(createdDate.getMinutes()).padStart(2, '0')}`;

            card.innerHTML = `
                <div class="todo-card-header">
                    <!-- 클릭 시 완료 상태 토글 버튼 실행 -->
                    <button class="status-badge btn-toggle" data-id="${todo.id}" data-completed="${todo.is_completed}" style="border: none; cursor: pointer;">
                        ${todo.is_completed ? '완료' : '대기중'}
                    </button>
                    <span class="todo-date">${dateString}</span>
                </div>
                <h3 class="todo-title">${todo.title}</h3>
                ${todo.content ? `<p class="todo-body">${todo.content}</p>` : ''}
                <div class="todo-actions">
                    <button class="btn-text btn-delete-spa" data-id="${todo.id}" style="color: #ef4444;">삭제</button>
                </div>
            `;

            todoListContainer.appendChild(card);
        });

        // 렌더링 완료 후 각 카드의 버튼에 클릭 리스너 연결
        attachCardListeners();
    };

    // 3. 동적 생성된 버튼에 대한 클릭 리스너 바인딩
    const attachCardListeners = () => {
        // [비동기 삭제 버튼 이벤트 처리]
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
                        loadTodos(); // 화면 갱신을 위해 데이터 재수집
                    } else {
                        alert('삭제에 실패했습니다.');
                    }
                } catch (error) {
                    console.error(error);
                    alert('삭제 중 통신 에러 발생');
                }
            });
        });

        // [비동기 완료상태 토글(PATCH) 이벤트 처리]
        document.querySelectorAll('.btn-toggle').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const todoId = e.target.getAttribute('data-id');
                const isCompleted = e.target.getAttribute('data-completed') === 'true';

                try {
                    // 부분 수정을 의미하는 PATCH 방식 호출
                    const response = await fetch(`${apiBaseUrl}${todoId}/`, {
                        method: 'PATCH',
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

    // 4. 할일 비동기 등록 양식(Form Submit) 이벤트 처리
    todoForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = titleInput.value.trim();
        const content = contentInput.value.trim();

        if (!title) return;

        try {
            const response = await fetch(apiBaseUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // 중요: 장고 POST는 세션 인증 상태에서도 반드시 CSRF 헤더를 실어야 함
                },
                body: JSON.stringify({
                    title: title,
                    content: content,
                    is_completed: false
                })
            });

            if (response.ok) {
                // 입력 항목 비우고 리스트 다시 로딩
                titleInput.value = '';
                contentInput.value = '';
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

    // 5. 최초 페이지 진입 시 목록 자동 로드 가동
    loadTodos();
});