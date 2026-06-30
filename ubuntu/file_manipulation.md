# 에러 로그만 따로 수집하는 예시
python3 manage.py 2> error.log

# 정상 출력과 에러를 모두 같은 파일에 저장
python3 manage.py &> all_output.log

# 정상 출력은 파일로, 에러는 화면에 출력
python3 manage.py > output.log