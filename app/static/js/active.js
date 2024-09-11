// document.addEventListener('DOMContentLoaded', () => {
//     // Initialize Socket.IO
//     const socket = io(); // Connects to the server

//     // Function to fetch and display active users
//     function fetchActiveUsers() {
//         fetch('/active_users') // Adjust this URL to your endpoint
//             .then(response => response.json())
//             .then(users => {
//                 const userList = document.getElementById('active-users');
//                 userList.innerHTML = ''; // Clear current list
//                 users.forEach(user => {
//                     const li = document.createElement('li');
//                     li.textContent = user.username;
//                     userList.appendChild(li);
//                 });
//             })
//             .catch(error => console.error('Error fetching active users:', error));
//     }

//     // Handle updates from the server about active users
//     socket.on('update_user_list', (users) => {
//         // Update the list with the latest active users
//         const userList = document.getElementById('active-users');
//         userList.innerHTML = ''; // Clear current list
//         users.forEach(user => {
//             const li = document.createElement('li');
//             li.textContent = user.username;
//             userList.appendChild(li);
//         });
//     });

//     // Initial fetch of active users
//     fetchActiveUsers();
// });
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
                    li.textContent = `${user.username} ${user.is_online ? '(Online)' : '(Offline)'}`;
                    userList.appendChild(li);
                });
            });
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
                });
    }

    // Listen for updates from the server
    socket.on('update_user_list', () => {
        fetchActiveUsers();
        fetchInactiveUsers();
    });

    // Initial fetch
    fetchActiveUsers();
    fetchInactiveUsers();
});
