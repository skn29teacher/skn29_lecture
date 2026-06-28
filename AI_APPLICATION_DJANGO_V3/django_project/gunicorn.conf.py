import multiprocessing

bind = "unix:/tmp/gunicorn.sock"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
backlog = 2048
timeout = 30
accesslog = "-"
errorlog = "-"
loglevel = "info"
proc_name = "django_todoboard"
