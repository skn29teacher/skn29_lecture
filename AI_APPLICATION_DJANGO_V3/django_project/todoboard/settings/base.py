# 개발과 운영환경에서 공통으로 사용하는 설정
import environ
from pathlib import Path

# settings/base.py 위치에서 3단계 상위로 이동 프로젝트 루트경로
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# django-environ 초기화
env = environ.Env(
    DEBUG=(bool,False)
)

# .env 파일 읽기
environ.Env.read_env(env_file=BASE_DIR / '.env')

SECRET_KEY=env('SECRET_KEY')
DEBUG=env('DEBUG')

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'todos',  # 추가
    'rest_framework', # rest api 추가
]

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
                # 개발한 전역 변수 공급용 컨텍스트 프로세서 함수 등록
                'todos.context_processors.global_spa_config',
            ],
        },
    },
]

WSGI_APPLICATION = 'todoboard.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'  # 각 어플하위의 static
STATICFILES_DIRS = [    # 루트디레터리의 static
    BASE_DIR / 'static',
]

# 3. 배포용 정적 자원 수집 최종 물리 디렉토리 경로 정의 (기존 설정과 중복되지 않는 고유 명칭 부여 권장)
STATIC_ROOT = BASE_DIR / 'staticfiles'


MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 외래키 관련
# 1. Custom User 모델 등록 (앱이름.모델명)
AUTH_USER_MODEL = 'todos.CustomUser'

# 2. 로그인 필수 접근 제어 시 리다이렉트할 경로 지정
LOGIN_URL = 'todos:login'