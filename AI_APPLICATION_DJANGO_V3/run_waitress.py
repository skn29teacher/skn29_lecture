from waitress import serve
from todoboard.wsgi import application

if __name__ == '__main__':
    # 윈도우 환경에서 로컬테스트를 위해서 루프백주소(127.0.0.1)와 포트 8000번에 할당
    # 운영환경의 동시성 대응을위해서 스레드 풀 개수를 4개로 지정
    print('Starting Waitress WSGI sever on http://127.0.0.1:8000')
    serve(application, host='127.0.0.1', port=8000, threads=4)