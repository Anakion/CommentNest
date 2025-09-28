
    const statusEl = document.getElementById('status');
    let socket = null;
    const expandedComments = new Set();

    // ==================== WebSocket ====================
    function connectWebSocket() {
        if (socket) socket.close();
        const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        const wsUrl = wsProtocol + window.location.host + '/api/v1/ws/comments';
        socket = new WebSocket(wsUrl);

        socket.onopen = () => {
            statusEl.textContent = 'Подключено';
            statusEl.className = 'connected';
            loadComments();
        };
        socket.onclose = () => {
            statusEl.textContent = 'Отключено';
            statusEl.className = 'disconnected';
            setTimeout(connectWebSocket, 5000);
        };
        socket.onerror = (e) => {
            console.error('WebSocket ошибка:', e);
            statusEl.textContent = 'Ошибка подключения';
            statusEl.className = 'disconnected';
        };
        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'new_comment') {
                const comment = data.data;
                if (!comment.parent_id) addMainComment(comment, true, true);
                else addReply(comment, true, true);
            }
        };
    }

    // ==================== Комментарии ====================
    async function loadComments() {
        try {
            const res = await fetch('/api/v1/comments/with-replies?per_page=50&sort_by=created_at&order=desc');
            if (!res.ok) throw new Error('Ошибка загрузки комментариев');
            const comments = await res.json();
            displayComments(comments);
        } catch(e) {
            console.error('Ошибка:', e);
            document.getElementById('comments').innerHTML = '<p>Ошибка загрузки комментариев</p>';
        }
    }

    function displayComments(comments) {
        const container = document.getElementById('comments');
        if (!comments || comments.length === 0){
            container.innerHTML = '<p>Комментариев пока нет. Будьте первым!</p>';
            return;
        }
        container.innerHTML = '';
        comments.forEach(comment => {
            addMainComment(comment, false, false);
            if (comment.replies) {
                comment.replies.sort((a,b)=>new Date(b.created_at)-new Date(a.created_at))
                .forEach(reply => addReply(reply,false,false));
            }
        });
    }

    function addMainComment(comment, scroll=true, insertAtStart=true){
        const container = document.getElementById('comments');
        if(document.getElementById(`comment-${comment.id}`)) return;
        const hasReplies = comment.replies && comment.replies.length>0;
        const arrowHtml = hasReplies ? '<div class="toggle-replies collapsed"></div>' : '<div style="width:24px;margin-right:10px;"></div>';
        const html = `
            <div class="comment" id="comment-${comment.id}">
                <div class="comment-header" onclick="toggleReplies(this)">
                    ${arrowHtml}
                    <div>
                        <div class="user-name">${escapeHtml(comment.user_name)}</div>
                        <div class="timestamp">${new Date(comment.created_at).toLocaleString()}</div>
                    </div>
                </div>
                <div class="comment-text">${escapeHtml(comment.text)}</div>
                <button onclick="event.stopPropagation(); showReplyModal(${comment.id}, '${escapeHtml(comment.user_name)}')" class="reply-btn">Ответить</button>
                ${hasReplies?`<div class="replies-container"></div>`:''}
            </div>`;
        if(insertAtStart) container.insertAdjacentHTML('afterbegin',html);
        else container.insertAdjacentHTML('beforeend',html);
        if(scroll) container.scrollIntoView({behavior:'smooth'});
    }

    function addReply(reply, scroll=true, insertAtStart=true){
        const parent = document.getElementById(`comment-${reply.parent_id}`);
        if(!parent) return;
        let repliesContainer = parent.querySelector('.replies-container');
        if(!repliesContainer){
            repliesContainer = document.createElement('div');
            repliesContainer.classList.add('replies-container');
            parent.appendChild(repliesContainer);
            const header = parent.querySelector('.comment-header');
            const toggle = header.querySelector('.toggle-replies');
            if(!toggle){
                const newToggle = document.createElement('div');
                newToggle.classList.add('toggle-replies','expanded');
                newToggle.onclick=(e)=>{e.stopPropagation();toggleReplies(header)};
                header.insertBefore(newToggle, header.firstChild);
            }
        }
        if(repliesContainer.querySelector(`#reply-${reply.id}`)) return;
        const html = `
            <div class="reply" id="reply-${reply.id}">
                <div class="user-name">${escapeHtml(reply.user_name)}</div>
                <div class="comment-text">${escapeHtml(reply.text)}</div>
                <div class="timestamp">${new Date(reply.created_at).toLocaleString()}</div>
            </div>`;
        if(insertAtStart) repliesContainer.insertAdjacentHTML('afterbegin',html);
        else repliesContainer.insertAdjacentHTML('beforeend',html);
        repliesContainer.classList.add('visible');
        if(scroll) repliesContainer.scrollIntoView({behavior:'smooth'});
    }

    // ==================== Прочее ====================
    function toggleReplies(element){
        const container = element.closest('.comment').querySelector('.replies-container');
        const toggleBtn = element.querySelector('.toggle-replies');
        if(container && toggleBtn){
            container.classList.toggle('visible');
            toggleBtn.classList.toggle('collapsed');
            toggleBtn.classList.toggle('expanded');
            const id = element.closest('.comment').id;
            if(container.classList.contains('visible')) expandedComments.add(id);
            else expandedComments.delete(id);
        }
    }

    function showReplyModal(commentId, userName){
        const modal = document.getElementById('replyModal');
        document.getElementById('replyToUser').textContent = userName;
        document.getElementById('replyCommentId').value = commentId;

        // Очищаем поля и ошибки при открытии модального окна
        document.getElementById('replyUserName').value = '';
        document.getElementById('replyUserEmail').value = '';
        document.getElementById('replyText').value = '';
        document.getElementById('replyCaptcha').value = '';
        clearErrors('reply');

        modal.style.display='flex';
        document.getElementById('cancelReply').onclick=()=>{
            modal.style.display='none';
            clearErrors('reply');
        };
        modal.onclick=(e)=>{
            if(e.target===modal) {
                modal.style.display='none';
                clearErrors('reply');
            }
        };
    }

    function escapeHtml(unsafe){
        if(!unsafe) return '';
        return unsafe.toString().replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")
            .replace(/"/g,"&quot;").replace(/'/g,"&#039;");
    }

    // ==================== Ошибки полей ====================
    function clearErrors(prefix=''){
        const fields = ['userName','userEmail','commentText','captcha'];
        fields.forEach(field => {
            const errEl = document.getElementById(prefix + (prefix ? field.charAt(0).toUpperCase() + field.slice(1) : field) + 'Error');
            if(errEl) errEl.textContent = '';
        });
    }

    function showErrors(errors, prefix=''){
        clearErrors(prefix);
        if(!errors || !Array.isArray(errors)) return;

        const fieldMap = {
            'user_name': prefix ? 'replyUserName' : 'userName',
            'email': prefix ? 'replyUserEmail' : 'userEmail',
            'text': prefix ? 'replyText' : 'commentText',
            'captcha': prefix ? 'replyCaptcha' : 'captcha'
        };

        errors.forEach(error => {
            const fieldName = error.loc && error.loc[1];
            if(fieldName && fieldMap[fieldName]) {
                const errorEl = document.getElementById(fieldMap[fieldName] + 'Error');
                if(errorEl) {
                    errorEl.textContent = error.msg;
                }
            }
        });
    }

    // ==================== События DOM ====================
    document.addEventListener('DOMContentLoaded',()=>{

        connectWebSocket();

        // Главный комментарий
        document.getElementById('sendButton').addEventListener('click', async()=>{
            const payload = {
                user_name: document.getElementById('userName').value.trim(),
                email: document.getElementById('userEmail').value.trim(),
                text: document.getElementById('commentText').value.trim(),
                captcha: document.getElementById('captcha').value.trim(),
                parent_id: null
            };
            try{
                const response = await fetch('/api/v1/comments/',{
                    method:'POST',
                    headers:{'Content-Type':'application/json'},
                    body:JSON.stringify(payload)
                });
                const data = await response.json();
                console.log('Ответ сервера (main):', data);
                if(response.ok){
                    document.getElementById('commentText').value='';
                    document.getElementById('captcha').value='';
                    clearErrors();
                } else {
                    showErrors(data.detail || []);
                }
            } catch(e){
                console.error('Ошибка:', e);
            }
        });

        // Ответ на комментарий
        document.getElementById('submitReply').addEventListener('click', async()=>{
            const payload = {
                user_name: document.getElementById('replyUserName').value.trim(),
                email: document.getElementById('replyUserEmail').value.trim(),
                text: document.getElementById('replyText').value.trim(),
                captcha: document.getElementById('replyCaptcha').value.trim(),
                parent_id: document.getElementById('replyCommentId').value
            };
            try{
                const response = await fetch('/api/v1/comments/',{
                    method:'POST',
                    headers:{'Content-Type':'application/json'},
                    body:JSON.stringify(payload)
                });
                const data = await response.json();
                console.log('Ответ сервера (reply):', data);
                if(response.ok){
                    document.getElementById('replyText').value='';
                    document.getElementById('replyCaptcha').value='';
                    document.getElementById('replyModal').style.display='none';
                    clearErrors('reply');
                } else {
                    showErrors(data.detail || [], 'reply');
                }
            } catch(e){
                console.error('Ошибка:', e);
            }
        });

    });
