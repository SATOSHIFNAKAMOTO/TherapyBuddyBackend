// mood.js file
document.addEventListener('DOMContentLoaded', function () {
    const moodButtons = document.querySelectorAll('.emoji-button');

    moodButtons.forEach(button => {
        button.addEventListener('click', function () {
            const mood = this.dataset.mood; 

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
                console.log(data); 
                alert('Your mood has been recorded: ' + mood); 
                updateMoodList(); // Refresh the display with the new entry
            })
            .catch((error) => {
                console.error('There has been a problem with your fetch operation:', error);
            });
        });
    });

    function updateMoodList() {
        fetch('/get_moods')
            .then(response => response.json())
            .then(data => {
                const moodList = document.getElementById('mood-list');
                moodList.innerHTML = ''; 

                data.forEach(moodEntry => {
                    const moodItem = document.createElement('div');
                    moodItem.textContent = `Mood: ${moodEntry.mood}, Recorded at: ${moodEntry.timestamp}`;
                    moodList.appendChild(moodItem);
                });
            })
            .catch((error) => {
                console.error('Error fetching moods:', error);
            });
    }

    updateMoodList(); // Retrieve and display moods on initial page load
});
