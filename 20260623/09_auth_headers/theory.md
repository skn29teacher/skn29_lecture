# HTTP 헤더 제어와 Authorization Bearer 토큰 연동

## 1. HTTP 헤더 (HTTP Headers)
HTTP 헤더는 클라이언트와 서버가 HTTP 요청 또는 응답과 함께 추가적인 정보(메타데이터)를 전달할 수 있도록 해줍니다.

- **요청 헤더(Request Headers)**: 클라이언트 정보, 원하는 응답 타입, 캐시 옵션, 사용자 인증 수단 등을 담습니다 (예: `User-Agent`, `Accept`, `Authorization`).
- **응답 헤더(Response Headers)**: 응답 본문 크기, 데이터 타입, 쿠키 지시어 등을 담습니다 (예: `Content-Length`, `Content-Type`, `Set-Cookie`).

## 2. Authorization 헤더와 Bearer 토큰 인증
웹 API 환경에서 클라이언트를 인증할 때 가장 널리 쓰이는 표준 방식이 **Bearer 토큰 인증** 방식입니다.

- **작동 방식**: 로그인 성공 시 발급받은 문자열 토큰을 매 요청마다 HTTP `Authorization` 헤더에 담아 전송합니다.
- **포맷 규칙**: `Authorization: Bearer <토큰문자열>` 형태로 전송하며, 대소문자 구분을 지켜야 합니다.

## 3. 자바스크립트 Fetch API에서의 헤더 구성
Fetch 요청 시 두 번째 매개변수 객체의 `headers` 필드에 헤더 키-값 쌍을 지정해 보낼 수 있습니다.
```javascript
fetch(url, {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer my-secret-token'
    }
});
```

---

## Django로의 연계 지점
향후 Django 프레임워크에서 JWT(JSON Web Token)나 REST Framework(DRF)의 Token인증을 구현할 때, 백엔드 미들웨어 또는 뷰 단에서 클라이언트가 전달한 `Authorization` 헤더를 검사하게 됩니다.
- Django 내부 메타 환경 변수 접근 예시: `token = request.META.get('HTTP_AUTHORIZATION')`
- Django 3.x+ 직관적 헤더 접근 예시: `token = request.headers.get('Authorization')`
FastAPI에서 `Header(None)` 매개변수를 통해 헤더값을 취하는 과정이 Django의 `request.headers.get()`과 완전히 동일한 메커니즘을 밟고 있다는 점을 숙지합니다.
