# 템플릿 엔진과 정적 파일 관리

HTML 구조 설계에 필요한 DTL(Django Template Language)의 상세 제어문 작성법, 레이아웃 재사용을 위한 템플릿 상속 코드, 정적 스타일시트(CSS)와 미디어 파일(Media)을 장고 설정에 엮는 구체적인 구현 방식을 배웁니다.

---

## 1. DTL (Django Template Language) 상세 제어문 작성법

장고 템플릿 엔진은 파이썬 객체 데이터 바인딩 및 제어문 흐름을 위한 특수 약속 기호를 제공합니다.

### 템플릿 기호 및 제어 코드 스니펫
- **변수 출력**: `{{ 변수명 }}` 또는 객체 속성 조회 `{{ todo.title }}`
- **반복문 (For)**:
  ```html
  {% for todo in todos %}
      <p>{{ todo.title }}</p>
  {% empty %}
      <p>목록이 비어있습니다.</p>
  {% endfor %}
  ```
- **조건문 (If)**:
  ```html
  {% if todo.is_completed %}
      <span>작업 완료</span>
  {% else %}
      <span>대기 중</span>
  {% endif %}
  ```
- **주소 자동 추적 (URL)**:
  `{% url '네임스페이스:경로이름' 인자값 %}`
  ```html
  <a href="{% url 'todos:about' %}">소개 페이지로 이동</a>
  ```

---

## 2. 템플릿 상속 구체적 코드 모습

중복 코드를 차단하기 위해 화면의 기본 뼈대를 만드는 부모 템플릿과 세부 내용을 정의하는 자식 템플릿의 연결 구조입니다.

### 부모 파일 (todos/templates/todos/base.html)
```html
<!DOCTYPE html>
<html>
<head>
    <title>웹서비스 타이틀</title>
</head>
<body>
    <header>메인 메뉴 헤더 영역</header>
    
    <main>
        <!-- 자식 템플릿들이 자신만의 HTML 요소를 밀어 넣을 공간 선언 -->
        {% block content %}
        {% endblock %}
    </main>
    
    <footer>푸터 저작권 영역</footer>
</body>
</html>
```

### 자식 파일 (todos/templates/todos/todo_list.html)
```html
<!-- 1. 가장 첫 줄에 부모 템플릿 파일을 상속받을 것임을 선언합니다. -->
{% extends 'todos/base.html' %}

<!-- 2. 부모가 비워둔 content 블록 내부를 개별 요소로 채워 넣습니다. -->
{% block content %}
    <h2>할일 목록 화면</h2>
    <p>오늘도 알찬 하루를 보냅시다.</p>
{% endblock %}
```

---

## 3. 정적 파일 (Static) 연동 및 CSS 등록 절차

웹 브라우저에 다운로드시켜 적용할 CSS 스타일시트, 자바스크립트 소스를 장고와 결합하는 상세 방법입니다.

### settings.py 정적 경로 지정
```python
# settings.py
STATIC_URL = 'static/'

# 프로젝트 루트(BASE_DIR) 밑의 static 폴더를 공용 정적 파일 경로로 묶습니다.
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```

### HTML 내 정적 스타일시트 로딩 코드
템플릿 최상단에 static 라이브러리를 로드한 후 태그 형식으로 링크를 설정합니다.
```html
{% load static %}
<link rel="stylesheet" href="{% static 'todos/css/style.css' %}">
```

---

## 4. 미디어 파일 (Media) 업로드 및 개발 서버 서빙 설정

사용자가 전송하는 파일(예: 할일 인증 이미지 등)을 처리하기 위한 설정 및 뷰 매핑 코드입니다.

### settings.py 미디어 경로 지정
```python
# settings.py
# 브라우저가 사용자 파일에 접근하는 URL 시작점
MEDIA_URL = 'media/'

# 실제 파일이 물리적으로 복사되어 적재될 서버 저장 디렉토리 경로
MEDIA_ROOT = BASE_DIR / 'media'
```

### urls.py 개발 전용 미디어 URL 연결 설정 (todoboard/urls.py)
개발 모드(`DEBUG = True`)에서 장고가 스스로 미디어 파일을 중개(Serving)할 수 있도록 라우터를 이어붙입니다.
```python
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('', include('todos.urls')),
]

# 디버그 모드가 켜져 있을 때만 미디어 업로드 경로를 로컬 호스트 URL에 등록합니다.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
- 운영 환경에서는 Nginx나 AWS S3 등 전용 인프라가 미디어 서빙을 가동하므로, 오직 로컬 환경 테스트를 위해서만 본 설정 코드를 활용합니다.
