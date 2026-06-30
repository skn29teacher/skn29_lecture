```
docker run -it --name django-dev -p 8000:8000 -v c:\DjangoProject:/workspace ubuntu bash

apt update

apt install python3 python3-pip -y

apt install python3-venv -y

cd workspace

python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate

pip install django
```