# 4차시: 파일 조작 및 텍스트 리다이렉션

## 1. 학습 목표
* 터미널 내에서 파일을 신규 생성하고 텍스트를 입력하는 기법을 실습합니다.
* 리다이렉션(`>`, `>>`) 문법을 이용하여 파일에 텍스트 데이터를 추가하고 파일을 복사, 이동, 삭제합니다.
* 실무에서 자주 마주치는 파일 탐색, 내용 확인, 텍스트 편집 방법을 익힙니다.

---

## 2. 관련 이론

### 2-1. 표준 입출력 스트림 (Standard Streams)
리눅스의 모든 프로세스는 기본적으로 3가지 입출력 채널을 가집니다.

| 스트림 | 번호 | 설명 | 기본 연결 장치 |
|--------|------|------|----------------|
| 표준 입력 (stdin) | 0 | 데이터를 읽어오는 채널 | 키보드 |
| 표준 출력 (stdout) | 1 | 정상 결과를 출력하는 채널 | 터미널 화면 |
| 표준 에러 (stderr) | 2 | 에러 메시지를 출력하는 채널 | 터미널 화면 |

리다이렉션은 이 채널들의 연결 대상을 **파일**로 바꿔주는 기능입니다.

### 2-2. 리다이렉션 종류

| 기호 | 이름 | 동작 | 주의사항 |
|------|------|------|----------|
| `>` | 출력 리다이렉션 | 파일을 새로 만들거나 기존 내용을 **덮어씀** | 기존 파일 내용이 즉시 삭제됨 |
| `>>` | 추가 리다이렉션 | 파일 끝에 내용을 **덧붙임** | 파일이 없으면 새로 생성 |
| `2>` | 에러 리다이렉션 | stderr(에러 메시지)를 파일로 저장 | 에러 로그 수집 시 사용 |
| `2>>` | 에러 추가 리다이렉션 | 에러 메시지를 파일 끝에 계속 추가 | 운영 에러 누적 로그 시 사용 |
| `&>` | 전체 리다이렉션 | stdout과 stderr를 동시에 같은 파일로 저장 | 모든 출력을 한 파일에 통합 |

```bash
# 에러 로그만 따로 수집하는 예시
python3 app.py 2> error.log

# 정상 출력과 에러를 모두 같은 파일에 저장
python3 app.py &> all_output.log

# 정상 출력은 파일로, 에러는 화면에 출력
python3 app.py > output.log
```

### 2-3. 파일 생성 방법 3가지
리눅스에서 빈 파일 또는 텍스트가 담긴 파일을 만드는 방법은 여러 가지입니다.

```bash
# 방법 1: touch - 빈 파일 생성 (또는 타임스탬프 갱신)
touch app.log

# 방법 2: echo + 리다이렉션 - 내용이 있는 파일 즉시 생성
echo "초기 설정값" > config.txt

# 방법 3: cat + 리다이렉션 (heredoc 방식) - 여러 줄 입력 후 Ctrl+D로 저장
cat > memo.txt
첫 번째 줄
두 번째 줄
(Ctrl + D 를 눌러 저장)
```

### 2-4. 파일 내용 확인 명령어 비교

| 명령어 | 특징 | 적합한 상황 |
|--------|------|-------------|
| `cat` | 파일 전체 내용을 한 번에 출력 | 짧은 설정 파일, 간단한 로그 확인 |
| `head -n N` | 파일 앞 N줄만 출력 (기본 10줄) | 로그 파일의 시작부 확인 |
| `tail -n N` | 파일 끝 N줄만 출력 (기본 10줄) | 최신 로그, 가장 최근 이벤트 확인 |
| `less` | 페이지 단위 스크롤 뷰어 | 수천 줄 이상의 대용량 파일 탐색 |
| `wc -l` | 파일의 전체 줄 수 카운트 | 로그 건수, 데이터 행 수 파악 |

```bash
# 앞 20줄 확인
head -n 20 server.log

# 마지막 50줄 확인
tail -n 50 server.log

# 파일 줄 수 세기
wc -l server.log

# less로 대용량 파일 탐색 (q로 종료, /검색어 로 검색)
less /var/log/syslog
```

### 2-5. cp / mv / rm 심화

**cp (복사)**
```bash
# 기본 복사
cp 원본파일 대상파일

# 디렉토리 전체 복사 (-r: recursive)
cp -r /app/config /app/config_backup

# 메타데이터(권한, 타임스탬프) 보존하며 복사 (-p)
cp -p deploy.sh deploy.sh.bak

# 덮어쓰기 전 확인 프롬프트 (-i: interactive)
cp -i new_config.txt /etc/myapp/config.txt
```

**mv (이동/이름 변경)**
```bash
# 파일 이름 변경
mv old_name.txt new_name.txt

# 파일을 다른 디렉토리로 이동
mv app.log /var/log/myapp/

# 여러 파일을 한 디렉토리로 이동
mv file1.txt file2.txt file3.txt /backup/
```

**rm (삭제)**
```bash
# 파일 삭제
rm 파일명

# 삭제 전 확인 (-i)
rm -i 중요파일.txt

# 디렉토리와 하위 파일 전체 강제 삭제 (-rf)
rm -rf /tmp/test_build

# 주의: 아래 명령어는 절대 실행하지 말 것!
# rm -rf /   (루트 전체 삭제 - 시스템 파괴)
# rm -rf /*  (동일하게 위험)
```

