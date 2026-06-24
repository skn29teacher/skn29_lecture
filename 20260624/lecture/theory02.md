# MTV 패턴과 URL 라우팅 및 뷰

장고에서 사용자의 요청을 수신하여 URL 주소를 해독하고, 함수형 혹은 클래스형 뷰를 통해 HTTP 응답을 반환하는 구체적인 코드 작성 방법과 구조를 학습합니다.

---

## 1. URL 라우팅 설정 방법

장고 프로젝트는 메인 URL 파일에서 각 기능별 애플리케이션의 하위 URL 주소를 통합 관리하는 포워딩 방식을 채택합니다.

### 프로젝트 메인 URL 설정 (todoboard/urls.py)
외부에서 들어오는 모든 웹 요청의 진입점입니다. `include` 함수를 사용하여 하위 앱으로 요청을 토스합니다.
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 관리자 페이지 주소 매핑
    path('admin/', admin.site.urls),
    
    # 루트 주소('')로 오는 모든 요청은 todos 앱의 urls.py로 넘깁니다.
    path('', include('todos.urls')),
]
```

### 애플리케이션 내부 URL 설정 (todos/urls.py)
앱 단위 폴더 내부에 직접 생성하는 라우팅 파일입니다. 메인 라우터로부터 전달받은 하위 주소를 뷰 함수/클래스와 직접 1대1 매핑합니다.
```python
from django.urls import path
from . import views

# 앱의 네임스페이스를 지정하여 템플릿 등에서 주소를 역추적(reverse)할 때 식별자로 씁니다.
app_name = 'todos'

urlpatterns = [
    # 'http://127.0.0.1:8000/' 주소 요청 시 views.todo_list_welcome 함수 실행
    path('', views.todo_list_welcome, name='todo_welcome'),
    
    # 'http://127.0.0.1:8000/about/' 주소 요청 시 views.AboutView 클래스 뷰 실행
    path('about/', views.AboutView.as_view(), name='about'),
]
```

---

## 2. 함수 기반 뷰 (FBV) 작성 방법

함수 기반 뷰는 파이썬의 일반 함수 형태로 작성합니다. 브라우저의 HTTP 요청 정보를 담은 `request` 객체를 첫 번째 인자로 필수 수신하며, 반드시 `HttpResponse` 또는 `render` 등의 응답 객체를 리턴해야 합니다.

### FBV 상세 소스코드 예시 (todos/views.py)
```python
from django.http import HttpResponse

def todo_list_welcome(request):
    # request: 클라이언트로부터 들어온 HTTP 요청 메타데이터가 담긴 객체
    # HttpResponse: 클라이언트 브라우저로 텍스트나 HTML을 담아 내보내는 응답 객체
    return HttpResponse("할일 관리 애플리케이션(TodoBoard) 방문을 환영합니다. (함수 기반 뷰)")
```
- 함수 기반 뷰는 구조가 단순하여 직관적으로 코드를 한눈에 파악할 수 있는 강점이 있습니다.

---

## 3. 클래스 기반 뷰 (CBV) 작성 방법

클래스 기반 뷰는 장고 내장 `django.views.View` 클래스를 상속받아 정의합니다. HTTP 요청 메소드(GET, POST, PUT, DELETE 등)에 해당하는 이름을 가진 소문자 메소드를 정의하여 분기 처리를 자동화합니다.

### CBV 상세 소스코드 예시 (todos/views.py)
```python
from django.http import HttpResponse
from django.views import View

class AboutView(View):
    # 클라이언트가 GET 요청을 보냈을 때 자동으로 실행되는 메소드
    def get(self, request):
        return HttpResponse("이 애플리케이션은 사용자 기반의 할일 관리 웹앱입니다. (클래스 기반 뷰)")

    # 클라이언트가 POST 요청을 보냈을 때 자동으로 실행되는 메소드 (예시)
    def post(self, request):
        return HttpResponse("데이터가 제출되었습니다.")
```

### URL 매핑 시 주의 사항
- 클래스 기반 뷰를 `urls.py`에 등록할 때는 반드시 클래스명 뒤에 `.as_view()` 메소드를 호출해 주어야 합니다.
- `as_view()`는 클래스의 인스턴스를 생성하고, 들어오는 HTTP 요청 메소드 타입을 분석하여 적절한 내부 클래스 메소드(get, post 등)로 연결해 주는 진입점 역할을 합니다.
