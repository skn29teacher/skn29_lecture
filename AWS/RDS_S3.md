# RDS 생성
1. 콘솔에서 RDS 검색 - Aurora and RDS
2. 전체 구성으로 생성 - 엔진은 PostgreSQL
3. 템플릿 - 프리티어
4. DB 인스턴스 식별자 - skn29-db2
5. 마스터 암호 생성 = admin1234
6. 기존 VPC 보안 그룹 - default 해제하고 ec2에서 설정한 보안그룹 skn29-sg 선택
7. 맨 아래 추가 구성 - 초기 데이터베이스 이름 - skn29db  (주의! 데이터베이스 이름에 하이픈을 인식 못할 가능성 있음)

# RDS 보안그룹에 EC2 접근 허용
1. EC2 콘솔에접속 - 보안그룹 - 인바운드 규칙 편집 - 규칙추가
 - 유형 PostgreSQL
 - 소스:검색버튼- EC2용 보안그룹 skn29-sg 클릭 후 저장

# 연결테스트
```
sudo apt install -y postgresql-client
psql -h <RDS엔트포인트> -U postgres -d skn29db
```

# 엔드포인트 확인
생성된 RDS 클릭하면 다음과 같은 화면이 보임 - "skn29-db2.cnwkm602y18u.ap-northeast-2.rds.amazonaws.com"
```
연결 단계
아래 단계에 따라 도구에 각 단계의 코드를 붙여넣고 명령을 실행하세요. 스니펫은 인증 구성을 동적으로 반영합니다.
curl -o global-bundle.pem https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem

export RDSHOST="skn29-db2.cnwkm602y18u.ap-northeast-2.rds.amazonaws.com" 
psql "host=$RDSHOST port=5432 dbname=skn29db user=postgres sslmode=verify-full sslrootcert=./global-bundle.pem"
```


# Django RDS 연결
```
cd ~/myproject
source venv/bin/activate

# 드라이버 설치 및 패키지
pip install psycopg2-binary python-dotenv
```

config/settings.py 수정
```
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),   # RDS 엔드포인트
        'PORT': '5432',
    }
}
```

.env 생성
```
vim ~/myproject/.env

DB_NAME=skn29db
DB_USER=postgres
DB_PASSWORD=admin1234
DB_HOST=skn29-django-db.xxxxxx.ap-northeast-2.rds.amazonaws.com
# --> RDS->DB클릭->엔드포인트항목
```

# gitignore 설정
echo ".env" >> ~/myproject/.gitignore

# 마이그레이션 수행
```
python manage.py migrate
# Django 서비스 재시작
sudo systemctl restart gunicorn

# DB 접속
psql -h <RDS엔드포인트> -U postgres -d <내DB이름>
# 테이블 목록 조회
\dt

# 특정 테이블 조회
select * from <테이블명>;
```

# DBeaver 등 외부 tool 연결
- host : 엔드포인트
- ssh탭을 클릭해서 pem 파일 연결  -모바텀x 연결과정과 비슷

# S3 버킷생성
 - 이름만 고유하게 작성하고 생성

 # EC2에 S3 접근용 IAM 역활 연결
 1. IAM 검색 및 이동 - 왼쪽 역확(Role) - 역활 만들기
 2. 서비스  : EC2선택 - 권한 정책추가:AmazonS3FullAccess
 3. 역활이름 : skn29-ec2-s3-role - 생성
 
