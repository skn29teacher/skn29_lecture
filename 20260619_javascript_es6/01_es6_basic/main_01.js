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

    

});