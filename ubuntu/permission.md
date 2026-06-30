# 5차시: 파일 권한(Permission) 체계 및 제어

## 1. 학습 목표
* 리눅스의 핵심 보안 체계인 읽기, 쓰기, 실행 권한 분류를 파악합니다.
* `chmod` 명령어를 활용하여 기호와 8진수 숫자로 권한 속성을 변경합니다.
* `chown`으로 파일 소유자와 그룹을 변경하는 방법을 익힙니다.
* 실무에서 자주 마주치는 `Permission denied` 오류를 스스로 해결할 수 있습니다.

---

## 2. 관련 이론

### 2-1. 리눅스 소유권 구조

리눅스 상의 모든 파일과 디렉토리는 세 가지 대상에 대한 권한을 독립적으로 관리합니다.

| 대상 | 기호 | 설명 |
|------|------|------|
| 소유자 | `u` (user) | 파일을 생성하거나 권한을 받은 계정 |
| 그룹 | `g` (group) | 소유자가 속한 팀/부서 단위의 계정 묶음 |
| 기타 사용자 | `o` (others) | 위 둘을 제외한 시스템의 모든 계정 |
| 전체 | `a` (all) | u + g + o 전체 |

### 2-2. 권한의 종류

| 권한 | 기호 | 숫자값 | 파일에서 | 디렉토리에서 |
|------|------|--------|--------|-------------|
| 읽기 | `r` | 4 | 파일 내용 확인 가능 | 목록 조회(`ls`) 가능 |
| 쓰기 | `w` | 2 | 파일 내용 수정/삭제 가능 | 하위 파일 생성/삭제 가능 |
| 실행 | `x` | 1 | 스크립트/프로그램 실행 가능 | `cd` 로 진입 가능 |
| 없음 | `-` | 0 | 해당 권한 보유하지 않음 | 해당 권한 보유하지 않음 |

### 2-3. 권한 표시 형식 해석

`ls -l` 명령어 실행 시 나타나는 권한 표시를 읽는 방법입니다:

```
-rwxr-xr-x  1  root  root  1234  Jun 10 10:00  deploy.sh
↑       ↑：↔↑：↔↑：↔
파일종류  소유자  그룹   기타
```

| 위치 | 문자 | 의미 |
|------|------|------|
| 1번째 | `-` 또는 `d` | `-`: 일반 파일, `d`: 디렉토리, `l`: 심볼릭링크 |
| 2~4번째 | `rwx` | 소유자 권한 |
| 5~7번째 | `r-x` | 그룹 권한 |
| 8~10번째 | `r-x` | 기타 사용자 권한 |

**실예 해석**:
```
rwxr-xr-x = 소유자(7) 그룹(5) 기타(5) = 755
rw-r--r-- = 소유자(6) 그룹(4) 기타(4) = 644
rwx------ = 소유자(7) 그룹(0) 기타(0) = 700
```

### 2-4. 실무에서 자주 쓰는 권한 조합

| 권한 값 | 의미 | 사용 상황 |
|---------|------|----------|
| `755` | 소유자 rwx, 그룹/기타 r-x | 웹 서버 실행 파일, 배포 스크립트 |
| `644` | 소유자 rw-, 그룹/기타 r-- | 일반 설정 파일, HTML/CSS/JS 정적 파일 |
| `600` | 소유자 rw-, 그룹/기타 없음 | SSH 인증키, 비밀키 파일 |
| `700` | 소유자 rwx, 그룹/기타 없음 | 개인 실행 스크립트, 제어용 도구 |
| `777` | 모두 rwx | 임시 디렉토리 (가장 위험, 실무에서 거의 사용 안 함) |
| `444` | 모두 r-- | 읽기 전용 문서, 템플릿 파일 |

> **주의**: `chmod 777`은 보안상 매우 위험합니다. 운영 서버에서 `777`을 설정하면 누구든 파일을 수정하거나 실행할 수 있게 됩니다.

### 2-5. chown - 소유자 변경

```bash
# 소유자 변경
chown 새소유자 파일명

# 소유자와 그룹 함께 변경
chown 사용자:그룹 파일명

# 디렉토리 전체 재귀적 변경 (-R)
chown -R www-data:www-data /var/www/html
```

실무 예시:
```bash
# nginx가 /var/www/html 디렉토리를 읽어야 하는데 권한이 없을 때
ls -l /var/www/html
# drwxr-xr-x root root  <- nginx(www-data 계정)는 진입 불가
chown -R www-data:www-data /var/www/html
```

