# [06] Django Admin과 인증 시스템 실습 가이드

---

## 실습 요약 및 핵심 흐름
1. **Custom User 모델 정의 및 설정**: `AbstractUser`를 확장한 `CustomUser` 모델을 만들고 `settings.py`에 주입합니다.
2. **외래키 관계 설정**: `Todo` 모델이 작성자(`author`)를 가질 수 있도록 Custom User와 ForeignKey 관계를 설정합니다.
3. **어드민 화면 등록**: `admin.py` 파일 내에 Custom User와 Todo 모델을 맞춤 화면 레이아웃에 맞춰 등록합니다.
4. **인증 폼 및 뷰 연동**: 회원가입 폼을 제작하고 회원가입, 로그인, 로그아웃을 처리하는 뷰 함수 및 URL 경로를 매핑합니다.
5. **접근 통제**: `@login_required` 데코레이터를 이용해 비로그인 사용자를 제한하고, 저장 시 현재 사용자를 작성자로 바인딩합니다.

---

## 1단계: 모델 파일 수정 (Custom User 및 외래키 연결)
- **파일 경로**: `todos/models.py` (전체 덮어쓰기 권장)
- **작성할 내용**: 기본 User 모델 대신 별도의 닉네임(`nickname`) 필드를 포함하는 `CustomUser`를 새롭게 정의하고, `Todo` 모델에 작성자 필드(`author`)를 외래키로 추가합니다.

```python
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# 1. Django 기본 User 모델을 확장하여 nickname 필드가 추가된 Custom User 정의
class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.username

# 2. Todo 모델에 작성자(author) 외래키 관계 매핑 추가
class Todo(models.Model):
    # settings.AUTH_USER_MODEL을 외래키의 대상 모델로 지정하여 Custom User를 바인딩합니다.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='todos', 
        null=True, 
        blank=True
    )
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```

---

## 2단계: 환경 설정 파일 수정
- **파일 경로**: `todoboard/settings.py`
- **작성할 내용**: 장고가 기본 User 모델 대신 우리가 새로 작성한 `CustomUser`를 인증용 모델로 사용하도록 환경 변수를 추가하고, 비로그인 상태일 때 접근 제한 시 이동시킬 로그인 URL 명칭을 세팅합니다.

`settings.py` 파일의 하단 혹은 적절한 위치에 다음 2개의 설정을 추가합니다.
```python
# 1. Custom User 모델 등록 (앱이름.모델명)
AUTH_USER_MODEL = 'todos.CustomUser'

# 2. 로그인 필수 접근 제어 시 리다이렉트할 경로 지정
LOGIN_URL = 'todos:login'
```

---

## 3단계: 장고 어드민 파일 수정
- **파일 경로**: `todos/admin.py` (전체 덮어쓰기 권장)
- **작성할 내용**: 관리자 화면에서 Custom User의 닉네임이 잘 보이도록 목록 그리드 및 상세 화면 영역을 사용자 정의(Custom)하고, Todo를 관리하기 위한 목록 열, 필터 박스, 검색 도구를 배치합니다.

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Todo

# 1. Custom User 모델의 속성 커스터마이징 등록
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # 목록 화면에 표시할 컬럼 지정
    list_display = ['username', 'email', 'nickname', 'is_staff']
    # 상세 정보 조회/수정 화면에서 닉네임 필드 레이아웃 추가
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nickname',)}),
    )
    # 회원 생성 화면(새 유저 등록) 시 닉네임 필드 레이아웃 추가
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('nickname',)}),
    )

# 2. Todo 관리자 화면 커스터마이징 등록
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'created_at']
    search_fields = ['title', 'content']

