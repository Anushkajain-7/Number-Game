let currentStep = 1;

async function startGame() {
    try {
        const res = await fetch('/api/start', { method: 'POST' });
        const data = await res.json();

        if (data.status === 'success') {
            updateUI(data.node, data.step);
            sessionStorage.setItem('gamePath', JSON.stringify([])); // Clear history
        }
    } catch (e) {
        console.error("Error starting game", e);
        document.getElementById('question-text').innerText = "Error connecting to server.";
    }
}

async function answer(choice) {
    try {
        const res = await fetch('/api/answer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ answer: choice })
        });
        const data = await res.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        // Save path to session storage for result page
        sessionStorage.setItem('gamePath', JSON.stringify(data.path));

        if (data.finished) {
            // It's a guess! Redirect to result page
            // extract guess from node
            const guess = data.node.guess;
            window.location.href = `/result?guess=${guess}`;
        } else {
            // Next question
            updateUI(data.node, data.step);
            updateGlobalPathSidebar(data.path);
        }

    } catch (e) {
        console.error("Error answering", e);
    }
}

function updateUI(node, step) {
    // Fade out text first
    const qText = document.getElementById('question-text');
    qText.style.opacity = 0;

    setTimeout(() => {
        qText.innerText = node.text;
        document.getElementById('step-indicator').innerText = `Step ${step}`;
        qText.style.opacity = 1;
    }, 200);
}

function updateGlobalPathSidebar(path) {
    const sb = document.getElementById('path-sidebar');
    sb.style.display = 'block';
    sb.innerHTML = ''; // Re-render simple list
    // reverse to show latest at top? No, chronological is better for trail
    path.forEach(p => {
        const div = document.createElement('div');
        div.className = 'path-step';
        div.innerHTML = `Q: ${p.question} <span class="${p.answer === 'YES' ? 'path-answer-yes' : 'path-answer-no'}">${p.answer}</span>`;
        sb.appendChild(div);
    });
    // Scroll to bottom
    sb.scrollTop = sb.scrollHeight;
}
