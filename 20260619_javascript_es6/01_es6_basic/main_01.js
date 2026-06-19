document.addEventListener('DOMContentLoaded',()=>{
    const termScope = document.getElementById("term-scope");    
    const termConst = document.getElementById("term-const")
    const termThis = document.getElementById("term-this")
    const profileContainer = document.getElementById('profile-card-container')

    document.getElementById('btn-var-scope')?.addEventListener('click',()=>{
        if(true){
            var escapedVar = "var는 함수 스코프 블록 외부로 유출됩니다."
        }
        termScope.textContent = `블록 내부에서 var로 선언한 변수 호출 성공:\n "${escapedVar}"\n\이처럼 var는 if나 for 블럭 밖에서도 살아남아 전역 오염을 일으킵니다. ` ;
    });

    document.getElementById('btn-let-scope')?.addEventListener('click',()=>{
        let errorMessage = "";
        // 블럭 스코프 테스트
        try{
            if(true){
                let isolatedLet = "let은 블럭 내부에 격리됩니다.";
            }
            // 블럭 밖에서   isolatedLet 호출 시도
            console.log(isolatedLet);
        }catch(e){
            errorMessage += `[블럭 외부 참조에러]let/const는 블럭 밖에서 읽수 없습니다.\n 오류메세지는 ${e.message}`;
        }
        // TDZ  선언 전 호출 테스트
        try{
            console.log(tdzVariable);
            let tdzVariable = '나중에 선언된 let 변수'
        }catch(e){
            errorMessage +=`\n\n[참조 에러] let/const는 호이스팅은 되지만 초기화 전에 참조불가영역 TDZ에 묶여 에러를 발생\n 오류메세지는 ${e.message}`
        }
        termScope.textContent = errorMessage;
    });
    
    document.getElementById("btn-loop-var")?.addEventListener('click',()=>{
        termScope.textContent = "var 루프 비동기 출력 작동중......\n";
        // var로 선언한 인덱스는 루프 완료시점에 3으로 설정됩니다.
        for( var i =0 ; i <3 ; i++){
            console.log(i);
            // 100ms 뒤 작동하는 비동기 함수 실행
            setTimeout(()=>{
                termScope.textContent += `[var 출력] 비동기 콜백 시점의 인덱스 i 값: ${i}\n`;
                console.log(`[var 오염 로그] 인덱스 i : ${i}`);
            }, 100);
        }
    });

    document.getElementById('btn-loop-let')?.addEventListener('click',()=>{
        termScope.textContent = "let 루프 비동기 출력 작동중......\n";
        for(let k = 0; k<3; k++){
            setTimeout(() => {
                termScope.textContent += `[let 출력] 비동기 콜백시점의 인덱스 k 값: ${k}\n`;
                console.log(`[let 안전 로그] 인덱스 k : ${k}`);
            }, 100);
        }
    });

    // 객체의 얕은 변경 제어 및 Objet.freeze() 동결
    document.getElementById('btn-const-modify')?.addEventListener('click',()=>{
        const mutableUser = {name:'홍길동', level:"초급"};
        // 속성 수정 및 추가 시도
        mutableUser.level = "중급";
        mutableUser.name ="javaScript ES6";
        termConst.textContent = `const 객체 속성 수정결과:\n${JSON.stringify(mutableUser,null,2)}`;
        termConst.textContent += "\n\n(참조 주소 자체를 바꾸는 mutableUser= {} 형태의 불가능하지만 내부 프로퍼티 제어는 차단되지 않는다"
    });
    document.getElementById('btn-const-freeze')?.addEventListener('click',()=>{
        // strict mode 활성화 해서 동결된 객체 수정시 에러를 유도
        // "use strict"

        const frozeUser = {name:'홍길동', level:"초급"};
        // 객체를 물리적 동결
        Object.freeze(frozeUser);
        let freezeLog = `객체 동결 성공 여부 : ${Object.isFrozen(frozeUser)? "동결 완료" : "동결 실패"}\n `
        try{
            frozeUser.level="중급";
            freezeLog += `에러없이 통과되었으나 수정사항이 반영안됨 현재 level = ${frozeUser.level}`;
        }catch(e){
            freezeLog += `수정 에러 발생 : ${e.message}`
        }
        termConst.textContent = freezeLog;        
    });

}); // load