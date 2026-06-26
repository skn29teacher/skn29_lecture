# 개발과 운영환경에서 공통으로 사용하는 설정
import environ
from pathlib import Path

# settings/base.py 위치에서 3단계 상위로 이동 프로젝트 루트경로
BASE_DIR = Path(__file__).resolve().parent.parent.parent