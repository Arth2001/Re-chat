document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');

    function scrollToBottom() {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    scrollToBottom();  // Scroll to the bottom on page load

    // Optional: Scroll to bottom when a new message is added
    const observer = new MutationObserver(scrollToBottom);
    observer.observe(chatBox, { childList: true });
});
