# 3차시: HTTP 요청 구조 분석 - POST 메서드와 리퀘스트 바디

## 1. HTTP 요청 바디 (Request Body)
클라이언트가 서버로 대용량 데이터나 구조화된 객체를 보낼 때, URL에 노출하지 않고 안전하게 데이터를 전달하기 위해 HTTP 요청 패킷의 **바디(Body)** 영역에 데이터를 담아 보냅니다.

## 2. HTTP POST 메서드와 핵심 요청 헤더
- **POST 메서드**: 새로운 자원을 생성하거나, 폼 양식 제출, 대량의 데이터 가공 처리를 서버에 요청할 때 사용합니다.
- **Content-Type**: 요청 바디에 동봉된 데이터가 어떤 형식(Format)인지 서버에 알려주는 중요 헤더입니다. JSON 객체를 전송할 때는 주로 `application/json` 값을 사용합니다.
- **Content-Length**: 요청 바디의 크기(바이트 수)를 의미하며, 서버가 바이트 스트림을 얼마만큼 읽어야 요청 본문이 끝나는지 판단하는 기준이 됩니다.

## 3. 데이터 직렬화 (Serialization)
- 클라이언트 측(JS)에서는 객체를 전송하기 위해 문자열 타입으로 바꾼 직렬화(`JSON.stringify()`)를 거칩니다.
- 서버 측(FastAPI)에서는 수신한 JSON 문자열을 파이썬 객체로 파싱(역직렬화)하여 사용하며, 이 과정에서 Pydantic 모델을 통해 타입과 유효성을 자동으로 검증합니다.

---

## Django로의 연계 지점
향후 Django에서 API 형태로 JSON 데이터를 POST 요청으로 받을 때, Django 뷰는 데이터를 다음과 같이 처리하게 됩니다.
- 예: `data = json.loads(request.body)`
FastAPI에서 Pydantic 스키마(`PostCreate`)를 이용해 매개변수로 받는 구조가 Django의 `request.body` 바이트열 데이터를 로드하여 다루는 과정과 개념적으로 동일하다는 것을 이해하는 것이 중요합니다.
