# 미디어 파일 업로드 백엔드 설계

비동기 웹 애플리케이션(SPA) 환경에서 사용자가 게시글이나 할 일 항목에 이미지나 문서를 첨부하여 업로드하는 경우, 이러한 자원은 정적 자원(Static)과 구분하여 미디어 파일(Media)로 처리해야 합니다. Django REST Framework(DRF) 환경에서 미디어 파일을 수용하기 위한 데이터베이스 모델 설계 및 직렬화(Serialization) 기법을 학습합니다.

---

## 1. 정적 파일과 미디어 파일의 구분

- **정적 파일 (Static Files)**: 개발자가 웹 서비스를 구축할 때 미리 준비하여 배치하는 자원(CSS 스타일시트, 브라우저용 Javascript, 로고 이미지 등)입니다.
- **미디어 파일 (Media Files)**: 웹 서비스 가동 후 사용자가 폼 업로드 등을 통해 백엔드 서버에 업로드하여 적재되는 자원(인증용 사진, 게시판 첨부 파일 등)입니다.

---

## 2. 미디어 관리를 위한 Django 전역 설정

사용자가 전송한 파일을 서버가 안전하게 수신하고 이를 다시 브라우저로 서비스하기 위해 두 가지 설정 변수를 구성합니다.

### settings.py 설정
```python
# settings.py

# 1. 사용자가 업로드한 파일에 접근할 때 브라우저가 요청할 기준 URL 경로
MEDIA_URL = 'media/'

# 2. 업로드된 실제 파일이 물리적으로 복사되어 보관될 서버 측 디렉토리 경로
MEDIA_ROOT = BASE_DIR / 'media'
```

### 개발용 미디어 서빙 라우터 연동
실제 서비스 배포 단계에서는 Nginx나 AWS S3 같은 전용 웹 서버 인프라를 통해 미디어 파일을 서빙하지만, 개발 단계(로컬 호스트)에서는 Django 경량 서버가 미디어 요청을 중개할 수 있도록 메인 라우터 설정을 연동해주어야 합니다.
파일명: `todoboard/urls.py`
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todos.urls')),
]

# 개발 모드(DEBUG = True)인 경우에 한해서만 미디어 URL을 라우팅 테이블에 주입합니다.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 3. 백엔드 API 고도화 구현

할 일(Todo) 모델이 이미지 자원을 보관할 수 있도록 구조를 확장하고, 이를 API로 노출하기 위해 직렬화기를 연동합니다.

### 1단계: 모델에 이미지 필드 추가
Django에서 이미지를 검증하고 다루기 위해서는 이미지 라이브러리인 Pillow 설치가 필요합니다.
```bash
pip install Pillow
```

파일명: `todos/models.py`
```python
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)

class Todo(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='todos', null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    # 이미지 저장을 위한 ImageField 추가 (upload_to 설정으로 미디어 루트 하위 세부 경로 구획)
    image = models.ImageField(upload_to='todos/images/', blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```

데이터베이스 스키마가 변경되었으므로 변경 이력 설계도를 생성하고 데이터베이스에 최종 구워냅니다.
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2단계: 직렬화기(Serializer) 확장
API가 이미지 자원을 받아들이고 가공된 미디어 주소를 출력할 수 있도록 Serializer의 필드 목록에 이미지를 반영합니다.
파일명: `todos/serializers.py`
```python
from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Todo
        # fields 리스트에 'image' 필드를 새로 노출합니다.
        fields = ['id', 'author', 'author_username', 'title', 'content', 'image', 'is_completed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
```

이렇게 처리하면 DRF는 사용자가 업로드한 멀티파트 파일을 자동으로 파싱하여 `MEDIA_ROOT/todos/images/`에 안착시키며, 브라우저가 해당 투두를 GET 요청으로 수집할 때 자동으로 전체 접근 주소(예: `http://127.0.0.1:8000/media/todos/images/photo.jpg`)를 연산하여 전달합니다.
