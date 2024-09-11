document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');

    function scrollToBottom() {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    scrollToBottom();  // Scroll to the bottom on page load

    // Optional: Scroll to bottom when a new message is added
    const observer = new MutationObserver(scrollToBottom);
    observer.observe(chatBox, { childList: true });






// });
// document.addEventListener('DOMContentLoaded', () => {
    // Initialize Socket.IO
    const socket = io(); // Connects to the server

    // Function to fetch and display active users
    function fetchActiveUsers() {
        fetch('/active_users') // Adjust this URL to your endpoint
            .then(response => response.json())
            .then(users => {
                const userList = document.getElementById('active-users');
                userList.innerHTML = ''; // Clear current list
                users.forEach(user => {
                    const li = document.createElement('li');
                    li.textContent = user.username;
                    userList.appendChild(li);
                });
            })
            .catch(error => console.error('Error fetching active users:', error));
    }

    // Handle updates from the server about active users
    socket.on('update_user_list', () => {
        fetchActiveUsers(); // Fetch and update the list of active users
    });

    // Initial fetch of active users
    fetchActiveUsers();
});

