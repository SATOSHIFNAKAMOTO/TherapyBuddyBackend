async function sendMessage() {
    const userInputField = document.getElementById('userInput');
    const userMessage = userInputField.value;
    userInputField.value = ''; // Clear the input field

    try {
        // Replace `your_public_url` with the Public URL provided
        const response = await fetch('https://335d8d29-3047-4295-bae6-9512c47e2f63-prod.e1-us-cdp-2.choreoapis.dev/therapy-buddy-3/therapybuddybackend-2/chatbot-803/v1.0', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userMessage }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        // Append the bot's response to the chat
        const chatDiv = document.getElementById('chat');
        chatDiv.innerHTML += `<div class='message'>Bot: ${data.message}</div>`;
    } catch (error) {
        console.error('Error sending message:', error);
    }
}
