// TravelMate AI - Client-Side Interactive Engine

document.addEventListener('DOMContentLoaded', () => {
    // 1. "Ask TravelMate AI" widget logic
    const aiForm = document.getElementById('askAiForm');
    const aiInput = document.getElementById('aiQueryInput');
    const aiResponseBox = document.getElementById('aiResponseBox');
    const aiResponseText = document.getElementById('aiResponseText');
    const aiSpinner = document.getElementById('aiSpinner');

    // Quick suggestion pills click handler
    document.querySelectorAll('.ai-pill-suggestion').forEach(pill => {
        pill.addEventListener('click', () => {
            const query = pill.getAttribute('data-query');
            if (aiInput) {
                aiInput.value = query;
                submitAiQuery(query);
            }
        });
    });

    if (aiForm) {
        aiForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const query = aiInput.value.trim();
            if (query) {
                submitAiQuery(query);
            }
        });
    }

    function submitAiQuery(query) {
        if (!aiResponseBox || !aiResponseText) return;

        aiResponseBox.classList.remove('d-none');
        if (aiSpinner) aiSpinner.classList.remove('d-none');
        aiResponseText.innerHTML = '<span class="text-muted">Analyzing route, packlists, and regional conditions...</span>';

        fetch('/assistant/ask-ai/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        })
        .then(res => res.json())
        .then(data => {
            if (aiSpinner) aiSpinner.classList.add('d-none');
            // Format markdown bold & bullet lists
            let formatted = data.response
                .replace(/\n/g, '<br>')
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            aiResponseText.innerHTML = formatted;
        })
        .catch(err => {
            if (aiSpinner) aiSpinner.classList.add('d-none');
            aiResponseText.innerHTML = '<span class="text-danger">Unable to connect to AI server. Please try again.</span>';
        });
    }

    // 2. Interactive Review Sentiment Tester (Figma Screen 3 Tool 6)
    const testReviewBtn = document.getElementById('testReviewBtn');
    const testReviewInput = document.getElementById('testReviewInput');
    const sentimentLabel = document.getElementById('sentimentResultLabel');
    const sentimentPosBar = document.getElementById('sentimentPosBar');
    const sentimentNeuBar = document.getElementById('sentimentNeuBar');
    const sentimentNegBar = document.getElementById('sentimentNegBar');

    if (testReviewBtn && testReviewInput) {
        testReviewBtn.addEventListener('click', () => {
            const text = testReviewInput.value.trim();
            if (!text) return;

            const formData = new FormData();
            formData.append('review_text', text);

            fetch('/assistant/sentiment-api/', {
                method: 'POST',
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (sentimentLabel) {
                    sentimentLabel.textContent = `${data.label} (${data.positive_pct}% Positivity)`;
                    sentimentLabel.className = data.label === 'Positive' ? 'badge bg-success' : (data.label === 'Negative' ? 'badge bg-danger' : 'badge bg-warning');
                }
                if (sentimentPosBar) sentimentPosBar.style.width = `${data.positive_pct}%`;
                if (sentimentNeuBar) sentimentNeuBar.style.width = `${data.neutral_pct}%`;
                if (sentimentNegBar) sentimentNegBar.style.width = `${data.negative_pct}%`;
            });
        });
    }
});
