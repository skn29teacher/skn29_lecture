# [07] Django REST Framework 기초 API 실습 가이드

**Django REST Framework(DRF)** 를 적용하여 데이터베이스 객체 데이터를 JSON 문자열 포맷으로 변환 및 수신하는 직렬화기(Serializer)를 구축하고, `APIView` 클래스를 활용해 모던 REST 규격의 CRUD API 서버 백엔드를 직접 설계하는 방법을 설명합니다.

이전의 추상적인 이론 설명에서 벗어나, 어느 폴더의 어떤 파일을 어떻게 수정해야 하는지 구체적인 경로와 전체 소스코드를 빠짐없이 기록했습니다.

---

## 실습 요약 및 핵심 흐름
1. **DRF 패키지 환경 등록**: `settings.py` 내 `INSTALLED_APPS`에 `rest_framework` 모듈을 추가합니다.
2. **Serializer 정의**: `todos/serializers.py` 파일을 만들어 파이썬 객체 데이터와 JSON 포맷 간의 자동 변환 파이프라인을 설정합니다.
3. **API 뷰 클래스 개발**: `todos/api_views.py` 파일을 생성해 `APIView` 클래스를 상속한 HTTP GET/POST/PUT/DELETE 엔드포인트 핸들러를 작성합니다.
4. **URL 라우팅 설정**: API 주소를 구분하여 호출할 수 있도록 애플리케이션 `urls.py`를 업데이트합니다.

---

## 1단계: 환경 설정 파일 수정 (DRF 모듈 설치 및 등록)
- **파일 경로**: `todoboard/settings.py`
- **작성할 내용**: 장고에 REST API 어플리케이션 구축을 보조하는 `rest_framework` 패키지가 통합되도록 앱 목록에 추가합니다.

`settings.py`의 `INSTALLED_APPS` 리스트 안에 `'rest_framework'`를 등록합니다.
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 1. Django REST Framework 등록
    'rest_framework',
    
    'todos',
]
```

---

## 2단계: 직렬화기(Serializer) 정의
- **파일 경로**: `todos/serializers.py` (신규 생성)
- **작성할 내용**: `Todo` 모델과 맵핑하여 클라이언트에게 JSON으로 내보낼 항목과 데이터 수신 시 자동으로 검사할 규칙을 지정합니다. 작성자의 닉네임이나 유저네임(`author.username`)을 보기 위해 읽기 전용 필드를 결합합니다.

```python
from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    # ReadOnlyField: 유저 이름 필드를 읽기 전용(ReadOnly)으로 직렬화해 출력에 결합
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        # 1. 직렬화의 타겟이 되는 데이터베이스 모델 클래스 지정
        model = Todo
        
        # 2. JSON 데이터로 묶어 송수신할 컬럼 명칭 리스트 정의
        fields = [
            'id', 'author', 'author_username', 'title', 
            'content', 'is_completed', 'created_at', 'updated_at'
        ]
        
        # 3. 데이터 쓰기(POST/PUT) 요청 시 사용자 직접 수정을 막고 시스템이 자동 입력할 읽기전용 필드들 설정
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
```

---

## 3단계: API 뷰 파일 작성 (`APIView` 기반 엔드포인트 설계)
- **파일 경로**: `todos/api_views.py` (신규 생성)
- **작성할 내용**: `APIView` 클래스를 상속하여 HTTP 메소드와 일치하는 내부 함수(`get`, `post`, `put`, `delete`)를 선언하고, 데이터를 조회하거나 저장할 때의 유효성 검사 및 에러 응답 로직을 수록합니다.

```python
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Todo
from .serializers import TodoSerializer

