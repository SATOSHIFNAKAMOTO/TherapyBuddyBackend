document.addEventListener("DOMContentLoaded", function() {
    const moodButtons = document.querySelectorAll('.emoji-button');
    
    moodButtons.forEach(button => {
        button.addEventListener('click', function() {
            const mood = this.getAttribute('data-mood');
            fetch('/submit_mood', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ mood: mood }),
            })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch((error) => console.error('Error:', error));
        });
    });
});
