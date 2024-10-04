document.addEventListener('DOMContentLoaded', () => {
    const socket = io(); // Initialize socket.io
    let currentRoom; // Store the current room for messaging

    // Fetch active users and update the list
    function fetchActiveUsers() {
        fetch('/active_users')
            .then(response => response.json())
            .then(users => {
                const userList = document.getElementById('active-users');
                userList.innerHTML = ''; // Clear current list
                users.forEach(user => {
                    const li = document.createElement('li');
                    li.textContent = user.username;
                    li.onclick = () => selectUser(user.id); // Select user to chat with
                    userList.appendChild(li);
                });
            })
            .catch(error => console.error('Error fetching active users:', error));
    }

    // Fetch and display inactive users
    function fetchInactiveUsers() {
        fetch('/inactive_users')
            .then(response => response.json())
            .then(users => {
                const userList = document.getElementById('inactive-users');
                userList.innerHTML = ''; // Clear current list
                users.forEach(user => {
                    const li = document.createElement('li');
                    li.textContent = user.username;
                    userList.appendChild(li);
                });
            })
            .catch(error => console.error('Error fetching inactive users:', error));
    }

    // Listen for updates from the server
    socket.on('update_user_list', () => {
        fetchActiveUsers();
        fetchInactiveUsers();
    });

    // Initial fetch
    fetchActiveUsers();
    fetchInactiveUsers();

    // Handle message display
    socket.on('message', (data) => {
        const chatBox = document.getElementById(`chat-box-${data.sessionId}`);
        if (chatBox) {
            const newMessage = document.createElement('div');
            newMessage.textContent = `${data.sender}: ${data.message}`;
            chatBox.appendChild(newMessage);
        }
    });

    // Open chat box for selected user
    function selectUser(otherUserId) {
        const chatBoxId = `chat-box-${otherUserId}`;
        openChat(chatBoxId);
        joinChatRoom(otherUserId); // Join the room for this user
    }

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
    

    // Sending a message
    function sendMessage(chatBoxId) {
        const messageInput = document.getElementById(`message-input-${chatBoxId}`);
        const message = messageInput.value.trim(); // Trim whitespace from input
        if (message && currentRoom) {
            socket.emit('private_message', { room: currentRoom, message: message });
            messageInput.value = ''; // Clear input after sending
        }
    }

    // Join a private room when starting a chat with another user
    function joinChatRoom(otherUserId) {
        const room = `room-${otherUserId}`; // Define room based on user ID
        socket.emit('join_room', { room });
        currentRoom = room; // Store current room
    }

    // Listen for new private messages
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
            const chatBoxId = button.dataset.chatBoxId; // Assume chatBoxId is stored in data attribute
            sendMessage(chatBoxId);
        });
    });
});
