document.getElementById('executeBtn').addEventListener('click', async () => {
    const input = document.getElementById('objectiveInput').value;
    const btn = document.getElementById('executeBtn');
    const agentCard = document.getElementById('activeAgentDisplay');
    const agentName = document.getElementById('agentName');
    const agentStatus = document.getElementById('agentStatus');
    const jsonViewer = document.getElementById('jsonViewer').querySelector('code');

    if (!input.trim()) return;

    // UI Updates - Processing State
    btn.disabled = true;
    btn.innerText = "Executing Protocol...";
    agentCard.classList.add('active-pulse');
    agentName.innerText = "Routing...";
    agentStatus.innerText = "Analyzing Objective";
    jsonViewer.innerHTML = "Initializing CPS/1.0 PION Sequence...";

    try {
        const response = await fetch('/api/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ objective: input })
        });

        const data = await response.json();
        
        // UI Updates - Success State
        // Add a slight artificial delay for dramatic effect
        setTimeout(() => {
            const role = data.payload.agent_role || "Unknown Agent";
            agentName.innerText = role;
            document.querySelector('.agent-icon').innerText = role.charAt(0);
            agentStatus.innerText = "Execution Complete";
            
            // Format JSON beautifully
            jsonViewer.innerHTML = syntaxHighlight(JSON.stringify(data, null, 2));
            
            btn.disabled = false;
            btn.innerText = "Execute PION Protocol";
            agentCard.classList.remove('active-pulse');
        }, 800);

    } catch (error) {
        agentName.innerText = "Error";
        agentStatus.innerText = "Connection Failed";
        jsonViewer.innerHTML = "Error connecting to CHIMERA API Server.";
        btn.disabled = false;
        btn.innerText = "Execute PION Protocol";
        agentCard.classList.remove('active-pulse');
    }
});

// Simple JSON Syntax Highlighter
function syntaxHighlight(json) {
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        let color = '#a5b4fc'; // Default string color (blueish)
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                color = '#38bdf8'; // Key color
            } else {
                color = '#34d399'; // String value color
            }
        } else if (/true|false/.test(match)) {
            color = '#fbbf24'; // Boolean
        } else if (/null/.test(match)) {
            color = '#f87171'; // Null
        } else {
            color = '#c084fc'; // Number
        }
        return '<span style="color:' + color + ';">' + match + '</span>';
    });
}
