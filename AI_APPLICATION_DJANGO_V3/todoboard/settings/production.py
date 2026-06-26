# 운영환경(배포)
from .base import *

DEBUG=False

# 호스트목록
ALLOWED_HOSTS=env.list('ALLOWED_HOSTS', default=['localhost','127.0.0.1'])

# PostgreSQL 설정
# django-environ의 env.db() 함수는 DATABASE_URL 환경변수를 읽어서 자동으로 설정값을 빌드
DATABASES = {
    'default': env.db('DATABASE_URL')
}