# 장고 어드민에 맵핑 클래스와 함께 모델 최종 등록
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Todo, TodoAdmin)
```

---

## 4단계: 회원가입용 폼 추가
- **파일 경로**: `todos/forms.py`
- **작성할 내용**: 기존 `UserCreationForm`은 기본 User 객체 생성을 타겟팅하므로, 이를 상속받아 `CustomUser` 객체를 올바르게 인스턴스화하고 추가된 `email`과 `nickname` 필드가 가입창에 함께 출력되도록 커스텀 폼을 하단에 추가합니다.

기존 `TodoForm`이 적힌 `todos/forms.py` 하단에 다음 코드를 덧붙여 작성합니다.
```python
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # 대상 모델을 CustomUser로 지정
        model = CustomUser
        # 회원 가입 데이터 수집 시 이메일과 닉네임을 기본 필드 뒤에 덧붙여 출력
        fields = UserCreationForm.Meta.fields + ('email', 'nickname')
        labels = {
            'email': '이메일 주소',
            'nickname': '닉네임'
        }
```

---

## 5단계: 회원 기능 및 로그인 권한 제어 뷰 작성
- **파일 경로**: `todos/views.py` (전체 덮어쓰기 권장)
- **작성할 내용**: 회원가입, 로그인, 로그아웃의 백엔드 처리와 세션 등록 기능을 작성하고, 모든 CRUD 기능 함수 상단에 `@login_required` 데코레이터를 붙여 보안 관리를 구성합니다.

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseForbidden
from .models import Todo
from .forms import TodoForm, CustomUserCreationForm

# 1. 로그인한 사용자 본인의 할일 목록만 필터링하여 노출
@login_required
def todo_list(request):
    todos = Todo.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'todos/todo_list.html', {'todos': todos})

# 2. 할일 등록 시 현재 로그인 중인 사용자의 세션 정보(request.user)를 작성자로 주입
@login_required
def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            # commit=False: DB 인서트 직전에 정보 수집만 수행한 대기 상태 객체 반환
            todo = form.save(commit=False)
            todo.author = request.user # 현재 세션 유저를 작성자로 지정
            todo.save() # 최종 DB에 저장
            return redirect('todos:todo_list')
    else:
        form = TodoForm()
    return render(request, 'todos/todo_form.html', {'form': form, 'action': '등록'})

# 3. 작성자가 아니면 수정을 할 수 없도록 보안 통제 추가
@login_required
def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    # 현재 접근한 사용자가 실제 등록자가 아니면 403 금지 에러 반환
    if todo.author != request.user:
        return HttpResponseForbidden("본인의 할일만 수정할 수 있습니다.")
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todos:todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todos/todo_form.html', {'form': form, 'action': '수정'})

# 4. 작성자가 아니면 삭제를 할 수 없도록 보안 통제 추가
@login_required
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if todo.author != request.user:
        return HttpResponseForbidden("본인의 할일만 삭제할 수 있습니다.")
    
    if request.method == 'POST':
        todo.delete()
    return redirect('todos:todo_list')

# 5. 회원가입 뷰
def signup(request):
    # 이미 로그인한 상태라면 목록 화면으로 돌려보냅니다.
    if request.user.is_authenticated:
        return redirect('todos:todo_list')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user) # 가입 성공 시 세션 로그인도 원스톱으로 처리
            return redirect('todos:todo_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'todos/signup.html', {'form': form})

# 6. 로그인 뷰
def login_view(request):
    if request.user.is_authenticated:
        return redirect('todos:todo_list')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # ID / Password의 진위 검증 가동
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user) # 통과된 사용자를 세션에 등록
                return redirect('todos:todo_list')
    else:
        form = AuthenticationForm()
    return render(request, 'todos/login.html', {'form': form})

# 7. 로그아웃 뷰
def logout_view(request):
    auth_logout(request) # 세션 해제 및 세션 쿠키 소멸 처리
    return redirect('todos:login')

class AboutView(View):
    def get(self, request):
        return render(request, 'todos/about.html')
```

---

## 6단계: URL 매핑 파일에 인증 루트 결합
- **파일 경로**: `todos/urls.py`
- **작성할 내용**: 회원가입, 로그인, 로그아웃 페이지를 호출할 수 있는 주소 체계를 추가합니다.

