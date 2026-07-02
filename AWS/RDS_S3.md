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

DB_NAME=skn29-db
DB_USER=postgres
DB_PASSWORD=admin1234
DB_HOST=skn29-django-db.xxxxxx.ap-northeast-2.rds.amazonaws.com
# --> RDS->DB클릭->엔드포인트항목
```