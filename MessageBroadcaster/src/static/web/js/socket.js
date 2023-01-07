const socket = io();
let messageContainer = document.querySelector(".messages");

socket.on("connect", () => {
  let p = document.createElement("p")
  p.innerText = "You're connected"
  messageContainer.appendChild(p)
})

// Emit message to flask server when user hits Enter
let messageInput = document.getElementById("messageInput")
messageInput.addEventListener("keypress", (e) => {
  if (e.which === 13) {
    let currenttime = new Date().toLocaleString();
    socket.emit("message", currenttime+"> "+messageInput.value)
    messageInput.value = ""
  }
})

// Receives message back and display it
socket.on("message", (message) => {
  let messageElement = document.createElement("p")
  messageElement.innerHTML = "<b>" + message.substring(0,message.indexOf('>')+1) + "</b>" +   message.substring(message.indexOf('>')+1);
  messageContainer.appendChild(messageElement)
})