// Navigation
const navLinks = document.querySelectorAll('.nav-link');
const views = document.querySelectorAll('.view');

navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const target = link.getAttribute('href').slice(1);
        
        // Update active nav link
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        
        // Update active view
        views.forEach(v => v.classList.remove('active'));
        document.getElementById(target).classList.add('active');
        
        // Load view-specific data
        if (target === 'logs') loadLogs();
        if (target === 'rules') loadRules();
    });
});

// Refresh stats
function refreshStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            document.getElementById('total-processed').textContent = data.total_emails_processed;
            document.getElementById('replies-sent').textContent = data.auto_replies_sent;
            document.getElementById('forwarded').textContent = data.emails_forwarded;
            document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
        })
        .catch(error => console.error('Error:', error));
    
    fetch('/api/unread-count')
        .then(response => response.json())
        .then(data => {
            document.getElementById('unread').textContent = data.unread_count;
        })
        .catch(error => console.error('Error:', error));
}

// Load logs
function loadLogs() {
    fetch('/api/logs?limit=50')
        .then(response => response.json())
        .then(logs => {
            const tbody = document.getElementById('logs-tbody');
            tbody.innerHTML = '';
            
            logs.forEach(log => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${log.from_email}</td>
                    <td>${log.subject}</td>
                    <td>${log.category}</td>
                    <td>${log.action}</td>
                    <td>${new Date(log.timestamp).toLocaleString()}</td>
                    <td>${log.rule}</td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('logs-tbody').innerHTML = '<tr><td colspan="6" class="loading">Error loading logs</td></tr>';
        });
}

// Load rules
function loadRules() {
    fetch('/api/rules')
        .then(response => response.json())
        .then(rules => {
            const rulesList = document.getElementById('rules-list');
            rulesList.innerHTML = '';
            
            rules.forEach(rule => {
                const ruleDiv = document.createElement('div');
                ruleDiv.className = 'rule-item';
                ruleDiv.innerHTML = `
                    <div>
                        <div class="rule-name">${rule.name}</div>
                        <div class="rule-status">Action: ${rule.action} | Keywords: ${rule.conditions.keywords.join(', ')}</div>
                    </div>
                    <label class="rule-toggle">
                        <input type="checkbox" ${rule.active ? 'checked' : ''} onchange="updateRuleStatus(${rule.rule_id}, this.checked)">
                        Active
                    </label>
                `;
                rulesList.appendChild(ruleDiv);
            });
        })
        .catch(error => console.error('Error:', error));
}

// Update rule status
function updateRuleStatus(ruleId, active) {
    fetch(`/api/rules/${ruleId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ active: active })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Rule updated:', data);
        loadRules();
    })
    .catch(error => console.error('Error:', error));
}

// Bot controls
function startBot() {
    alert('Bot would start (not implemented in this demo)');
}

function stopBot() {
    alert('Bot would stop (not implemented in this demo)');
}

function addRule() {
    alert('Add rule dialog would open (not implemented in this demo)');
}

function saveSettings() {
    alert('Settings saved (not implemented in this demo)');
}

// Auto-refresh on load
window.addEventListener('load', () => {
    refreshStats();
    setInterval(refreshStats, 30000); // Refresh every 30 seconds
});