> **실무 팁**: 운영 서버에서 `rm -rf`를 실행할 때는 경로를 변수에 담고 `echo`로 먼저 확인한 뒤 실행하는 습관을 들이세요.
> ```bash
> TARGET="/tmp/old_logs"
> echo "삭제 대상: $TARGET"   # 경로 확인 후
> rm -rf "$TARGET"           # 실행
> ```

### 2-6. 파일/디렉토리 탐색 명령어

```bash
# 현재 위치 확인
pwd

# 디렉토리 이동
cd /var/log          # 절대 경로 이동
cd ../config         # 상대 경로 이동
cd ~                 # 홈 디렉토리로 이동
cd -                 # 이전 위치로 돌아가기

# 파일 목록 확인
ls -al               # 숨김 파일 포함 상세 목록
ls -lh               # 파일 크기를 사람이 읽기 쉬운 단위로 출력
ls -lt               # 수정 시간 기준 내림차순 정렬

# 특정 이름 패턴의 파일 찾기
find /var/log -name "*.log"             # 확장자로 탐색
find /app -name "config*" -type f       # 파일만 탐색
find /tmp -mtime +7                     # 7일 이상 지난 파일 탐색
find / -size +100M                      # 100MB 초과 파일 탐색
```

---

## 3. 실습 단계 및 명령어

### 실습 1: 빈 파일 생성 및 초기 내용 기입
```bash
cd /root/workspace
touch server_test.txt
echo "Server Started" > server_test.txt
cat server_test.txt
```

### 실습 2: 파일 덧붙이기와 덮어쓰기 차이 확인
```bash
# 내용 덧붙이기 (>>) - 기존 내용 유지
echo "Connection Open" >> server_test.txt
echo "User Login: admin" >> server_test.txt
cat server_test.txt
# 출력 예시:
# Server Started
# Connection Open
# User Login: admin

# 내용 덮어쓰기 (>) - 기존 내용 전부 삭제 후 새로 작성
echo "Database Disconnected" > server_test.txt
cat server_test.txt
# 출력 예시:
# Database Disconnected  (이전 내용은 모두 사라짐)
```

### 실습 3: 에러 로그 분리 수집
```bash
# 존재하지 않는 파일을 cat 하면 에러 발생
cat /nonexistent_file 2> error.log

# 에러 메시지가 화면 대신 파일에 저장됨
cat error.log
```

### 실습 4: 파일 내용 확인 도구 비교 실습
```bash
# 여러 줄 로그 데이터 생성
for i in $(seq 1 30); do echo "Line $i: Event occurred"; done > sample.log

# 전체 출력
cat sample.log

# 앞 5줄
head -n 5 sample.log

# 마지막 5줄
tail -n 5 sample.log

# 전체 줄 수 확인
wc -l sample.log
```

### 실습 5: 파일 복사 및 백업
```bash
# 중요 파일 백업 (확장자에 .bak 추가)
cp server_test.txt server_test.txt.bak

# 백업 디렉토리 생성 및 이동
mkdir -p backup_storage/2024
mv server_test.txt.bak backup_storage/2024/
ls -l backup_storage/2024/
```

### 실습 6: find로 파일 탐색
```bash
# 현재 디렉토리에서 .txt 파일 전체 탐색
find /root/workspace -name "*.txt"

# 최근 10분 내에 수정된 파일 탐색
find /root/workspace -mmin -10
```

### 실습 7: 강제 삭제
```bash
rm server_test.txt
rm -rf backup_storage
```

---

## 4. 자주 겪는 실수와 주의사항

| 실수 유형 | 발생 상황 | 예방법 |
|-----------|-----------|--------|
| `>` 로 덮어써 버림 | `>>` 대신 `>` 입력 | 중요 파일은 먼저 `cp`로 백업 |
| `rm -rf` 잘못된 경로 | 변수 오타, 공백 경로 | 삭제 전 `echo $TARGET` 으로 경로 확인 |
| 루트 권한으로 cp 없이 편집 | 원본 파일 직접 수정 | 항상 `.bak` 백업 후 수정 |
| find 결과 없음 | 경로 오타, 권한 부족 | `-maxdepth` 옵션으로 탐색 범위 조절 |

---

## 5. 서버 운영 관점의 실전 시나리오

### 시나리오 A: 웹서버 점검 모드 전환
배포 도중 사이트를 임시 점검 페이지로 전환해야 할 때:
```bash
# 1. 현재 index.html 백업
cp /var/www/html/index.html /var/www/html/index.html.bak

# 2. 점검 안내 페이지로 교체
echo "<h1>서비스 점검 중입니다. 잠시 후 다시 접속해 주세요.</h1>" > /var/www/html/index.html

# 3. 점검 완료 후 원본 복원
cp /var/www/html/index.html.bak /var/www/html/index.html
```

### 시나리오 B: 설정 파일 변경 이력 관리
```bash
# 날짜를 파일명에 포함해 백업
DATE=$(date +%Y%m%d_%H%M%S)
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.$DATE.bak

# 백업 목록 확인
ls -lt /etc/nginx/*.bak
```

### 시나리오 C: 오래된 임시 파일 일괄 정리
```bash
# 7일 이상 지난 임시 파일 탐색 후 확인
find /tmp -mtime +7 -type f

# 확인 후 삭제
find /tmp -mtime +7 -type f -delete
```
