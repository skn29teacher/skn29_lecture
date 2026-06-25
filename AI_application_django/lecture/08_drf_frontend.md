# [08] DRF와 JS Fetch 연동 및 미니 프로젝트 완성 가이드

장고 프로젝트에 **`ModelViewSet`** 과 **`DefaultRouter`** 를 도입해 보일러플레이트 API 코드를 대폭 절감하고, **`django-cors-headers`** 패키지를 세팅해 CORS 정책을 제어하며, 자바스크립트 **Fetch API**를 사용하여 페이지 새로고침 없이 비동기적으로 동작하는 단일 페이지 애플리케이션(SPA) 풀스택 결과물을 완성하는 법을 설명합니다.

이전의 추상적인 이론 설명에서 벗어나, 어느 폴더의 어떤 파일을 어떻게 수정해야 하는지 구체적인 경로와 전체 소스코드를 빠짐없이 기록했습니다.

---

## 실습 요약 및 핵심 흐름
1. **API 간소화 (`ModelViewSet`)**: `todos/api_views.py` 파일 내 개별 CRUD용 `APIView` 대신 하나로 묶어 자동화된 액션을 제공하는 `ModelViewSet`으로 교체합니다.
2. **라우터 연동 (`DefaultRouter`)**: `todos/urls.py`에 라우터를 등록하여 REST API 엔드포인트 주소 체계를 일괄 자동 배치합니다.
3. **CORS 우회 설정**: 백엔드 포트와 프론트엔드 포트가 다를 때 발생하는 브라우저 통신 거부를 방지하도록 `settings.py`에 CORS 미들웨어를 심어줍니다.
4. **SPA 화면 템플릿 제작**: 비동기 통신으로 동작할 DOM 컨테이너를 포함하는 `todos/templates/todos/spa.html` 화면을 생성하고, `todos/views.py`에 이를 호출하는 진입점을 만듭니다.
5. **Fetch API 연동 스크립트 작성**: `todos/static/todos/js/app.js`를 만들어 비동기로 데이터 조회(GET), 등록(POST), 부분수정(PATCH), 삭제(DELETE)하는 로직을 통합 구현하고, 장고의 보안 검증을 통과하도록 헤더에 `X-CSRFToken`을 전달하는 코드를 설계합니다.

---

## 1단계: API 뷰 파일 수정 (`ModelViewSet` 교체)
- **파일 경로**: `todos/api_views.py` (전체 덮어쓰기 권장)
- **작성할 내용**: 기존의 개별 조회/수정/삭제 뷰들을 하나로 정리합니다. 로그인 상태에 맞추어 표시 데이터 목록을 동적 필터링하는 `get_queryset`과 새 할일 등록 시 로그인 유저를 바인딩하는 `perform_create` 메소드를 구현합니다.

```python
from rest_framework import viewsets, permissions
from .models import Todo
from .serializers import TodoSerializer

# ModelViewSet을 상속하면 목록조회, 신규등록, 상세조회, 전체수정, 부분수정, 삭제 처리가 자동 통합됩니다.
class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    # 현재 로그인 세션에 따라 본인 데이터 쿼리셋만 필터링 후 반환
    def get_queryset(self):
        return Todo.objects.filter(author=self.request.user).order_by('-created_at')

    # 새 할일 등록 시 Serializer가 차단한 author 필드에 현재 요청 유저 자동 삽입
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

---

## 2단계: 애플리케이션 URL 매핑 파일 수정 (`DefaultRouter` 등록)
- **파일 경로**: `todos/urls.py` (전체 덮어쓰기 권장)
- **작성할 내용**: `DefaultRouter` 인스턴스를 하나 만들고 뷰셋을 등록하여, 자동으로 REST API 주소가 맵핑될 수 있게 하위 주소 체계 경로에 포함시킵니다. SPA 페이지를 띄워줄 `spa_index` 진입점도 함께 등록합니다.

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views

# 1. 디폴트 라우터 초기화
router = DefaultRouter()
# 2. todos 라는 식별자 경로 뒤에 뷰셋 바인딩 등록
router.register('todos', api_views.TodoViewSet, basename='api_todo')

app_name = 'todos'

urlpatterns = [
    # 전통적인 템플릿(HTML) 전용 경로
    path('', views.todo_list, name='todo_list'),
    path('create/', views.todo_create, name='todo_create'),
    path('<int:pk>/update/', views.todo_update, name='todo_update'),
    path('<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.AboutView.as_view(), name='about'),
    
    # 신규 추가: SPA 진입점 뷰 경로
    path('spa/', views.spa_index, name='spa_index'),

    # 신규 추가: 라우터가 계산한 REST API 경로 세트 일괄 주입
    # 이 매핑으로 인해 /todos/api/todos/ 및 /todos/api/todos/<pk>/ 주소가 자동 개설됩니다.
    path('api/', include(router.urls)),
]
```

