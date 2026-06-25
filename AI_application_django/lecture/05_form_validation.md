# [05] Django 폼과 모델폼 및 유효성 검사 가이드


---

## 실습 요약 및 핵심 흐름
1. **`TodoForm` 정의**: `todos/forms.py` 파일을 새로 만들고 `Todo` 모델과 연동합니다.
2. **뷰 함수 전환**: `todos/views.py` 내의 기존 단순 응답용 함수들을 `TodoForm`을 사용하는 뷰 함수로 변경합니다.
3. **URL 매핑 변경**: URL 쿼리 스트링(`?id=1`) 방식 대신 장고 표준 경로 변수(`<int:pk>`) 방식으로 변경합니다.
4. **템플릿(HTML) 레이아웃 적용**: `base.html`을 만들고 공통 레이아웃을 상속받아 입력 폼(`todo_form.html`)과 리스트 화면(`todo_list.html`)을 연동합니다.

---

## 1단계: 폼 파일 생성
- **파일 경로**: `todos/forms.py` (신규 생성)
- **작성할 내용**: `Todo` 모델의 필드(`title`, `content`, `is_completed`)를 받아와 입력 제약 조건과 렌더링에 사용할 CSS 클래스 속성을 매핑합니다.

```python
from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        # 1. 폼과 1대1로 연동할 데이터 모델 클래스 지정
        model = Todo
        
        # 2. 사용자에게 입력을 받아 처리할 대상 컬럼 리스트 지정
        fields = ['title', 'content', 'is_completed']
        
        # 3. HTML 엘리먼트 렌더링 시 적용할 CSS 클래스 속성 및 Placeholder 설정
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '할 일을 입력하세요 (예: 파이썬 복습하기)'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'placeholder': '상세한 할 일 설명이나 메모를 적어주세요'
            }),
            'is_completed': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            })
        }
        
        # 4. 브라우저 화면에 출력될 레이블명 매칭
        labels = {
            'title': '할 일 제목',
            'content': '메모 및 세부내용',
            'is_completed': '완료 상태'
        }
```

---

## 2단계: 뷰 파일 수정
- **파일 경로**: `todos/views.py` (전체 덮어쓰기 권장)
- **작성할 내용**: 기존의 문자열 출력 방식 대신 HTML 템플릿을 호출하며, GET(입력 화면)/POST(데이터 유효성 검사 및 저장) 분기 로직을 처리하는 표준 뷰를 작성합니다.

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Todo
from .forms import TodoForm

def todo_list(request):
    # 등록된 전체 할 일을 최신순으로 가져와 리스트 템플릿에 전달
    todos = Todo.objects.all().order_by('-created_at')
    return render(request, 'todos/todo_list.html', {'todos': todos})

def todo_create(request):
    if request.method == 'POST':
        # 사용자가 폼에 채워 전송(POST)한 원시 데이터를 폼 인스턴스에 밀어 넣습니다.
        form = TodoForm(request.POST)
        # 데이터 유효성(빈 값 검사, 글자 수 한도, 형식 일치 등)을 점검합니다.
        if form.is_valid():
            # 유효성 검증을 통과한 데이터를 DB에 저장합니다.
            form.save()
            # 저장 완료 후 목록 화면으로 리다이렉트합니다.
            return redirect('todos:todo_list')
    else:
        # GET 요청일 때는 입력을 위한 빈 폼 객체를 생성합니다.
        form = TodoForm()
        
    return render(request, 'todos/todo_form.html', {'form': form, 'action': '등록'})

def todo_update(request, pk):
    # 수정할 대상을 기본 키(pk)로 조회
    todo = get_object_or_404(Todo, pk=pk)
    
    if request.method == 'POST':
        # 기존 인스턴스(instance=todo)에 새로운 POST 데이터를 덮어씌웁니다.
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todos:todo_list')
    else:
        # 수정 화면 조회 시 기존 값을 채워 폼을 생성합니다.
        form = TodoForm(instance=todo)
        
    return render(request, 'todos/todo_form.html', {'form': form, 'action': '수정'})

