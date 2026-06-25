# 컨텍스트 프로세서를 활용한 JS 전역 변수 바인딩

모던 웹 서비스 개발 환경에서는 백엔드와 프론트엔드가 데이터를 긴밀하게 주고받아야 합니다. Django 컨텍스트 프로세서(Context Processor)를 사용하여 템플릿 렌더링 시 전역으로 필요한 백엔드 설정값(예: API 엔드포인트 URL, 서비스 설정 등)을 템플릿 변수로 주입하고, 이를 브라우저의 Javascript 전역 변수로 동적 바인딩하여 하드코딩 결합을 완화하는 소프트웨어 아키텍처 기법을 학습합니다.

---

## 1. 프론트-백엔드 데이터 결합 완화의 필요성

전통적인 장고 템플릿 뷰는 데이터의 주입과 렌더링이 서버 측에서 일괄 완결되지만, 비동기 호출이 결합된 SPA 구조에서는 프론트엔드 Javascript가 직접 API 요청을 송신할 서버 엔드포인트 URL을 소유하고 있어야 합니다.

### 하드코딩의 문제점
- Javascript 파일 내부에 URL 경로를 `const apiBaseUrl = '/api/todos/';` 와 같이 리터럴 텍스트로 고정해두면, 장고 라우팅 설정(`urls.py`)이 변경되었을 때 JS 코드도 동시 수정해 주어야 하므로 휴먼 에러 가능성과 유지보수 공수가 동반 상승합니다.

### 컨텍스트 프로세서를 통한 해결
- Django의 `reverse` 유틸리티를 활용하여 런타임에 뷰 엔드포인트 실제 주소를 도출한 뒤 전역 변수로 할당합니다.
- HTML 문서의 로드 영역에 이 변수를 출력하여 JS가 주소를 인지하게 함으로써 백엔드 주소체계의 변경에 유연하게 대응할 수 있도록 격리합니다.

---

## 2. 구현 흐름 분석

```text
[ Django settings.py / urls.py ]
      │ 런타임에 reverse('todos:api_todo-list') 수행
      ▼
[ context_processors.py ]
      │ 전역 사전 등록: {'API_BASE_URL': '/api/todos/'} 반환
      ▼
[ spa.html (Template Engine) ]
      │ 렌더링 시 <script> const apiBaseUrl = "{{ API_BASE_URL }}"; 바인딩
      ▼
[ app.js (Browser Runtime) ]
      │ fetch(apiBaseUrl, ...) 실행하여 비동기 데이터 송수신
```

---

## 3. 코드 연동 상세

### 1단계: 커스텀 컨텍스트 프로세서 구현
파일명: `todos/context_processors.py`
```python
from django.urls import reverse

def global_spa_config(request):
    """
    SPA 화면의 프론트엔드 자바스크립트가 수신할 전역 설정을 제공합니다.
    """
    try:
        # reverse 유틸리티로 Django URL 네임스페이스의 실제 물리 주소를 역추적합니다.
        api_url = reverse('todos:api_todo-list')
    except Exception:
        api_url = '/api/todos/'
        
    return {
        'API_BASE_URL': api_url,
        'SITE_META_TITLE': 'TodoBoard Premium SPA',
    }
```

### 2단계: settings.py 등록
파일명: `todoboard/settings.py`
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 개발한 전역 변수 공급용 컨텍스트 프로세서 함수 등록
                'todos.context_processors.global_spa_config',
            ],
        },
    },
]
```

### 3단계: SPA 템플릿에서의 변수 바인딩
파일명: `todos/templates/todos/spa.html`
```html
{% block content %}
<div class="content-header">
    <div class="header-text">
        <!-- 1. 컨텍스트 프로세서의 SITE_META_TITLE 변수 동적 출력 -->
        <h2 class="section-title">{{ SITE_META_TITLE }}</h2>
        <p class="section-desc">페이지 새로고침 없이 실시간으로 할일을 조작할 수 있는 풀스택 SPA 모드입니다.</p>
    </div>
</div>

<!-- 중간 생략 -->

<!-- CSRF 토큰 및 API 주소 바인딩 -->
<script>
    const csrfToken = "{{ csrf_token }}";
    // 2. 컨텍스트 프로세서에서 동적으로 역산해 준 API 경로 변수를 JS 상수에 대입
    const apiBaseUrl = "{{ API_BASE_URL }}";
</script>
<script src="{% static 'todos/js/app.js' %}"></script>
{% endblock %}
```

이를 통해 브라우저가 `/spa/` 화면을 최초 요청하면 장고 템플릿 엔진이 렌더링하는 시점에 실제 유효 주소를 런타임에 끼워 넣습니다. 프론트엔드 자바스크립트(`app.js`)는 주소 정보의 소스 코드가 하드코딩되었는지 알 필요 없이 전달받은 상수 `apiBaseUrl` 주소를 통해 요청을 안정적으로 처리하게 됩니다.
