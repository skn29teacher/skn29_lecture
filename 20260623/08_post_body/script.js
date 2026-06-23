document.addEventListener('DOMContentLoaded', ()=>{
    const postTitle = document.querySelector('#post-title');
    const postBody = document.querySelector('#post-body');
    const btnSubmit = document.querySelector('#btn-submit');
    const postsContainer = document.querySelector('#posts-container');

    // get 방식
    function loadPosts(){
        fetch('http://127.0.0.1:8000/api/posts')
        .then( response=>{
            if(!response.ok) throw new Error(`오류 : 코드 : ${response.status}`);            
            return response.json();
        })
        .then( posts =>{
            postsContainer.innerHTML = '';
            if(posts.length === 0){
                postsContainer.innerHTML = '<p style="text-align: center; color: \
                    var(--text-secondary);">방명록 없음</p>'
                return;
            }
            posts.forEach(element => {
                const div = document.createElement('div');
                div.className = 'post-item';
                div.innerHTML = `
                    <div class="post_author">${element.title}</div>
                    <div class="post-body">${element.body}</div>
                    `;
                postsContainer.appendChild(div);
            });
        })
        .catch(e=>{
            postsContainer.textContent = e.message;
        });
    }

    loadPosts();


    btnSubmit.addEventListener('click',()=>{
        fetch("http://127.0.0.1:8000/api/posts",{
            method : 'POST',
            headers : {'Content-Type':'application/json'},
            body : JSON.stringify({title:postTitle.value.trim(), body:postBody.value.trim()})
        })
        .then(response=>{
            return response.json();
        })
        .then(data=>{
            postTitle.value='';
            postBody.value='';
            loadPosts();
        })
        .catch(e=>{
            alert(e.message);
        });        
    });
})