def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    # POST 방식으로 요청이 들어오면 삭제를 처리합니다.
    if request.method == 'POST':
        todo.delete()
    return redirect('todos:todo_list')

class AboutView(View):
    def get(self, request):
        return render(request, 'todos/about.html')
```

---

## 3단계: 애플리케이션 URL 매핑 파일 수정
- **파일 경로**: `todos/urls.py` (전체 덮어쓰기 권장)
- **작성할 내용**: 뷰 함수 이름과 URL 경로를 다시 매핑합니다. 수정/삭제의 대상 id를 URL 파라미터인 `<int:pk>` 형태로 전달할 수 있도록 최신 경로 규칙을 적용합니다.

```python
from django.urls import path
from . import views

app_name = 'todos'

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('create/', views.todo_create, name='todo_create'),
    path('<int:pk>/update/', views.todo_update, name='todo_update'),
    path('<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('about/', views.AboutView.as_view(), name='about'),
]
```

---

## 4단계: HTML 템플릿 파일 생성 및 작성

`todos/templates/todos/` 디렉토리에 아래 4개의 템플릿 파일들을 작성합니다. (폴더가 없는 경우 새로 만드세요.)

### 1) 공통 베이스 템플릿
- **파일 경로**: `todos/templates/todos/base.html`
- **설명**: 프로젝트 전체 페이지에서 공유할 헤더, 네비게이션, 푸터 영역을 정의합니다.

```html
{% load static %}
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TodoBoard</title>
    <!-- 구글 폰트 적용 -->
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Noto+Sans+KR:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'todos/css/style.css' %}">
</head>
<body>
    <header class="app-header">
        <div class="header-container">
            <h1 class="logo"><a href="{% url 'todos:todo_list' %}">TodoBoard</a></h1>
            <nav class="nav-links" style="display: flex; align-items: center; gap: 20px;">
                <a href="{% url 'todos:todo_list' %}" class="nav-item">할일 목록</a>
                <a href="{% url 'todos:about' %}" class="nav-item">소개</a>
            </nav>
        </div>
    </header>

    <main class="app-main">
        <div class="main-container">
            {% block content %}
            {% endblock %}
        </div>
    </main>

    <footer class="app-footer">
        <div class="footer-container">
            <p>TodoBoard. 모든 권리 보유.</p>
        </div>
    </footer>
</body>
</html>
```

### 2) 할일 목록 조회 화면
- **파일 경로**: `todos/templates/todos/todo_list.html`
- **설명**: 등록된 할 일들을 카드 레이아웃으로 렌더링하고 각각 수정 및 삭제할 수 있는 동작 링크를 배치합니다.

```html
{% extends 'todos/base.html' %}

{% block content %}
<div class="content-header">
    <div class="header-text">
        <h2 class="section-title">나의 할일 관리</h2>
        <p class="section-desc">체계적이고 직관적인 오늘 하루의 할일 목록입니다.</p>
    </div>
    <a href="{% url 'todos:todo_create' %}" class="btn btn-primary">새 할일 등록</a>
</div>

<div class="todo-board-container">
    <div class="todo-grid">
        {% for todo in todos %}
            <div class="todo-card {% if todo.is_completed %}completed{% endif %}">
                <div class="todo-card-header">
                    <span class="status-badge">
                        {% if todo.is_completed %}완료{% else %}대기중{% endif %}
                    </span>
                    <span class="todo-date">{{ todo.created_at|date:"Y-m-d H:i" }}</span>
                </div>
                <h3 class="todo-title">{{ todo.title }}</h3>
                {% if todo.content %}
                    <p class="todo-body">{{ todo.content }}</p>
                {% endif %}
                <div class="todo-actions">
                    <a href="{% url 'todos:todo_update' todo.pk %}" class="btn-text">수정</a>
                    <!-- 삭제는 CSRF 토큰 검증을 통과하도록 안전하게 POST 폼으로 처리합니다. -->
                    <form action="{% url 'todos:todo_delete' todo.pk %}" method="post" class="delete-form" onsubmit="return confirm('정말 이 할일을 삭제하시겠습니까?');">
                        {% csrf_token %}
                        <button type="submit" class="btn-text btn-delete">삭제</button>
                    </form>
                </div>
            </div>
        {% empty %}
            <div class="empty-state">
                <p>등록된 할일이 없습니다. 상단의 '새 할일 등록' 버튼을 눌러 추가해 보세요.</p>
            </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

