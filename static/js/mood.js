// mood.js file
document.addEventListener('DOMContentLoaded', function () {
    const moodButtons = document.querySelectorAll('.emoji-button');
  
    moodButtons.forEach(button => {
        button.addEventListener('click', function () {
            const mood = this.dataset.mood;  // 'data-mood' attribute value of clicked button
  
            fetch('/submit_mood', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ mood: mood }),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                console.log(data); // For debugging: log the data received from server
                alert('Your mood has been recorded: ' + mood);  // Alert or modify the DOM as required
            })
            .catch((error) => {
                console.error('There has been a problem with your fetch operation:', error);
            });
        });
    });
});
