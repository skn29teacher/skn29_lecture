document.addEventListener('DOMContentLoaded', ()=>{
    const btnSearch = document.querySelector('#btn-search');
    const searchInput = document.querySelector('#search-input');  

    function fetchUsers(){
        const query = searchInput.value.trim();
        const urlObj = new URL('http://127.0.0.1:8000/api/users');
        // http://127.0.0.1:8000/api/users?search='홍길동'
        if(query){
            urlObj.searchParams.append('search',query); 
        }
        // fetch 호출
        fetch(urlObj.toString())
        .then( response =>{
            if(!response.ok){
                throw new Error(`HTTP 에러 코드 : ${response.status}`);
            }
            return response.json();
        })
        .then( users=>{
            if(users.length === 0){
                // 
                return;
            }
            // 사용자정보들
            users.forEach(user => { 
                // user.id
                // user.username
                // user.email
                // user.company_name
            });
        })
        .catch(e=>{
            // e.message
        });
    }

    btnSearch.addEventListener('click', fetchUsers);
    
});