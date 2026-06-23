document.addEventListener('DOMContentLoaded', () => {
    const btnRequest = document.getElementById('btn-request');
    const btnWrongSchema = document.getElementById('btn-wrong-schema');
    const btnClear = document.getElementById('btn-clear');
    
    const tokenInput = document.getElementById('token-input');
    
    const responseStatus = document.getElementById('response-status');
    const responseBody = document.getElementById('response-body');

    const API_URL = 'http://127.0.0.1:8000/api/secure-data';

    // 결과 출력 헬퍼 함수
    function displayResponse(status, data) {
        responseStatus.textContent = status;
        responseStatus.style.color = '';
        if (status === 200) {
            responseStatus.style.color = '#34d399'; // 초록 (성공)
        } else if (status === 400 || status === 401 || status === 403) {
            responseStatus.style.color = '#fbbf24'; // 주황 (클라이언트 에러)
        } else {
            responseStatus.style.color = '#f87171'; // 빨강 (에러)
        }
        responseBody.textContent = JSON.stringify(data, null, 4);
    }

    // 공통 요청 전송 함수
    function sendSecureRequest(headerValue) {
        const headers = {};
        if (headerValue !== undefined) {
            headers['Authorization'] = headerValue;
        }

        fetch(API_URL, {
            method: 'GET',
            headers: headers
        })
            .then(async response => {
                const data = await response.json();
                displayResponse(response.status, data);
            })
            .catch(error => {
                displayResponse('Network Error', { error: error.message });
            });
    }

    // 1. 정상 규격으로 토큰 전송 (Bearer <토큰>)
    btnRequest.addEventListener('click', () => {
        const token = tokenInput.value.trim();
        sendSecureRequest(`Bearer ${token}`);
    });

    // 2. Bearer가 누락된 비정상적인 헤더 규격 전송
    btnWrongSchema.addEventListener('click', () => {
        const token = tokenInput.value.trim();
        sendSecureRequest(token); // Bearer 스키마 생략하고 토큰만 전송
    });

    // 3. Authorization 헤더 자체를 누락하고 전송
    btnClear.addEventListener('click', () => {
        sendSecureRequest(undefined); // 헤더 추가하지 않음
    });
});
