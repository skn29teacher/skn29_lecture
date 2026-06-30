# 3차시: 파일 시스템 구조 이해 및 탐색

## 1. 학습 목표
* 리눅스의 대표적인 디렉토리 구조와 계층별 역할을 인지합니다.
* 디렉토리 내부를 탐색하고 이동하며 특정 디렉토리를 생성, 삭제하는 기본 명령어를 습득합니다.

## 2. 관련 이론
* **리눅스 디렉토리 계층 구조**: 리눅스는 모든 디바이스와 설정을 하나의 루트 파일 시스템(`/`) 트리 구조 아래에 두는 규칙을 가지고 있습니다.
  * `/bin`: 가장 기본적인 리눅스 핵심 실행 파일들이 위치합니다.
  * `/etc`: 시스템 부팅 및 개별 서버 프로그램들의 설정 텍스트 파일들이 보관됩니다.
  * `/home`: 루트가 아닌 일반 사용자들의 개별 개인 홈 폴더입니다.
  * `/var`: 실행 상태에서 실시간으로 변하는 시스템 정보 및 서버 에러 로그 파일들이 적재됩니다.

## 3. 실습 단계 및 명령어
1. **최상위 루트 디렉토리 이동 및 구조 확인**:
   ```bash
   cd /
   pwd
   ls -la
   ```
2. **상대 경로와 절대 경로 탐색**:
   * 절대 경로 이동: 루트 기준 고정 이동
     ```bash
     cd /etc
     ```
   * 상대 경로 이동: 현재 자신의 물리 위치 기준 한 단계 위로 이동
     ```bash
     cd ..
     ```
3. **신규 전용 디렉토리 생성 및 삭제**:
   * 새로운 실습 폴더 생성:
     ```bash
     mkdir /root/workspace
     cd /root/workspace
     ```
   * 빈 디렉토리 삭제 (`rmdir`은 내부에 파일이 존재하면 경고를 뱉고 지워지지 않습니다):
     ```bash
     mkdir temp_folder
     rmdir temp_folder
     ```

## 4. 서버 운영 관점의 사용 시점 예시
* **서버 진단 시 기본 환경 확인**: 백엔드 서버에서 데이터베이스 연동 에러가 발생할 때, 데이터베이스 드라이버 설정이 있는 디렉토리(`/etc/app-config/`)로 신속하게 경로를 이동(`cd`)하여 설정 파일의 누락 여부를 확인하는 과정에 쓰입니다.


# Docker 컨테이너에서 Django 프로젝트 생성 후 Windows 브라우저에서 접속하기

