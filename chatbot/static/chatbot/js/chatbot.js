const submitBtn = document.getElementById('submit-btn');
const userInput = document.getElementById('user-input');

let chatArea = document.getElementById('chat-area');

let error;

function sendMessage() {
    const message = userInput.value;
    if(message.trim() === "") {
        return;
    }
    chatArea.innerHTML += `<div class='user'>${message}</div>`;

    fetch("/chatbot/reply/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        chatArea.innerHTML += `<div class="bot">${data.reply}</div>`;
        // chatArea.scrollTop = chatArea.scrollHeight;
    });

    userInput.value = "";
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

submitBtn.addEventListener('click', sendMessage);