# 비동기 상태 요약 대시보드 컴포넌트 추가

단일 페이지 애플리케이션(SPA) 환경에서 할 일 데이터를 비동기 방식으로 추가, 삭제, 혹은 완료 상태로 변경할 때, 전체 페이지의 새로고침 없이 상단에 위치한 현황 대시보드의 통계 수치(전체 개수, 대기 수, 완료 수, 달성률 등)를 클라이언트 사이드 스크립트를 통해 실시간으로 재계산하여 부분 갱신(Partial Update)하는 메커니즘을 학습합니다.

---

## 1. 클라이언트 사이드 실시간 데이터 집계 기법

비동기 통신으로 백엔드 API로부터 할 일 목록 JSON 데이터를 성공적으로 가져왔거나, 수정 요청 성공 후 목록을 다시 취합했을 때 브라우저 메모리에 로드된 데이터 배열(Array)을 즉석에서 루프를 돌거나 필터링 연산을 수행해 통계 수치를 연산합니다.

- **전체 개수**: 배열의 길이(`todos.length`)를 구합니다.
- **완료 개수**: 자바스크립트의 `Array.prototype.filter` 메서드를 사용하여 `is_completed`가 참(`true`)인 데이터 개수를 파악합니다.
- **달성률**: `(완료 개수 / 전체 개수) * 100` 수식을 연산하되, 전체 개수가 0인 경우에 나누기 분모 오류(Division by Zero)가 나지 않도록 예외 처리 로직을 적용합니다.

---

## 2. DOM API를 활용한 실시간 부분 갱신(Partial Update)

통계 계산이 끝나면 브라우저의 DOM 조작 명령어를 사용해 지정한 아이디(`id`)를 가진 통계 엘리먼트의 내부 텍스트 노드(`innerText`) 값만 즉각 치환합니다.
- **이점**: 페이지 전체 레이아웃을 다시 로드하고 스타일시트를 다시 해석하는 리플로우(Reflow)와 리페인트(Repaint) 과정을 최소화하여 극도로 부드러운 화면 전환 속도와 렌더링 성능을 실현합니다.

---

## 3. 구현 코드 상세

### 1단계: SPA HTML 템플릿 내 대시보드 위젯 마크업 배치
파일명: `todos/templates/todos/spa.html`
```html
<!-- 실시간 비동기 집계가 바인딩될 대시보드 위젯 영역 -->
<div class="stats-dashboard" style="display: flex; gap: 15px; margin-top: 20px; flex-wrap: wrap;">
    <div class="stat-card" style="flex: 1; min-width: 120px; background: #ffffff; padding: 15px; border-radius: 10px; box-shadow: var(--shadow-sm); text-align: center; border-left: 5px solid var(--primary-color);">
        <div class="stat-label" style="font-size: 13px; color: #666; margin-bottom: 5px;">전체 할일</div>
        <!-- 자바스크립트가 추적할 id='stat-total' 배치 -->
        <div id="stat-total" class="stat-value" style="font-size: 24px; font-weight: bold; color: #333;">0</div>
    </div>
    <div class="stat-card" style="flex: 1; min-width: 120px; background: #ffffff; padding: 15px; border-radius: 10px; box-shadow: var(--shadow-sm); text-align: center; border-left: 5px solid #f5a623;">
        <div class="stat-label" style="font-size: 13px; color: #666; margin-bottom: 5px;">대기중</div>
        <!-- 자바스크립트가 추적할 id='stat-pending' 배치 -->
        <div id="stat-pending" class="stat-value" style="font-size: 24px; font-weight: bold; color: #f5a623;">0</div>
    </div>
    <div class="stat-card" style="flex: 1; min-width: 120px; background: #ffffff; padding: 15px; border-radius: 10px; box-shadow: var(--shadow-sm); text-align: center; border-left: 5px solid var(--success-color);">
        <div class="stat-label" style="font-size: 13px; color: #666; margin-bottom: 5px;">완료됨</div>
        <!-- 자바스크립트가 추적할 id='stat-completed' 배치 -->
        <div id="stat-completed" class="stat-value" style="font-size: 24px; font-weight: bold; color: var(--success-color);">0</div>
    </div>
    <div class="stat-card" style="flex: 1; min-width: 120px; background: #ffffff; padding: 15px; border-radius: 10px; box-shadow: var(--shadow-sm); text-align: center; border-left: 5px solid #9b59b6;">
        <div class="stat-label" style="font-size: 13px; color: #666; margin-bottom: 5px;">달성률</div>
        <!-- 자바스크립트가 추적할 id='stat-rate' 배치 -->
        <div id="stat-rate" class="stat-value" style="font-size: 24px; font-weight: bold; color: #9b59b6;">0%</div>
    </div>
</div>
```

### 2단계: Javascript 대시보드 상태 집계 및 갱신 기능 개발
파일명: `todos/static/todos/js/app.js`
```javascript
document.addEventListener('DOMContentLoaded', () => {
    // ... (중략)
    
    // 1. 통계 수치 노출용 DOM 노드 레퍼런스 확보
    const statTotal = document.getElementById('stat-total');
    const statPending = document.getElementById('stat-pending');
    const statCompleted = document.getElementById('stat-completed');
    const statRate = document.getElementById('stat-rate');

    // 2. 비동기 수신한 데이터를 활용한 전역 통계 계산 및 화면 주입 함수 정의
    const updateDashboard = (todos) => {
        const total = todos.length;
        const completed = todos.filter(todo => todo.is_completed).length;
        const pending = total - completed;
        // 나눗셈 분모 분기 예외 처리
        const rate = total > 0 ? Math.round((completed / total) * 100) : 0;

        // innerText 를 사용해 마크업은 건드리지 않고 텍스트값만 조작
        if (statTotal) statTotal.innerText = total;
        if (statPending) statPending.innerText = pending;
        if (statCompleted) statCompleted.innerText = completed;
        if (statRate) statRate.innerText = `${rate}%`;
    };

    // 할일 목록 로드 함수
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
            
            // 3. API 목록 호출 및 갱신 완료 후 실시간 수치 동기화
            updateDashboard(todos);
        } catch (error) {
            console.error(error);
        }
    };
    
    // 이하 생략
});
```

이 연동이 작동하면 할 일을 추가로 등록하여 API가 성공하거나, 카드의 완료 버튼을 누르거나, 삭제 버튼을 눌러 비동기 목록 갱신(`loadTodos()`)이 다시 수행될 때마다, 대시보드의 숫자 정보와 달성률 바(Bar) 영역이 끊김 없는 비동기 전환과 함께 즉각 동기화됩니다.
