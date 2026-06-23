document.addEventListener('DOMContentLoaded', ()=>{
    const postTitle = document.querySelector('#post-title');
    const postBody = document.querySelector('#post-body');
    const btnSubmit = document.querySelector('#btn-submit');
    const postsContainer = document.querySelector('#posts-container');

    // get 방식
    function loadPosts(){
        fetch('http://127.0.0.1/api/posts')
        .then( response=>{
            if(!response.ok) throw new Error(`오류 : 코드 : ${response.status}`);            
            return response.json();
        })
        .then( posts =>{
            if(posts.length === 0){
                postsContainer.innerHTML = '<p style="text-align: center; color: \
                    var(--text-secondary);">방명록 없음</p>'
                return;
            }
            posts.array.forEach(element => {
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
})