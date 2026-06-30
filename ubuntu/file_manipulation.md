# 에러 로그만 따로 수집하는 예시
python3 manage.py 2> error.log

# 정상 출력과 에러를 모두 같은 파일에 저장
python3 manage.py &> all_output.log

# 정상 출력은 파일로, 에러는 화면에 출력
python3 manage.py > output.log

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