> 목표
>
> Docker Ubuntu 컨테이너에서 Django 프로젝트를 생성하고,
> Windows 브라우저(http://localhost:8000)에서 접속하는 가장 간단한 예제

---

# 1. 프로젝트를 저장할 Windows 폴더 생성

예제

```
C:\
└── DjangoProject
```

PowerShell

```powershell
mkdir C:\DjangoProject
```

---

# 2. Ubuntu 컨테이너 실행 (Volume 연결)

```bash
docker run -it ^
--name django-dev ^
-p 8000:8000 ^
-v C:\DjangoProject:/workspace ^
ubuntu:22.04
```

PowerShell에서 한 줄로 입력

```bash
docker run -it --name django-dev -p 8000:8000 -v C:\DjangoProject:/workspace ubuntu:22.04
```

옵션 설명

| 옵션 | 설명 |
|-------|------|
| -it | 터미널 실행 |
| --name | 컨테이너 이름 |
| -p 8000:8000 | Windows와 Docker 포트 연결 |
| -v | Windows 폴더와 Docker 폴더 연결 |

---

# 3. Ubuntu 패키지 업데이트

```bash
apt update
```

---

# 4. Python 설치

Ubuntu 이미지에는 Python이 없는 경우가 있으므로 설치합니다.

```bash
apt install python3 python3-pip -y
```

확인

```bash
python3 --version
```

예시

```
Python 3.10.x
```

---

# 5. Django 설치

```bash
pip3 install django
```

확인

```bash
django-admin --version
```

---

# 6. 작업 폴더 이동

```bash
cd /workspace
```

현재 위치 확인

```bash
pwd
```

출력

```
/workspace
```

---

# 7. Django 프로젝트 생성

```bash
django-admin startproject config .
```

생성 결과

```
workspace
│
├── manage.py
└── config
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

---

# 8. 데이터베이스 생성

```bash
python3 manage.py migrate
```

출력 예시

```
Applying auth...
Applying admin...
OK
```

---

# 9. 관리자 계정 생성

```bash
python3 manage.py createsuperuser
```

예시

```
Username : admin

Email :

Password :

Password (again) :
```

---

# 10. 개발 서버 실행

기본 실행

```bash
python3 manage.py runserver
```

하지만 Docker에서는 접속되지 않습니다.

반드시

```bash
python3 manage.py runserver 0.0.0.0:8000
```

로 실행해야 합니다.

이유

```
127.0.0.1

↓

컨테이너 내부에서만 접속 가능
```

```
0.0.0.0

↓

외부(Windows)에서도 접속 가능
```

---

# 11. Windows 브라우저 접속

브라우저

```
http://localhost:8000
```

또는

```
http://127.0.0.1:8000
```

Django 시작 화면이 나타나면 성공입니다.

---

# 12. 관리자 페이지

```
http://localhost:8000/admin
```

로그인

```
아이디
↓

admin

비밀번호
↓

생성한 비밀번호
```

---

# 13. Windows에서 프로젝트 확인

Windows

```
C:\DjangoProject
```

Docker

```
/workspace
```

는 실시간 동기화됩니다.

Windows에서

```
settings.py
```

를 수정하면

Docker에서도 즉시 반영됩니다.

---

# 14. 서버 종료

컨테이너 안에서

```
Ctrl + C
```

---

# 15. 컨테이너 종료

```
exit
```

또는

```bash
docker stop django-dev
```

---

# 16. 다시 실행

```bash
docker start django-dev
```

---

# 17. 다시 접속

```bash
docker exec -it django-dev bash
```

작업 폴더

```bash
cd /workspace
```

서버 실행

```bash
python3 manage.py runserver 0.0.0.0:8000
```

---

# 프로젝트 구조

```
Windows

C:\DjangoProject
        │
        │ Volume
        ▼
Docker Ubuntu

/workspace
        │
        ├── manage.py
        ├── db.sqlite3
        └── config
```

---

# 전체 명령어 순서

```bash
docker run -it --name django-dev -p 8000:8000 -v C:\DjangoProject:/workspace ubuntu:22.04

apt update

apt install python3 python3-pip -y

pip3 install django

cd /workspace

django-admin startproject config .

python3 manage.py migrate

python3 manage.py createsuperuser

python3 manage.py runserver 0.0.0.0:8000
```

---

# 브라우저 접속

메인 페이지

```
http://localhost:8000
```

관리자 페이지

```
http://localhost:8000/admin
```

---

# 개발 시 자주 사용하는 명령

```bash
docker start django-dev

docker exec -it django-dev bash

cd /workspace

python3 manage.py runserver 0.0.0.0:8000

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py createsuperuser
```

---

# 참고 사항

이 예제는 Docker 학습을 위한 가장 단순한 개발 환경입니다.

실무에서는 일반적으로 다음과 같은 구성을 사용합니다.

- Python 공식 이미지(`python:3.12-slim`) 기반 컨테이너
- `requirements.txt`로 패키지 관리
- `Dockerfile`을 사용한 이미지 빌드
- `docker compose`를 이용한 Django + PostgreSQL + Redis 등의 멀티 컨테이너 구성
- 개발 서버 대신 Gunicorn과 Nginx를 사용한 운영 환경 구성



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