document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const chatContainer = document.getElementById('chat-container');

    function addMessage(text, type) {
        const msgDiv = document.createElement('div');
        const baseClasses = "max-w-[80%] px-4 py-3 rounded-xl leading-relaxed text-sm";
        const userClasses = "self-end bg-blue-600 text-white rounded-br-sm";
        const systemClasses = "self-start bg-slate-100 rounded-bl-sm text-slate-800"; 
        const specificClasses = type === 'user' ? userClasses : systemClasses;
        msgDiv.className = `${baseClasses} ${specificClasses}`;
        
        let formattedText = text
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            
        msgDiv.innerHTML = formattedText;
        chatContainer.appendChild(msgDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async function handleSend() {
        const query = input.value.trim();
        if (!query) return;

        addMessage(query, 'user');
        input.value = '';

        const loadingDiv = document.createElement('div');

        const baseClasses = "max-w-[80%] px-4 py-3 rounded-xl leading-relaxed text-sm";
        const systemClasses = "self-start bg-slate-100 rounded-bl-sm text-slate-800";
        loadingDiv.className = `${baseClasses} ${systemClasses}`;
        loadingDiv.textContent = 'Thinking...';
        chatContainer.appendChild(loadingDiv);

        try {
            const response = await fetch('/api/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query })
            });
            
            const data = await response.json();
            
            chatContainer.removeChild(loadingDiv);

            if (data.error) {
                addMessage(`Error: ${data.error}`, 'system');
            } else {
                addMessage(data.response, 'system');
            }
        } catch (error) {
            chatContainer.removeChild(loadingDiv);
            addMessage('Sorry, something went wrong connecting to the server.', 'system');
            console.error('Error:', error);
        }
    }

    sendBtn.addEventListener('click', handleSend);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
    });
});
