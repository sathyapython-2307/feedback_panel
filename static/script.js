document.getElementById('feedbackForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('name').value.trim();
    const message = document.getElementById('message').value.trim();

    const res = await fetch('/api/feedback', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ name, message })
    });
    const data = await res.json();
    document.getElementById('alertBox').innerHTML = 
        `<div class="alert alert-success">${data.message}</div>`;
    document.getElementById('feedbackForm').reset();
    loadFeedbacks();
});

async function loadFeedbacks() {
    const res = await fetch('/api/feedbacks');
    const feedbacks = await res.json();
    const list = document.getElementById('feedbackList');
    list.innerHTML = '';
    feedbacks.forEach(fb => {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.innerHTML = `<strong>${fb.name}</strong>: ${fb.message} <br><small>${fb.time}</small>`;
        list.appendChild(li);
    });
}

window.onload = loadFeedbacks;
