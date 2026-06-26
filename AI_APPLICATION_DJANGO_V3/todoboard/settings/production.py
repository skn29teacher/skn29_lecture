from .base import *

# 운영 환경용 설정
DEBUG = False

# 운영 환경의 허용 호스트 설정
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# PostgreSQL 데이터베이스 설정
DATABASES = {
    'default': env.db('DATABASE_URL')
}

# 운영 환경용 정적 파일 수집 경로 설정
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ==============================================================================
# 보안 강화 설정 (HTTPS 및 쿠키 보안)
# ==============================================================================

# Nginx 리버스 프록시로부터 전달받은 SSL 헤더 검증 설정
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# HTTPS 접속이 아닐 경우 자동으로 HTTPS로 리다이렉션 수행
SECURE_SSL_REDIRECT = True

# 세션 및 CSRF 쿠키의 Secure 플래그 활성화 (HTTPS를 통해서만 전송되도록 강제)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HTTP Strict Transport Security (HSTS) 활성화 (브라우저가 1년간 HTTPS로만 접속하도록 지시)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# 브라우저 MIME Sniffing 방어 필터 적용
SECURE_CONTENT_TYPE_NOSNIFF = True