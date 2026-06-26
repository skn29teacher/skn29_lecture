import os
from urllib.parse import urlparse
from waitress import serve
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.views.static import serve as django_static_serve
from django.conf import settings

# 중요: Django 설정 모듈(Settings)을 가리키는 환경 변수를 최상단에서 기본값으로 지정합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todoboard.settings.local')

# Waitress 단독 구동 시 정적(Static) 파일과 미디어(Media) 파일을 모두 서빙하기 위한 커스텀 WSGI 핸들러
class StaticAndMediaFilesHandler(StaticFilesHandler):
    def __init__(self, application):
        super().__init__(application)
        # settings.MEDIA_URL을 urlparse로 파싱하여 ParseResult 객체로 보관합니다.
        self.media_url = urlparse(settings.MEDIA_URL)

    def _should_handle(self, path):
        # 중요: self.base_url과 self.media_url은 urlparse 결과(ParseResult)인 namedtuple입니다.
        # str.startswith()에 namedtuple을 직접 전달하면 튜플 내의 빈 문자열('') 원소로 인해 
        # 모든 요청 경로(예: '/')가 매칭되는 버그가 생기므로, 반드시 .path 속성을 추출하여 비교해야 합니다.
        return (path.startswith(self.base_url.path) and not self.base_url.netloc) or \
               (path.startswith(self.media_url.path) and not self.media_url.netloc)

    def serve(self, request):
        # 미디어 파일 요청인 경우 미디어 루트에서 찾아 서빙
        if request.path.startswith(self.media_url.path):
            path = request.path[len(self.media_url.path):]
            return django_static_serve(request, path, document_root=settings.MEDIA_ROOT)
        # 정적 파일 요청인 경우 부모 클래스(StaticFilesHandler)의 서빙 로직 수행
        return super().serve(request)

# WSGI 애플리케이션 정의
application = StaticAndMediaFilesHandler(get_wsgi_application())

if __name__ == '__main__':
    # 윈도우 환경에서 로컬 테스트를 위해 루프백 주소(127.0.0.1)와 포트 8000번에 할당합니다.
    # 운영 환경의 동시성 대응을 위해 스레드 풀 개수를 4개로 지정합니다.
    print("Starting Waitress WSGI server on http://127.0.0.1:8000")
    serve(application, host='127.0.0.1', port=8000, threads=4)
