document.addEventListener('DOMContentLoaded', ()=>{
    const btnSearch = document.querySelector('#btn-search');
    const searchInput = document.querySelector('#search-input');  
    const usersTbody = document.querySelector('#users-tbody');

    function fetchUsers(){
        usersTbody.textContent='';
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
                usersTbody.innerHTML ='<td colspan="5" style="text-align: center; color: var(--text-secondary);">검색결과가 없습니다.</td>';                
                return;
            }
            // 사용자정보들
            users.forEach(user => { 
                const tr = document.createElement('tr')
                tr.innerHTML = `
                <td>${user.id}</td>
                <td>${user.name}</td>
                <td>${user.username}</td>
                <td>${user.email}</td>
                <td>${user.company_name}</td>`
                usersTbody.appendChild(tr);
            });
        })
        .catch(e=>{
            // e.message
        });
    }

    btnSearch.addEventListener('click', fetchUsers);
    searchInput.addEventListener('keydown', (e)=>{
        if (e.key == 'Enter'){
            fetchUsers();
        }
    })
});