### 3) 등록 및 수정 입력 폼 화면
- **파일 경로**: `todos/templates/todos/todo_form.html`
- **설명**: 백엔드에서 전달된 `form` 객체를 활용해 필드를 순회하며 에러 메시지를 보여주고, 보안 토큰(`csrf_token`)을 주입한 입력 양식을 렌더링합니다.

```html
{% extends 'todos/base.html' %}

{% block content %}
<div class="form-container">
    <div class="form-card">
        <h2 class="form-title">할일 {{ action }}</h2>
        <p class="form-desc">오늘 마쳐야 할 할일의 상세한 내용을 등록하거나 수정합니다.</p>
        
        <form method="post" class="todo-form-body">
            <!-- 보안 공격(CSRF)을 방어하기 위한 난수 토큰 동봉 필수 -->
            {% csrf_token %}
            
            <!-- 백엔드에서 지정한 위젯과 필드를 반복하며 출력 -->
            {% for field in form %}
                <div class="form-group">
                    <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                    {{ field }}
                    {% if field.errors %}
                        <div class="field-errors">
                            {% for error in field.errors %}
                                <span class="error-text">{{ error }}</span>
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
            {% endfor %}
            
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">저장하기</button>
                <a href="{% url 'todos:todo_list' %}" class="btn btn-secondary">취소</a>
            </div>
        </form>
    </div>
</div>
{% endblock %}
```

### 4) 정보 소개 화면
- **파일 경로**: `todos/templates/todos/about.html`
- **설명**: 웹 어플리케이션을 간단하게 설명해 주는 고정 HTML 템플릿입니다.

```html
{% extends 'todos/base.html' %}

{% block content %}
<div class="about-container">
    <div class="about-card">
        <h2 class="about-title">TodoBoard 프로젝트</h2>
        <p class="about-lead">Django 프레임워크 학습을 위해 점진적으로 구축하는 할일 관리 웹애플리케이션입니다.</p>
        <div class="about-details">
            <p>본 프로젝트는 Django의 기본 MVT 패턴부터 데이터베이스 ORM, 폼 처리, 관리자 설정, 사용자 인증 시스템, 그리고 Django REST Framework를 활용한 API 구축 및 자바스크립트 Fetch 비동기 통신까지 아우르는 실습 결과물입니다.</p>
            <p>매 단계마다 모범 사례를 적용하여 견고하고 현대적인 아키텍처로 웹서비스를 설계해 나가는 과정을 포함하고 있습니다.</p>
        </div>
    </div>
</div>
{% endblock %}
```

---

## 5단계: 웹 앱 디자인을 위한 CSS 스타일 정의
- **파일 경로**: `todos/static/todos/css/style.css`
- **설명**: 전체 템플릿의 UI 레이아웃, 컬러 파레트, 폰트, 카드 레이아웃, 호버 효과 등 고급 디자인 요소를 적용합니다.
*(스타일의 구체적인 소스 코드는 최종 단계인 08번 실습 가이드와 동일하게 최종 완성본 `style.css`로 일체 등록됩니다.)*

---

## 데이터베이스 마이그레이션 실행
새로 변경된 데이터 모델이나 구조가 있을 때, 터미널을 열고 다음의 명령어를 실행하여 변경사항을 최종 반영합니다.
```bash
python manage.py makemigrations
python manage.py migrate
```
이후 로컬 서버를 기동하여 폼과 유효성 검사 기능이 브라우저에서 원활하게 작용하는지 점검합니다.
```bash
python manage.py runserver
```
