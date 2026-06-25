# collectstatic 정적 파일 배정 및 배포 준비

웹 서비스를 완성한 후 실제 프로덕션 서버(Nginx, Apache, AWS S3 등) 환경에 배포할 때, 템플릿 태그와 필터를 거친 HTML 코드 및 업로드된 미디어 파일과 여러 앱에 흩어져 있는 정적 파일(Static Files)을 체계적으로 조율하고 수집하여 배포를 완료하는 최적화 기법을 학습합니다.

---

## 1. 정적 파일 수집 체계와 STATIC_ROOT 설정

개발 단계에서는 장고의 가벼운 로컬 웹 서버가 각 앱 디렉토리 내의 `static/` 폴더를 실시간으로 탐색하여 정적 파일을 응답하지만, 운영 서버 배포 단계에서는 효율성과 보안을 위해 별도의 전용 웹 서버(예: Nginx)가 정적 파일 서빙을 직접 전담하는 것이 웹 표준 가이드라인입니다. 

이를 위해 여러 앱에 분산 적재되어 있는 정적 파일들을 단 하나의 전역 물리 폴더로 수집하여 몰아넣어야 합니다. 이 집적 디렉토리를 선언하는 설정 변수가 바로 **`STATIC_ROOT`**입니다.

### settings.py 설정
파일명: `todoboard/settings.py`
```python
# 1. 브라우저가 정적 파일에 접근하기 위해 요청할 URL 시작점
STATIC_URL = 'static/'

# 2. 개별 앱 내부가 아닌, 프로젝트 루트 단에서 수집할 공용 정적 디렉토리 경로 지정
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# 3. 배포용 정적 자원 수집 최종 물리 디렉토리 경로 정의 (기존 설정과 중복되지 않는 고유 명칭 부여 권장)
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

---

## 2. 정적 자원 집적 명령어 (collectstatic)

`STATIC_ROOT` 경로 설정이 완료되면, 터미널(CMD/Bash) 창에서 아래의 장고 관리 명령어를 수행합니다.
```bash
python manage.py collectstatic
```

### 명령어 작동 프로세스
1. **수집 범위 스캔**: 장고는 `INSTALLED_APPS`에 나열된 모든 기본 패키지(예: `django.contrib.admin` 등) 내부에 내장된 static 자원들과, `STATICFILES_DIRS`에 지정된 전역 static 자원들을 모조리 탐색합니다.
2. **복사 및 집적**: 스캔된 모든 스타일시트(CSS), 자바스크립트(JS), 기본 테마 이미지 파일들을 `STATIC_ROOT`에 정의된 `staticfiles/` 디렉토리 하위로 복사하여 일목요연하게 계층화합니다.
3. **최종 가동**: Nginx 등의 웹 서버에 해당 `staticfiles/` 경로를 지칭하여 외부 정적 서빙을 일임시키고, 장고 서버의 부하를 원천 격리시킵니다.

---

## 3. 미디어 파일(Media) 배포 시 유의사항

사용자가 올린 첨부 이미지 등의 미디어 파일은 `collectstatic` 명령어로 수집되지 않습니다. 
- **이유**: 정적 파일은 개발 시점에 결정되는 고정 자원이지만, 미디어 파일은 서비스 가동 도중 사용자에 의해 동적으로 생성되고 적재되는 휘발성 자원이기 때문입니다.
- **배포 대책**: 실무 운영 환경에서는 `MEDIA_ROOT` 경로를 Nginx의 파일 매핑 디렉토리와 연동하거나, 영구 보존성과 가용성을 위해 AWS S3(Simple Storage Service) 같은 외부 전용 오브젝트 스토리지에 API로 저장되도록 연동 설정을 별도 추가하여 대비해야 합니다.

---

## 4. 최종 통합 검증 절차

본 과정을 완성한 이후, 전체 시스템의 작동 무결성을 다음과 같이 검증합니다.

1. **데이터베이스 이력 수립 및 마이그레이션**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
2. **최고 관리자 계정 개설**:
   ```bash
   python manage.py createsuperuser
   ```
3. **정적 파일 수집 가동**:
   ```bash
   python manage.py collectstatic --noinput
   ```
4. **웹 서버 기동 및 비동기 동작 검사**:
   ```bash
   python manage.py runserver
   ```
   - 브라우저로 `http://127.0.0.1:8000/spa/` 에 접속하여 아바타 배지가 네비게이션 헤더에 올바르게 노출되는지 확인합니다.
   - 이미지를 첨부하여 새 할 일을 추가하고, 새로고침 없이 즉각 비동기로 카드가 생성되며 상단 대시보드의 달성률 수치가 연동 갱신되는지 최종 확인하여 검증을 완결합니다.
