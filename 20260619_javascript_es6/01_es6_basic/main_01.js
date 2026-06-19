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
    

});