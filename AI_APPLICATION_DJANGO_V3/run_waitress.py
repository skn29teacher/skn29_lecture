import os
from urllib.parse import urlparse
from waitress import serve
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.views.static import serve as django_static_serve
from django.conf import settings

# 중요: Django 설정 모듈(Settings)을 가리키는 환경 변수를 최상단에서 기본값으로 지정합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todoboard.settings.production')

class StaticAndMediaFilesHandler(StaticFilesHandler):
    def __init__(self, application):
        super().__init__(application)
        self.media_url = urlparse(settings.MEDIA_URL)

    def _should_handle(self, path):
        return (path.startswith(self.base_url.path) and not self.base_url.netloc) or \
               (path.startswith(self.media_url.path) and not self.media_url.netloc)

    def serve(self, request):
        if request.path.startswith(self.media_url.path):
            path = request.path[len(self.media_url.path):]
            return django_static_serve(request, path, document_root=settings.MEDIA_ROOT)
        return super().serve(request)

application = StaticAndMediaFilesHandler(get_wsgi_application())

if __name__ == '__main__':
    print("Starting Waitress WSGI server on http://127.0.0.1:8000")
    serve(
        application,
        host='127.0.0.1',
        port=8000,
        threads=4,
        trusted_proxy='127.0.0.1',
        trusted_proxy_headers={'x-forwarded-proto', 'x-forwarded-for', 'x-forwarded-host'}
    )