```python
from django.urls import path
from . import views

app_name = 'todos'

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('create/', views.todo_create, name='todo_create'),
    path('<int:pk>/update/', views.todo_update, name='todo_update'),
    path('<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.AboutView.as_view(), name='about'),
]
```

---

## 7단계: 로그인 & 회원가입 HTML 템플릿 제작 및 베이스 템플릿 변경

`todos/templates/todos/` 디렉토리에 아래 2개의 템플릿 파일을 신규 작성하고, 기존의 `base.html`도 사용자의 로그인 유무에 따라 버튼이 다르게 보이도록 갱신합니다.

### 1) 로그인 화면 템플릿
- **파일 경로**: `todos/templates/todos/login.html`
```html
{% extends 'todos/base.html' %}

{% block content %}
<div class="form-container">
    <div class="form-card">
        <h2 class="form-title">로그인</h2>
        <p class="form-desc">TodoBoard 서비스를 이용하시려면 계정 정보를 입력하세요.</p>
        
        <form method="post" class="todo-form-body">
            {% csrf_token %}
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
            
            {% if form.non_field_errors %}
                <div class="field-errors">
                    {% for error in form.non_field_errors %}
                        <span class="error-text">{{ error }}</span>
                    {% endfor %}
                </div>
            {% endif %}
            
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">로그인</button>
            </div>
        </form>
        
        <div class="form-footer-link" style="margin-top: 24px; text-align: center; font-size: 14px; color: var(--text-muted);">
            계정이 없으신가요? <a href="{% url 'todos:signup' %}" style="color: var(--primary-color); font-weight: 700;">회원가입</a>
        </div>
    </div>
</div>
{% endblock %}
```

### 2) 회원가입 화면 템플릿
- **파일 경로**: `todos/templates/todos/signup.html`
```html
{% extends 'todos/base.html' %}

{% block content %}
<div class="form-container">
    <div class="form-card">
        <h2 class="form-title">회원가입</h2>
        <p class="form-desc">새로운 계정을 만들고 TodoBoard 일정을 관리해 보세요.</p>
        
        <form method="post" class="todo-form-body">
            {% csrf_token %}
            {% for field in form %}
                <div class="form-group">
                    <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                    {{ field }}
                    {% if field.help_text %}
                        <span class="field-help" style="font-size: 11px; color: var(--text-muted); line-height: 1.3;">{{ field.help_text|safe }}</span>
                    {% endif %}
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
                <button type="submit" class="btn btn-primary">가입하기</button>
            </div>
        </form>
        
        <div class="form-footer-link" style="margin-top: 24px; text-align: center; font-size: 14px; color: var(--text-muted);">
            이미 계정이 있으신가요? <a href="{% url 'todos:login' %}" style="color: var(--primary-color); font-weight: 700;">로그인</a>
        </div>
    </div>
</div>
{% endblock %}
```

### 3) 공통 베이스 템플릿 수정
- **파일 경로**: `todos/templates/todos/base.html`
- **수정 내용**: 상단 네비게이션에 사용자가 로그인 상태인지 판별(`{% if user.is_authenticated %}`)하여 로그아웃 버튼과 인사말, 혹은 로그인/회원가입 버튼이 유동적으로 나오게 코드를 교체합니다.

```html
{% load static %}
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TodoBoard</title>
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
                <!-- 사용자 로그인 유무에 따른 메뉴 출력 분기 -->
                {% if user.is_authenticated %}
                    <span class="user-greeting" style="font-weight: 700; color: var(--primary-color); font-size: 14px;">
                        {{ user.nickname|default:user.username }}님
                    </span>
                    <a href="{% url 'todos:logout' %}" class="nav-item" style="color: #ef4444;">로그아웃</a>
                {% else %}
                    <a href="{% url 'todos:login' %}" class="nav-item">로그인</a>
                    <a href="{% url 'todos:signup' %}" class="nav-item">회원가입</a>
                {% endif %}
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