---

## 3단계: 환경 설정 파일 수정 (CORS 허용)
- **파일 경로**: `todoboard/settings.py`
- **작성할 내용**: 외부 프론트엔드 환경이나 다른 도메인 소스코드에서 비동기로 API 백엔드를 호출할 때 브라우저에 의해 발생하는 CORS 차단 공격 차단 동작을 방지하는 설정을 기입하고, 정적 파일 경로(STATIC)를 올바르게 정의합니다.

```python
# 1. corsheaders 앱 등록
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',  # 추가
    'rest_framework',
    'todos',
]

# 2. 미들웨어 '최상단' 부분에 CorsMiddleware 추가
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 최상단 배치 권장
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 3. 로컬 테스트 및 API 오픈을 위해 모든 오리진 출처 통신 허용 설정 기입
CORS_ALLOW_ALL_ORIGINS = True

# 4. 정적 파일 탐색 영역 정의 추가
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```

---

## 4단계: 뷰 파일에 SPA 화면 뷰 등록
- **파일 경로**: `todos/views.py`
- **작성할 내용**: 브라우저 요청 시 SPA 전용 HTML 파일을 넘겨줄 `spa_index` 함수 뷰를 덧붙여 선언합니다.

기존 `todos/views.py` 하단에 다음 뷰를 추가합니다.
```python
@login_required
def spa_index(request):
    # 비동기로 동작하게 될 spa 템플릿 호출
    return render(request, 'todos/spa.html')
```

---

## 5단계: SPA 전용 HTML 템플릿 생성
- **파일 경로**: `todos/templates/todos/spa.html` (신규 생성)
- **작성할 내용**: 왼쪽에는 새로운 할 일을 입력할 수 있는 폼 영역을 두고, 오른쪽에는 자바스크립트로 가져온 데이터 카드를 실시간 렌더링할 그리드 컨테이너 영역을 만듭니다. 또한 자바스크립트 측으로 장고 내부 CSRF 난수 토큰값과 백엔드 REST API URL 주소를 전달해 주는 매핑 스크립트를 포함합니다.

```html
{% extends 'todos/base.html' %}
{% load static %}

{% block content %}
<div class="content-header">
    <div class="header-text">
        <h2 class="section-title">비동기 할일 관리 (SPA)</h2>
        <p class="section-desc">페이지 새로고침 없이 실시간으로 할일을 조작할 수 있는 풀스택 SPA 모드입니다.</p>
    </div>
</div>

<div class="spa-layout" style="display: grid; grid-template-columns: 350px 1fr; gap: 30px; margin-top: 24px;">
    <!-- 비동기 입력 폼 카드 -->
    <div class="spa-form-column">
        <div class="form-card" style="padding: 24px; max-width: 100%; box-shadow: var(--shadow-sm);">
            <h3 style="font-size: 18px; font-weight: 800; margin-bottom: 16px;">새 할일 추가</h3>
            <form id="spa-todo-form" class="todo-form-body" style="gap: 16px;">
                <div class="form-group" style="gap: 6px;">
                    <label class="form-label" style="font-size: 13px;">할 일 제목</label>
                    <input type="text" id="spa-title" class="form-input" placeholder="비동기로 등록할 일을 적으세요" required>
                </div>
                <div class="form-group" style="gap: 6px;">
                    <label class="form-label" style="font-size: 13px;">상세 메모</label>
                    <textarea id="spa-content" class="form-input form-textarea" placeholder="상세 내용을 적어주세요" style="min-height: 80px;"></textarea>
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%;">비동기 저장</button>
            </form>
        </div>
    </div>

    <!-- 비동기 목록 뷰 영역 -->
    <div class="spa-list-column">
        <div id="spa-todo-list" class="todo-grid" style="grid-template-columns: 1fr;">
            <!-- 자바스크립트로 실시간 렌더링될 영역 -->
            <div class="empty-state">
                <p>할일을 비동기로 불러오는 중입니다...</p>
            </div>
        </div>
    </div>
</div>

<!-- CSRF 토큰 및 API 주소를 JS 전역 변수로 전달 -->
<script>
    const csrfToken = "{{ csrf_token }}";
    // DefaultRouter는 뷰셋 연동 시 '모델명-list', '모델명-detail' 역추적 네이밍 규칙을 자동 적용함
    const apiBaseUrl = "{% url 'todos:api_todo-list' %}"; 
</script>
<!-- 비동기 DOM 통제 스크립트 연결 -->
<script src="{% static 'todos/js/app.js' %}"></script>
{% endblock %}
```