# 1. 목록 조회 및 신규 생성 API 뷰
class TodoListAPIView(APIView):
    # 로그인 인증을 거친 검증된 클라이언트의 요청만 이 API에 진입할 수 있도록 허용합니다.
    permission_classes = [permissions.IsAuthenticated]

    # HTTP GET: 현재 로그인한 사용자가 등록한 할일들만 역순으로 조회하여 직렬화 전달
    def get(self, request):
        todos = Todo.objects.filter(author=request.user).order_by('-created_at')
        # many=True: 쿼리셋 목록 데이터를 다량 직렬화할 때 필수 옵션
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    # HTTP POST: 데이터 검증 후 신규 할일 객체 데이터베이스 영구 등록
    def post(self, request):
        # request.data를 직렬화기 생성자의 첫 인자로 주입하여 데이터를 바인딩
        serializer = TodoSerializer(data=request.data)
        
        if serializer.is_valid():
            # 저장(save)을 가동하면서 직렬화기 바깥에 있는 작성자(author) 속성에 현재 로그인 세션 계정 수동 지정
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        # 유효성 검사를 넘지 못하면 400 Bad Request와 에러 항목 메시지 JSON 리턴
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. 개별 상세 조회, 수정, 삭제 API 뷰
class TodoDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # 타겟 데이터의 식별과 계정 소유 권한을 조율하는 전처리기 도우미 함수
    def get_object(self, pk, user):
        todo = get_object_or_404(Todo, pk=pk)
        # 만약 본인의 데이터가 아니라면 403 Forbidden 권한 에러 방출
        if todo.author != user:
            self.permission_denied(self.request, message="본인의 할일이 아닙니다.")
        return todo

    # HTTP GET: 단일 데이터 상세 상세 조회
    def get(self, request, pk):
        todo = self.get_object(pk, request.user)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    # HTTP PUT: 단일 데이터 수정
    def put(self, request, pk):
        todo = self.get_object(pk, request.user)
        # 기존 Todo 인스턴스 정보와 새로 전달받은 입력 본문을 결합하여 수정 폼 직렬화기 로드
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # HTTP DELETE: 데이터 영구 삭제
    def delete(self, request, pk):
        todo = self.get_object(pk, request.user)
        todo.delete()
        # 성공적으로 지워졌음을 알리는 204 No Content 리턴
        return Response(status=status.HTTP_204_NO_CONTENT)
```

---

## 4단계: URL 매핑 파일에 API 라우트 연동
- **파일 경로**: `todos/urls.py`
- **작성할 내용**: 위에서 작성한 API 뷰 클래스들을 가져와 각각 `/todos/api/` 및 `/todos/api/<pk>/`에 주소 체계를 통합 배치합니다.

```python
from django.urls import path
from . import views
from . import api_views # API 뷰 모듈 추가 임포트

app_name = 'todos'

urlpatterns = [
    # 기존 HTML 템플릿용 뷰 매핑
    path('', views.todo_list, name='todo_list'),
    path('create/', views.todo_create, name='todo_create'),
    path('<int:pk>/update/', views.todo_update, name='todo_update'),
    path('<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.AboutView.as_view(), name='about'),
    
    # 신규 추가: REST API 백엔드 호출 전용 매핑 경로
    path('api/', api_views.TodoListAPIView.as_view(), name='api_todo_list'),
    path('api/<int:pk>/', api_views.TodoDetailAPIView.as_view(), name='api_todo_detail'),
]
```

---

## 동작 확인 및 테스트 가이드
서버를 켠 상태에서 REST API 개발 클라이언트 툴(Postman, Insomnia 등) 또는 브라우저 개발자 도구를 활용해 아래 엔드포인트에 로그인을 마친 뒤 요청을 보내 정상 응답이 수신되는지 파악합니다.

1. **로그인 상태로 주소창 테스트**:
   - `http://127.0.0.1:8000/todos/api/`
   - 정상 진입 시 Django REST Framework가 제공하는 웹 브라우저용 대화형 API 테스터 창이 뜨며 현재 사용자의 목록 JSON이 출력됩니다.
2. **비로그인(인증 헤더/세션 없음) 테스트**:
   - 로그아웃 후 위 주소로 강제 접속 시 `{"detail": "자격 인증 데이터가 제공되지 않았습니다."}` 라는 403 인증 경고 메시지가 JSON 형태로 반환되어야 합니다.
