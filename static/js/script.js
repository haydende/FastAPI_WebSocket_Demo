const clientId = Date.now();
let chatroomName = null;
let ws = null;

function sendMessage(event) {
    let input = document.getElementById("messageText");
    console.log(`Attempting to send message ["${input.value}"] to WebSocket ["${ws.url}"]`);
    ws.send(input.value);
    input.value = '';
    event.preventDefault();
}

function connectToChatroom(event) {
    const input = document.getElementById("chatroomNameText");
    chatroomName = input.value
    const url = `ws://localhost:8000/ws/${chatroomName}/${clientId}`;
    console.log(`Attempting to connect to WebSocket at URL [${url}]`);
    if (ws) {
        leaveRoom();
    }
    ws = new WebSocket(url);
    ws.onmessage = function (event) {
        let messages = document.getElementById('messages');
        let message = document.createElement('li');
        let content = document.createTextNode(event.data);
        messages.appendChild(message);
        message.appendChild(content);
    };
    document.getElementById("connected-label").innerHTML = `Connected to ${chatroomName} with ID ${clientId}`;
    event.preventDefault();
}

function leaveRoom(event) {
    if (ws) {
        ws.close();
        document.getElementById("connected-label").innerHTML = `Disconnected from ${chatroomName}!`;
        event.preventDefault();
    }
}