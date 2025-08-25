let connectionId = Date.now();

const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
const ws = new WebSocket(protocol + "//" + location.host + "/ws/" + connectionId);

ws.onmessage = function(event) {
    let chat = document.getElementById("chat");
    let message = document.createElement("div");
    message.textContent = event.data;
    chat.appendChild(message);
    chat.scrollTop = chat.scrollHeight;
};

document.getElementById("sendBtn").onclick = function() {
    let input = document.getElementById("messageInput");
    if (input.value.trim() !== "") {
        ws.send(input.value);
        input.value = "";
    }
};

document.getElementById("messageInput").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        document.getElementById("sendBtn").click();
    }
});