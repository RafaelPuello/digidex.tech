document.getElementById('send-button').addEventListener('click', function() {
    const userInput = document.getElementById('chat-input').value;

    if (userInput.trim() === "") return;

    // Check if the JWT token is available in localStorage
    const token = localStorage.getItem('jwtToken');
    const userUUID = document.getElementById('inventory-assistant').getAttribute('data-id');
    // Display the user's message
    const userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'user-message';
    userMessageDiv.innerText = userInput;
    document.getElementById('chat-messages').appendChild(userMessageDiv);
    document.getElementById('chat-input').value = "";

    // Prepare the AJAX request
    const xhr = new XMLHttpRequest();
    const apiUrl = `/api/v2/assistant/${userUUID}/chat/?question=${encodeURIComponent(userInput)}`;

    xhr.open('GET', apiUrl, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    // xhr.setRequestHeader('Authorization', `Bearer ${token}`);

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);

            const botMessageDiv = document.createElement('div');
            botMessageDiv.className = 'bot-message';
            botMessageDiv.innerText = response.chat;
            document.getElementById('chat-messages').appendChild(botMessageDiv);
            document.getElementById('chat-messages').scrollTop = document.getElementById('chat-messages').scrollHeight;
        } else if (xhr.readyState === 4) {
            console.error('Error:', xhr.statusText);
        }
    };
    // Send the request
    xhr.send();
});