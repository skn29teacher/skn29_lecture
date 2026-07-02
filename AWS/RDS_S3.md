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