document.addEventListener('DOMContentLoaded', function() {
    let currentRoom = null;
    const socket = io();  // This initializes the socket connection to your Flask-SocketIO backend


    // Define the openChat function
    function openChat(event, chatWindowId) {
        // Hide all chat windows
        var chatBoxes = document.getElementsByClassName('chat-box');
        for (var i = 0; i < chatBoxes.length; i++) {
            chatBoxes[i].style.display = 'none';
        }

        // Show the selected chat window
        var chatWindow = document.getElementById(chatWindowId);
        if (chatWindow) {
            chatWindow.style.display = 'block';
        }
    }

    // Select a user to start a chat session
    function selectUser(otherUserId) {
        const chatBoxId = `chat-box-${otherUserId}`;
        openChat(null, chatBoxId); // Open the chat window
        joinChatRoom(otherUserId);  // Join the room for the selected user
    }

    // Send a message in the current chat session
    function sendMessage(chatBoxId) {
        const messageInput = document.getElementById(`message-input-${chatBoxId}`);
        const message = messageInput.value.trim(); // Trim whitespace from input
        if (message && currentRoom) {
            socket.emit('private_message', { room: currentRoom, message: message });
            messageInput.value = ''; // Clear input after sending
        }
    }

    // Join a private chat room
    function joinChatRoom(otherUserId) {
        const room = `room-${otherUserId}`; // Define the room based on the other user's ID
        socket.emit('join_room', { room });
        currentRoom = room; // Store the current room for future use
    }

    // Listen for incoming private messages
    socket.on('new_private_message', (data) => {
        const chatBox = document.getElementById(`chat-box-${data.senderId}`);
        if (chatBox) {
            const newMessage = document.createElement('div');
            newMessage.textContent = data.message;
            chatBox.appendChild(newMessage); // Append the new message to the chat box
        }
    });

    // Add event listeners for message sending buttons
    document.querySelectorAll('.send-message-btn').forEach(button => {
        button.addEventListener('click', () => {
            const chatBoxId = button.dataset.chatBoxId; // Assume chatBoxId is stored in the data attribute
            sendMessage(chatBoxId);
        });
    });
});
