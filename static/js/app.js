let riskChart;
let journeyHistory = [10, 12, 15, 14, 11];

document.addEventListener("DOMContentLoaded", function () {
    initChart();
});

function initChart() {
    const ctx = document.getElementById('riskChart').getContext('2d');
    riskChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['خطوة 1', 'خطوة 2', 'خطوة 3', 'خطوة 4', 'خطوة 5'],
            datasets: [{
                label: 'مستوى المخاطرة (%)',
                data: journeyHistory,
                borderColor: '#198754',
                backgroundColor: 'rgba(25, 135, 84, 0.2)',
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { min: 0, max: 100, grid: { color: '#333' } },
                x: { grid: { color: '#333' } }
            },
            plugins: { legend: { labels: { color: '#fff' } } }
        }
    });
}

function runSimulation(type) {
    appendLog(`[REQUEST]: إرسال طلب محاكاة نوع: ${type}`);
    
    fetch(`/api/simulate/${type}`)
        .then(response => response.json())
        .then(data => {
            updateDashboard(data);
        })
        .catch(err => {
            appendLog(`[ERROR]: فشل الاتصال بالسيرفر: ${err}`);
        });
}

function updateDashboard(data) {
    const score = data.risk_score;
    const scoreDisplay = document.getElementById('riskScoreDisplay');
    const badge = document.getElementById('riskBadge');
    const recBox = document.getElementById('recommendationBox');
    const factorsList = document.getElementById('riskFactorsList');

    scoreDisplay.innerText = `${score}%`;

    let colorClass = 'text-success';
    let bgBadge = 'bg-success';
    let borderColor = '#198754';

    if (score >= 75) {
        colorClass = 'text-danger';
        bgBadge = 'bg-danger';
        borderColor = '#dc3545';
    } else if (score >= 45) {
        colorClass = 'text-warning';
        bgBadge = 'bg-warning text-dark';
        borderColor = '#ffc107';
    }

    scoreDisplay.className = `display-1 fw-bold ${colorClass}`;
    badge.className = `badge ${bgBadge} fs-6 mt-2`;
    badge.innerText = `${data.risk_level} RISK`;
    recBox.innerText = data.recommendation;

    factorsList.innerHTML = '';
    if (data.risk_factors.length === 0) {
        factorsList.innerHTML = '<div class="text-success"><i class="bi bi-check-circle-fill"></i> لا توجد مؤشرات خطر. السلوك اعتيادي.</div>';
    } else {
        data.risk_factors.forEach(f => {
            factorsList.innerHTML += `
                <div class="alert alert-dark border-secondary py-1 px-2 mb-1 d-flex justify-content-between align-items-center">
                    <span>${f.signal}</span>
                    <span class="badge bg-danger">${f.impact}</span>
                </div>
            `;
        });
    }

    journeyHistory.push(score);
    if (journeyHistory.length > 7) journeyHistory.shift();
    
    riskChart.data.datasets[0].data = journeyHistory;
    riskChart.data.datasets[0].borderColor = borderColor;
    riskChart.data.datasets[0].backgroundColor = `${borderColor}33`;
    riskChart.update();

    appendLog(`[RESPONSE]: النتيجة: ${score}% | القرار: ${data.action_code}`);
}

function appendLog(msg) {
    const logBox = document.getElementById('auditLog');
    const time = new Date().toLocaleTimeString('ar-SA');
    logBox.innerHTML += `<div>[${time}] ${msg}</div>`;
    logBox.scrollTop = logBox.scrollHeight;
}
