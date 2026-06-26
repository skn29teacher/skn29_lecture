# 운영환경(배포)
from .base import *

DEBUG=False

# 호스트목록
ALLOWED_HOSTS=env.list('ALLOWED_HOSTS', default=['localhost','127.0.0.1'])

# 임시 -> PostgreSQL 변경예정
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}