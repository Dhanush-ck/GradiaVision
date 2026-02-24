const submitBtn = document.getElementById('submit-btn');
const userInput = document.getElementById('user-input');

let chatArea = document.getElementById('chat-area');

let error;

function sendMessage() {
    const message = userInput.value;
    if(message.trim() === "") {
        return;
    }
    if(message.trim() == "/") {
        appendMessage(message.trim(), 'user');
        const msg = document.createElement('div');
        msg.classList.add('bot');

        const bubble = document.createElement('div');
        bubble.classList.add('bubble');
        bubble.classList.add('help');
        bubble.innerHTML = "<b>/</b> - for action list <br> <b>/sgpa</b> - gives your sgpa <br>";

        msg.appendChild(bubble);
        document.getElementById('chat-area').appendChild(msg);
        document.querySelector('.chat-area-holder').scrollTop = 999999;
        userInput.value = "";
        return;
    }
    appendMessage(message.trim(), 'user');

    fetch("/chatbot/reply/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: message.trim() })
    })
    .then(response => response.json())
    .then(data => {
        appendMessage(data.reply, 'bot');
    });

    userInput.value = "";
}

function appendMessage(text, role) {
  const msg = document.createElement('div');
  msg.classList.add(role);

  const bubble = document.createElement('div');
  bubble.classList.add('bubble');
  bubble.textContent = text;

  msg.appendChild(bubble);
  document.getElementById('chat-area').appendChild(msg);
  document.querySelector('.chat-area-holder').scrollTop = 999999;
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