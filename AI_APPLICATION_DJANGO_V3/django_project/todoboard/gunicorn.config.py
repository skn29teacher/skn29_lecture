import multiprocessing

# 바인딩 설정
# Nginx 와 IPC(Inter-Process Communication)통신을 수행할 unix 소켁 파일을 바인딩
bind = 'unix:/tmp/gunicorn.sock'

# cpu 코어수어 따른 워커 프로세스 개수 최적화
workers = multiprocessing.cpu_count() * 2 + 1

# 각 워커의 스레드 개수
threads = 2

# 대기 큐 크기(동시 요청이 가득 찼을 때 대기하는 요청 최대 개수)
backlog = 2048

# 단일요청당 타임아웃 제한 시간(초 단위)
timeout = 30

# 로그 설정
accesslog = "_"
errorlog = "_"
loglevel = "info"

# 시스템 프로세스 목록에 표시될 이름
proc_name = 'django_todoboard'