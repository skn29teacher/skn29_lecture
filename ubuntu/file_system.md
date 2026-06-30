```
# 컨터이서 생성시 볼륨을 셋팅.. 일반생성후 볼륨연결 안됨
docker run -it --name django-dev -p 8000:8000 -v c:\DjangoProject:/workspace ubuntu bash

apt update

apt install python3 python3-pip -y

apt install python3-venv -y

cd workspace

python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate

pip install django

# django 프로젝트 생성
django-admin startproject config .

# database 생성
python3 manage.py migrate

# 관리자 계정 생성
python3 manage.py createsuperuser

# 개발서버 실행
python3 manage.py  runserver 0.0.0.0:8000
```