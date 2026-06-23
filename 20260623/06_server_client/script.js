document.addEventListener('DOMContentLoaded',()=>{
    const btnConnect = document.querySelector('#btn-connect');
    const responseOutput = document.querySelector('#response-output');

    const API_URL = 'http://127.0.0.1:8000'
    btnConnect.addEventListener('click',()=>{
        fetch(`${API_URL}/api/countries`)
        .then( (response)=>{
            if(!response.ok){  // HTTP 상태코드가 200 ~ 299 가 아닐때
                throw new Error(`HTTP 오류 , 상태 코드 : ${response.status}`);
            }
            // 서버에 http 프로토콜을 통해 전달받은 데이터는 객체가 아니라 json 문자열
            // 문자열(response)을 .json()  객체로 변환
            return response.json();   // promise 객체를 내부적으로 리턴하게 되어 있음
        })
        .then( (data)=>{  // data는 json 객체 즉  리스트에 들어있는 딕셔너리들
            responseOutput.textContent = JSON.stringify(data);  
        })
        .catch( e =>{
            responseOutput.textContent = `오류발생 : ${e.message}`;
        });
    });

});