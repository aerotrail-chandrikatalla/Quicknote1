document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('noteForm');
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;

        // Your FastAPI endpoint URL
        const apiUrl = 'http://127.0.0.1:8000/notes';

        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                subject: title,
                description: description
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            alert('Note created successfully!');
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Failed to create note.');
        });
    });
});