---

## 3. 실습 단계 및 명령어

### 실습 1: 실습 파일 생성 및 기본 권한 조회
```bash
cd /root/workspace
touch run_server.sh
ls -l run_server.sh
# -rw-r--r-- 1 root root 0 Jun 10 10:00 run_server.sh
# └ 기본적으로 644 권한 (rw-r--r--)으로 생성됨
```

### 실습 2: 기호 표기법으로 권한 변경
```bash
# 소유자에게 실행 권한 추가
chmod u+x run_server.sh
ls -l run_server.sh
# -rwxr--r-- 가 됨

# 기타 사용자의 읽기/쓰기 권한 제거
chmod o-rw run_server.sh
ls -l run_server.sh
# -rwxr----- 가 됨

# 그룹에게 쓰기 권한 추가
chmod g+w run_server.sh
ls -l run_server.sh
# -rwxrw---- 가 됨
```

### 실습 3: 숫자 표기법으로 전체 권한 강제 설정
```bash
# 읽기 전용 (모두 r--)
chmod 444 run_server.sh
ls -l run_server.sh
# -r--r--r--

# 표준 웹 파일 권한 (rw-r--r--)
chmod 644 run_server.sh

# 실행 스크립트 표준 권한 (rwxr-xr-x)
chmod 755 run_server.sh
ls -l run_server.sh
# -rwxr-xr-x

# SSH 인증키와 같은 민감한 파일 (rw-------)
chmod 600 secret.key
```

### 실습 4: 실행 권한 없을 때 오류 확인 및 해결
```bash
# 실행 권한 없는 파일 실행 시도
chmod 644 run_server.sh   # 실행 권한 제거
./run_server.sh
# bash: ./run_server.sh: Permission denied   <- 이런 오류가 나타남!

# 해결
chmod +x run_server.sh
./run_server.sh  # 정상 실행
```

### 실습 5: 디렉토리 권한 확인
```bash
mkdir mydir
ls -ld mydir   # 디렉토리 자체 권한 확인 (-d 옵션)
# drwxr-xr-x

# 실행(x) 권한 없으면 cd 자체가 안 됨
chmod 644 mydir
cd mydir
# bash: cd: mydir: Permission denied

# 원복
chmod 755 mydir
```

---

## 4. 일반적인 오류와 해결 패턴

| 오류 메시지 | 원인 | 해결법 |
|------------|------|--------|
| `Permission denied` 실행 시 | 실행 권한 없음 | `chmod +x 파일명` |
| `Permission denied` 파일 수정 시 | 쓰기 권한 없음 | `chmod u+w 파일명` |
| `Permission denied` 디렉토리 진입 시 | 실행(x) 권한 없음 | `chmod u+x 디렉토리` |
| nginx/apache가 파일을 못 읽음 | 서버 프로세스 계정은 다른 사용자 | `chown -R www-data:www-data /var/www/html` |
| 로그 파일에 쓰지 못함 | 로그 디렉토리 쓰기 권한 없음 | `chmod 755 /var/log/myapp` |

---

## 5. 서버 운영 관점의 실전 시나리오

### 시나리오 A: 배포 스크립트 실행 오류 해결
```bash
# 파일 업로드 후 실행 시도
./deploy.sh
# -bash: ./deploy.sh: Permission denied

# 현재 권한 확인
ls -l deploy.sh
# -rw-r--r-- root root  <- 실행 권한(x) 없음

# 해결
chmod +x deploy.sh
./deploy.sh   # 정상 실행
```

### 시나리오 B: 웹 서버 정적 파일 권한 설정
```bash
# 웹 루트 디렉토리 소유자를 nginx 서비스 계정으로 변경
chown -R www-data:www-data /var/www/html

# HTML/CSS/JS 정적 파일: 읽기 가능, 쓰기 불가 (644)
find /var/www/html -type f -exec chmod 644 {} \;

# 디렉토리: 진입/목록 확인 가능, 쓰기 불가 (755)
find /var/www/html -type d -exec chmod 755 {} \;
```

### 시나리오 C: SSH 인증키 권한 문제
```bash
# SSH 접속 시 인증키 권한이 너무 넓으면 거절됨
# WARNING: UNPROTECTED PRIVATE KEY FILE!
# Permissions 0644 for 'id_rsa' are too open.

# 해결: 소유자만 읽기/쓰기 가능
chmod 600 ~/.ssh/id_rsa
chmod 700 ~/.ssh/
```
