# Docker 기본 명령어 및 컨테이너 관리 가이드

## 1. Docker 구조 이해

```
Docker Engine (Docker Desktop)
        │
        ├── Image (이미지)
        │      ├── ubuntu:22.04
        │      ├── python:3.12
        │      └── nginx
        │
        └── Container (컨테이너)
               ├── ubuntu2204
               ├── webserver
               └── mysql
```

- **Image** : 실행에 필요한 템플릿(설치 파일)
- **Container** : 이미지를 실행한 인스턴스

---

# 이미지(Image) 관리

## 이미지 다운로드

```bash
docker pull ubuntu:22.04
```

## 이미지 목록 확인

```bash
docker images
```

예시

```text
REPOSITORY   TAG      IMAGE ID       CREATED       SIZE
ubuntu       22.04    xxxxxxxxxxxx   2 weeks ago   77MB
```

## 이미지 삭제

```bash
docker rmi ubuntu:22.04
```

강제 삭제

```bash
docker rmi -f ubuntu:22.04
```

---

# 컨테이너(Container) 생성 및 실행

## 기본 실행

```bash
docker run -it ubuntu:22.04
```

옵션

| 옵션 | 설명 |
|-------|------|
| -i | 표준입력 유지 |
| -t | 가상 터미널 생성 |

---

## 이름을 지정하여 실행 (권장)

```bash
docker run -it --name ubuntu2204 ubuntu:22.04
```

---

## 백그라운드 실행

```bash
docker run -d --name ubuntu2204 ubuntu:22.04 sleep infinity
```

옵션

| 옵션 | 설명 |
|-------|------|
| -d | Detached(백그라운드) 실행 |

---

# 컨테이너 확인

## 실행 중인 컨테이너

```bash
docker ps
```

예시

```text
CONTAINER ID   IMAGE          STATUS
123456789abc   ubuntu:22.04   Up 3 minutes
```

---

## 전체 컨테이너 확인

```bash
docker ps -a
```

예시

```text
CONTAINER ID   STATUS
123456789abc   Exited (0)
```

---

# 컨테이너 시작

```bash
docker start ubuntu2204
```

---

# 컨테이너 종료

```bash
docker stop ubuntu2204
```

---

# 컨테이너 재시작

```bash
docker restart ubuntu2204
```

---

# 컨테이너 삭제

```bash
docker rm ubuntu2204
```

강제 삭제

```bash
docker rm -f ubuntu2204
```

---

# 컨테이너 이름 변경

```bash
docker rename ubuntu2204 myubuntu
```

---

# 컨테이너 접속

## 실행 중인 컨테이너 접속

```bash
docker exec -it ubuntu2204 bash
```

---

## 중지된 컨테이너 실행하면서 접속

```bash
docker start -ai ubuntu2204
```

---

# 컨테이너 내부 명령 실행

```bash
docker exec ubuntu2204 ls
```

```bash
docker exec ubuntu2204 pwd
```

```bash
docker exec ubuntu2204 whoami
```

---

# 컨테이너 로그 확인

```bash
docker logs ubuntu2204
```

실시간 로그

```bash
docker logs -f ubuntu2204
```

---

# 컨테이너 프로세스 확인

```bash
docker top ubuntu2204
```

---

# 리소스 사용량 확인

```bash
docker stats
```

---

# 컨테이너 상세 정보

```bash
docker inspect ubuntu2204
```

---

# 컨테이너 변경사항을 새로운 이미지로 저장

```bash
docker commit ubuntu2204 myubuntu:v1
```

확인

```bash
docker images
```

---

# 사용하지 않는 리소스 정리

중지된 컨테이너 삭제

```bash
docker container prune
```

사용하지 않는 이미지 삭제

```bash
docker image prune
```

전체 정리

```bash
docker system prune
```

모든 미사용 이미지까지 삭제

```bash
docker system prune -a
```

---

# 파일 전송

## 방법 1 : docker cp (가장 간단)

### Windows → Docker

```bash
docker cp C:\Users\Playdata\hello.txt ubuntu2204:/root/
```

---

### Docker → Windows

```bash
docker cp ubuntu2204:/root/hello.txt C:\Users\Playdata\
```

---

### 폴더 복사

Windows → Docker

```bash
docker cp C:\Project ubuntu2204:/root/
```

Docker → Windows

```bash
docker cp ubuntu2204:/root/Project C:\Backup\
```

---

# 방법 2 : Volume(바인드 마운트) 

Windows 폴더

```
C:\DockerShare
```

Docker 내부

```
/workspace
```

연결

```bash
docker run -it -v C:\DockerShare:/workspace ubuntu:22.04
```

컨테이너 내부

```bash
cd /workspace
```

이제

Windows에서

```
C:\DockerShare
```

에 파일을 생성하면

Docker에서도 즉시 보입니다.

Docker에서

```bash
echo hello > /workspace/test.txt
```

를 실행하면

Windows에도

```
C:\DockerShare\test.txt
```

가 즉시 생성됩니다.

실시간 동기화되므로 개발환경에서는 가장 많이 사용하는 방식입니다.

---