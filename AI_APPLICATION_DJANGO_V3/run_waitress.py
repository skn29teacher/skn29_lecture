from waitress import serve
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.views.static import serve as django_static_serve
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todoboard.settings.local')

# Waitress 단독 구성시 정적(static)파일과 미디어(Media) 파일을 모두 서빙 핸들러
class StaticAndMeidaFilesHandler(StaticFilesHandler):
    def __init__(self, application):
        super().__init__(application)
        self.media_url = settings.MEDIA_URL
    def _should_handle(self, path):
        # 요청경로가 static_url 또는 media_url로 시작하는지 검사
        return path.startswith(self.base_url) or path.statswith(self.media_url)
    def serve(self, request):
        # 미디어 파일 요청인경우 미디어 루트에서 찾아 서비
        if request.path.startswith(self.media_url):
            path = request.path[len(self.media_url) : ]
            return django_static_serve(request,path,document_root=settings.MEDIA_ROOT)
        # 정적파일인 경우 부모클래스의 서빙로직
        return super().serve(request)
# wsgi 어플리케이션 정의
application = StaticAndMeidaFilesHandler(get_wsgi_application())
if __name__ == '__main__':
    # 윈도우 환경에서 로컬테스트를 위해서 루프백주소(127.0.0.1)와 포트 8000번에 할당
    # 운영환경의 동시성 대응을위해서 스레드 풀 개수를 4개로 지정
    print('Starting Waitress WSGI sever on http://127.0.0.1:8000')
    serve(application, host='127.0.0.1', port=8000, threads=4)