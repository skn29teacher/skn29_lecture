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

# ec2 인스턴트 클릭
1. 오른쪽 상단에 IAM역활 수정 - 만든 IAM을 선택하고 - 업데이트

# ec2, s3 연동테스트
pip install boto3
```iam_test.py
import boto3
s3 = boto3.client('s3')
response = s3.list_buckets()
for bocket in response['Buckets']:
    print(bucket['Name'])
```

# Django s3패키지 설치  통신을 위해서
pip install django-storages

config/settings.py 수정
```
INSTALLED_APPS = [
    # ... 기존 앱 ...
    'storages',
]

# S3 버킷 정보 설정 (IAM 역할로 인증하므로 AWS_ACCESS_KEY_ID 등은 필요 없습니다)
AWS_STORAGE_BUCKET_NAME = 'skn29-static-<내 고유값>'
AWS_S3_REGION_NAME = 'ap-northeast-2'

# Django 4.2+ 권장 STORAGES 설정 방식
STORAGES = {
    # 미디어 파일 (업로드 이미지 등) 백엔드 설정
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    # 정적 파일 (css, js 등) 백엔드 설정
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
}
```
# 정적파일 수집 및 동기화
python manage.py collectstatic --noinput

# 의존성 패키지 생성 및 업데이트
pip freeze > requirements.txt

# 탄력적ip(Elastic IP) 할당
- 주의사항 EC2하고 연결된 상태에서는 무료 하지만. 연결하지않으면 또는 방치하면 시간 당 과금됨
- ec2-네트웍 및 보안(왼쪽메뉴) - 탄력적ip - 할당
- 생성된 ip클릭 - 작업- 탄력적ip주소연결
- 인스턴스선택- skn29-server -연결