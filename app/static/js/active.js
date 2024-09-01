document.addEventListener('DOMContentLoaded', () => {
    const socket = io(); // Initialize socket.io

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
                    userList.appendChild(li);
                });
            });
    }

    // Listen for updates from the server
    socket.on('update_user_list', fetchActiveUsers);

    // Initial fetch
    fetchActiveUsers();
});