---

## 6단계: 비동기 통신을 제어할 JavaScript 로직 작성
- **파일 경로**: `todos/static/todos/js/app.js` (신규 생성)
- **작성할 내용**: DOM이 열릴 때 Fetch API를 호출해 목록 데이터를 가져오고, 폼이 제출되면 비동기로 데이터 등록을 지시하며, 카드 내 삭제(DELETE) 및 상태 반전(PATCH) 버튼을 눌렀을 때 백엔드 통신 후 화면을 갱신하는 코드를 작성합니다.

```javascript
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
```

---

## 7단계: 전체 웹페이지 고급 디자인 스타일 완성
- **파일 경로**: `todos/static/todos/css/style.css` (신규 생성)
- **작성할 내용**: 전역 초기화, Outfit/Noto Sans 한글 폰트 주입, 그라데이션 로고 장식, 카드 형태 디자인 요소, 흐릿하게 반사되는 헤더 효과(Glassmorphism), 그리고 부드러운 호버 트랜지션 애니메이션을 수록합니다.

```css
/* 기본 변수 및 디자인 토큰 */
:root {
    --primary-color: #4f46e5;
    --primary-hover: #4338ca;
    --primary-light: #e0e7ff;
    --success-color: #10b981;
    --success-bg: #d1fae5;
    --warning-color: #f59e0b;
    --warning-bg: #fef3c7;
    --text-main: #1f2937;
    --text-muted: #6b7280;
    --bg-main: #f9fafb;
    --bg-card: #ffffff;
    --border-color: #e5e7eb;
    --border-radius-lg: 16px;
    --border-radius-md: 10px;
    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
}

/* 전역 초기화 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Outfit', 'Noto Sans KR', sans-serif;
    background-color: var(--bg-main);
    color: var(--text-main);
    line-height: 1.6;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

a {
    color: inherit;
    text-decoration: none;
}

/* 헤더 레이아웃 */
.app-header {
    background-color: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border-color);
    position: sticky;
    top: 0;
    z-index: 100;
}

.header-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 16px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo a {
    font-size: 24px;
    font-weight: 800;
    background: linear-gradient(135deg, var(--primary-color), #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}

.nav-links {
    display: flex;
    gap: 24px;
}

.nav-item {
    font-weight: 600;
    font-size: 15px;
    color: var(--text-muted);
    transition: color 0.2s ease;
}

.nav-item:hover {
    color: var(--primary-color);
}

/* 메인 레이아웃 */
.app-main {
    flex: 1;
    padding: 40px 24px;
}

.main-container {
    max-width: 1000px;
    margin: 0 auto;
}

/* 타이틀 및 헤더 영역 */
.content-header {
    margin-bottom: 32px;
}

.section-title {
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 8px;
    letter-spacing: -0.5px;
}

.section-desc {
    color: var(--text-muted);
    font-size: 16px;
}

/* 할일 카드 그리드 및 카드 디자인 */
.todo-board-container {
    margin-top: 24px;
}

.todo-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

.todo-card {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-lg);
    padding: 24px;
    box-shadow: var(--shadow-sm);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
}

.todo-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background-color: var(--primary-color);
    transition: background-color 0.3s ease;
}

.todo-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

.todo-card.completed::before {
    background-color: var(--success-color);
}

.todo-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.status-badge {
    font-size: 12px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 20px;
    color: var(--primary-color);
    background-color: var(--primary-light);
}

.todo-card.completed .status-badge {
    color: var(--success-color);
    background-color: var(--success-bg);
}

.todo-date {
    font-size: 12px;
    color: var(--text-muted);
}

.todo-title {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 10px;
    letter-spacing: -0.3px;
    transition: color 0.3s ease;
}

.todo-card.completed .todo-title {
    color: var(--text-muted);
    text-decoration: line-through;
}

.todo-body {
    color: var(--text-muted);
    font-size: 14px;
    flex-grow: 1;
    word-break: break-all;
}

.todo-card.completed .todo-body {
    color: #9ca3af;
}

/* 빈 상태 표시 */
.empty-state {
    grid-column: 1 / -1;
    text-align: center;
    padding: 60px 24px;
    background-color: var(--bg-card);
    border: 2px dashed var(--border-color);
    border-radius: var(--border-radius-lg);
    color: var(--text-muted);
}

/* 소개 페이지 */
.about-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px 0;
}

.about-card {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-lg);
    padding: 40px;
    max-width: 600px;
    box-shadow: var(--shadow-md);
}

.about-title {
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 16px;
    background: linear-gradient(135deg, var(--primary-color), #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.about-lead {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-main);
    margin-bottom: 20px;
}

.about-details p {
    font-size: 14px;
    color: var(--text-muted);
    margin-bottom: 14px;
    line-height: 1.7;
}

/* 공통 버튼 스타일 */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 700;
    border-radius: var(--border-radius-md);
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
    text-decoration: none;
}

.btn-primary {
    background-color: var(--primary-color);
    color: #ffffff;
}

.btn-primary:hover {
    background-color: var(--primary-hover);
    transform: translateY(-1px);
}

.btn-secondary {
    background-color: var(--primary-light);
    color: var(--primary-color);
    margin-left: 8px;
}

.btn-secondary:hover {
    background-color: #c7d2fe;
}

.btn-text {
    font-size: 13px;
    font-weight: 600;
    color: var(--primary-color);
    cursor: pointer;
    background: none;
    border: none;
    transition: color 0.2s ease;
}

.btn-text:hover {
    color: var(--primary-hover);
    text-decoration: underline;
}

.btn-delete {
    color: #ef4444;
}

.btn-delete:hover {
    color: #dc2626;
}

/* 카드 하단 버튼 배치 */
.todo-actions {
    margin-top: auto;
    padding-top: 12px;
    border-top: 1px solid var(--border-color);
    display: flex;
    gap: 16px;
    align-items: center;
}

.delete-form {
    display: inline;
}

.content-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
}

/* 폼 스타일링 */
.form-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px 0;
}

.form-card {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-lg);
    padding: 40px;
    width: 100%;
    max-width: 550px;
    box-shadow: var(--shadow-md);
}

.form-title {
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 8px;
    letter-spacing: -0.5px;
}

.form-desc {
    color: var(--text-muted);
    font-size: 14px;
    margin-bottom: 24px;
}

.todo-form-body {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-label {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-main);
}

.form-input {
    width: 100%;
    padding: 12px 16px;
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-md);
    font-family: inherit;
    font-size: 14px;
    outline: none;
    transition: border-color 0.2s ease;
}

.form-input:focus {
    border-color: var(--primary-color);
}

.form-textarea {
    min-height: 120px;
    resize: vertical;
}

.form-checkbox {
    width: 18px;
    height: 18px;
    cursor: pointer;
    accent-color: var(--primary-color);
}

.form-actions {
    margin-top: 10px;
    display: flex;
    justify-content: flex-end;
}

.field-errors {
    margin-top: 4px;
}

.error-text {
    font-size: 12px;
    color: #ef4444;
    font-weight: 600;
}

/* 푸터 레이아웃 */
.app-footer {
    background-color: #ffffff;
    border-top: 1px solid var(--border-color);
    padding: 24px;
    text-align: center;
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 500;
}

.footer-container {
    max-width: 1200px;
    margin: 0 auto;
}

/* 반응형 모바일 환경 지원 */
@media (max-width: 640px) {
    .header-container {
        flex-direction: column;
        gap: 12px;
    }
    
    .app-main {
        padding: 24px 16px;
    }
    
    .todo-grid {
        grid-template-columns: 1fr;
    }
    
    .about-card {
        padding: 24px;
    }
}
```

---

## 동작 확인 및 테스트 가이드
서버를 켠 다음, 웹 브라우저를 열고 `/spa/` 주소로 접속합니다.
- `http://127.0.0.1:8000/spa/`
1. **비동기 등록 테스트**: 좌측 등록 창에 제목과 세부 메모를 적고 "비동기 저장"을 누릅니다. 페이지가 리로드되지 않고 즉시 우측 리스트 그리드 카드에 할 일이 등록되는지 관찰합니다.
2. **비동기 완료상태 토글**: 카드의 "대기중" 혹은 "완료" 배지를 클릭합니다. 텍스트 선에 취소선이 생기거나 사라지며 상태가 비동기 갱신되는지 확인합니다.
3. **비동기 삭제**: 카드의 "삭제" 버튼을 클릭하고 얼럿 창에서 삭제 승인을 누릅니다. 카드가 비동기 통신을 통해 화면에서 부드럽게 지워지는지 확인합니다.
