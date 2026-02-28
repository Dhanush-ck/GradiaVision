const submitBtn = document.getElementById('submit-btn');
const userInput = document.getElementById('user-input');
userInput.focus();

let chatArea = document.getElementById('chat-area');

const welcomeScreen = document.getElementById('welcome-screen');

let error;

function sendMessage() {
    const message = userInput.value;
    hideWelcome();
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

        bubble.innerHTML = `
            <p class="commands-label">Here's what I can help you with 👇</p>
            <div class="command-list">
            <div class="command-chip" data-cmd="/cgpa">
                <span class="cmd-name">/cgpa</span>
                <span class="cmd-desc">See your current CGPA 📊</span>
            </div>
            <div class="command-chip" data-cmd="/predict">
                <span class="cmd-name">/predict</span>
                <span class="cmd-desc">Update your semester study details and get your next semester performance estimate 🔮</span>
            </div>
            <div class="command-chip" data-cmd="/">
                <span class="cmd-name">/</span>
                <span class="cmd-desc">Show these details again</span>
            </div>
            </div>
            `;

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
        // console.log(data.reply);
        if(data.help == 'help') {
            appendMessage(data.reply, 'bot', 'help');
        }
        else {
            appendMessage(data.reply, 'bot', ' ');
        }
    });

    userInput.value = "";
}

function appendMessage(text, role, type) {
  const msg = document.createElement('div');
  msg.classList.add(role);

  const bubble = document.createElement('div');
  bubble.classList.add('bubble');
  if(type == 'help') {
    bubble.classList.add('help');
    bubble.innerHTML = text;
  }
  else {
    bubble.textContent = text;
  }

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

document.querySelectorAll('.command-chip').forEach(chip => {
  chip.addEventListener('click', () => {
    const cmd = chip.dataset.cmd;
    document.getElementById('user-input').value = cmd;
    document.getElementById('submit-btn').click();
  });
});

document.getElementById('chat-area').addEventListener('click', (e) => {
  const chip = e.target.closest('.command-chip');
  if (!chip) return;

  const cmd = chip.dataset.cmd;
  document.getElementById('user-input').value = cmd;
  document.getElementById('submit-btn').click();
});

function hideWelcome() {
  welcomeScreen.classList.add('hidden');
  setTimeout(() => {
    welcomeScreen.style.display = 'none';
  }, 300);
}

userInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    document.getElementById('submit-btn').click();
  }
});