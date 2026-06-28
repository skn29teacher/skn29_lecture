# Django 운영 서버 설정 분리 및 환경 변수 관리

본 단계에서는 Django 프로젝트를 개발(Local) 환경과 운영(Production) 환경으로 분리하여 안전하고 효율적으로 관리할 수 있도록 설정을 패키지화하고 환경 변수를 적용하는 방법을 학습합니다.

---

## 1. 설정 분리의 필요성

Django 프로젝트를 처음 생성하면 `settings.py` 파일 하나에 모든 설정이 저장됩니다. 하지만 실제 서비스를 운영할 때는 다음과 같은 이유로 설정을 반드시 분리해야 합니다.

- **보안 강화**: 암호화 키(`SECRET_KEY`), 데이터베이스 접속 정보, API 키 등 민감한 정보가 소스 코드에 하드코딩되어 Git과 같은 버전 관리 시스템에 노출되는 것을 방지합니다.
- **환경별 차별화**: 개발 환경에서는 디버그 모드(`DEBUG = True`)를 켜서 에러 정보를 확인하지만, 운영 환경에서는 보안과 성능을 위해 디버그 모드를 반드시 꺼야(`DEBUG = False`) 합니다.
- **인프라 설정 다양화**: 개발 시에는 가벼운 SQLite를 사용하고, 운영 환경에서는 PostgreSQL 또는 MySQL과 같은 관리형 데이터베이스 시스템을 연결해야 합니다.

---

## 2. django-environ 라이브러리 개요

`django-environ`은 Twelve-Factor App 방법론에 따라 Django 설정을 환경 변수(Environment Variables)로부터 가져오도록 돕는 가장 인기 있는 라이브러리입니다. `.env` 파일을 로컬 개발 환경에 배치하여 환경 변수를 편리하게 로드할 수 있도록 지원합니다.

---

## 3. 단계별 구성 가이드

### 1단계: 의존성 패키지 정의
프로젝트 루트 디렉터리에 `requirements.txt` 파일을 생성하고 프로젝트에 필요한 라이브러리를 정의합니다. 환경 변수 관리를 위해 `django-environ`이 포함되어야 합니다.

- 파일명: `requirements.txt`
```text
Django>=5.0,<6.0
django-cors-headers
djangorestframework
django-environ
Pillow
```

### 2단계: 설정 디렉터리 구성 및 settings.py 이관
기존 `todoboard/settings.py` 파일을 제거하고, 다음과 같이 패키지 구조로 디렉터리를 구성합니다.

```text
todoboard/
└── settings/
    ├── __init__.py
    ├── base.py
    ├── local.py
    └── production.py
```

#### 공통 설정 파일 작성
`base.py`에는 개발과 운영 환경에서 공통으로 사용하는 설정을 작성합니다. 이때 `BASE_DIR` 경로가 `settings/base.py` 파일 기준으로 설정되므로, 기존보다 1단계 더 상위로 가도록 `parent.parent.parent`로 수정해야 합니다.

- 파일명: `todoboard/settings/base.py`
```python
import environ
from pathlib import Path

# settings/base.py 위치에서 3단계 상위로 이동하여 프로젝트 루트 경로 지정
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# django-environ 초기화
env = environ.Env(
    DEBUG=(bool, False)
)

# .env 파일 읽기
environ.Env.read_env(env_file=BASE_DIR / '.env')

# 환경 변수로부터 로드
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'todos',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'todoboard.urls'

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
                'todos.context_processors.global_spa_config',
            ],
        },
    },
]

WSGI_APPLICATION = 'todoboard.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

AUTH_USER_MODEL = 'todos.CustomUser'

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = 'todos:login'
CORS_ALLOW_ALL_ORIGINS = True
```

#### 로컬 개발용 설정 파일 작성
- 파일명: `todoboard/settings/local.py`
```python
from .base import *

# 로컬 개발 환경 설정
DEBUG = True

# 개발 중에는 SQLite 데이터베이스 사용
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

ALLOWED_HOSTS = ['*']
```

#### 운영 환경용 설정 파일 작성
- 파일명: `todoboard/settings/production.py`
```python
from .base import *

# 운영 환경 설정
DEBUG = False

# 쉼표로 구분된 호스트 목록을 리스트로 파싱하여 로드
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# 데이터베이스 설정 (SQLite 임시 적용, 이후 단계에서 PostgreSQL 연동 예정)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### 초기화 파일 작성
- 파일명: `todoboard/settings/__init__.py`
```python
# Django settings 패키지 지정을 위한 파일
```

### 3단계: 환경 변수 파일 정의
로컬 및 운영 서버의 디렉터리 루트에 실제 설정 값을 주입하는 `.env` 파일을 배치합니다. 깃(Git)에 등록할 수 있도록 설정 목록 포맷을 적어둔 `.env.template` 파일도 함께 관리합니다.

- 파일명: `.env`
```env
DEBUG=True
SECRET_KEY=django-insecure-t58eufc4a(&zvr)yq28g5ou+x=g!@1bj4x-@d5+we#rns5@qb%
ALLOWED_HOSTS=localhost,127.0.0.1
```

- 파일명: `.env.template`
```env
DEBUG=
SECRET_KEY=
ALLOWED_HOSTS=
```

### 4단계: Django 진입 모듈 설정
설정 파일이 패키지 형태로 분리되었으므로, Django를 실행하는 모듈들의 기본 설정을 `todoboard.settings`에서 `todoboard.settings.local`로 수정하여 로컬 환경에서 명령어 실행 시 자동으로 로컬 설정이 로드되도록 합니다.

- 파일명: `manage.py`
```python
# 기존 코드 수정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todoboard.settings.local')
```

- 파일명: `todoboard/wsgi.py` 및 `todoboard/asgi.py`
```python
# 기존 코드 수정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todoboard.settings.local')
```

---

## 4. 구동 테스트
설정이 정상적으로 분리되었는지 로컬 서버 구동 명령어로 검증합니다.

```bash
# 로컬 기본 설정을 이용한 서버 테스트
python manage.py runserver

# 운영 설정을 임시 적용하여 점검하는 테스트
python manage.py check --settings=todoboard.settings.production
```
이로써 서버의 소스 코드를 건드리지 않고 환경 변수 변경만으로 설정이 유연하게 제어되는 구조를 완성했습니다.
