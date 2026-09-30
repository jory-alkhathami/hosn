let riskChart;
let journeyHistory = [10, 12, 15, 14, 11];

document.addEventListener("DOMContentLoaded", function () {
    initChart();
});

function initChart() {
    const ctx = document.getElementById('riskChart').getContext('2d');
    
    // Gradient fill for chart
    let gradient = ctx.createLinearGradient(0, 0, 0, 200);
    gradient.addColorStop(0, 'rgba(181, 156, 174, 0.4)');
    gradient.addColorStop(1, 'rgba(181, 156, 174, 0.0)');

    riskChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['خطوة 1', 'خطوة 2', 'خطوة 3', 'خطوة 4', 'خطوة 5'],
            datasets: [{
                label: 'مستوى المخاطرة (%)',
                data: journeyHistory,
                borderColor: '#B59CAE',
                borderWidth: 3,
                backgroundColor: gradient,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#E2D7E0'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { min: 0, max: 100, grid: { color: 'rgba(181, 156, 174, 0.1)' }, ticks: { color: '#A396A1' } },
                x: { grid: { color: 'rgba(181, 156, 174, 0.1)' }, ticks: { color: '#A396A1' } }
            },
            plugins: { legend: { labels: { color: '#E2D7E0', font: { family: 'Tajawal' } } } }
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

    let colorStyle = '#B59CAE';
    let bgBadge = 'bg-mauve-badge';

    if (score >= 75) {
        colorStyle = '#E65C5C';
        bgBadge = 'bg-danger text-white';
    } else if (score >= 45) {
        colorStyle = '#E6A15C';
        bgBadge = 'bg-warning text-dark';
    }

    scoreDisplay.style.color = colorStyle;
    badge.className = `badge ${bgBadge} px-3 py-2 fs-6`;
    badge.innerText = `${data.risk_level} RISK`;
    recBox.innerText = data.recommendation;

    factorsList.innerHTML = '';
    if (data.risk_factors.length === 0) {
        factorsList.innerHTML = '<div class="text-mauve"><i class="bi bi-check-circle-fill me-1"></i> لا توجد مؤشرات خطر. السلوك اعتيادي.</div>';
    } else {
        data.risk_factors.forEach(f => {
            factorsList.innerHTML += `
                <div class="alert alert-dark border-secondary py-2 px-3 mb-2 d-flex justify-content-between align-items-center rounded-3">
                    <span class="small">${f.signal}</span>
                    <span class="badge bg-danger">${f.impact}</span>
                </div>
            `;
        });
    }

    journeyHistory.push(score);
    if (journeyHistory.length > 7) journeyHistory.shift();
    
    riskChart.data.datasets[0].data = journeyHistory;
    riskChart.data.datasets[0].borderColor = colorStyle;
    riskChart.update();

    appendLog(`[RESPONSE]: النتيجة: ${score}% | القرار: ${data.action_code}`);
}

function appendLog(msg) {
    const logBox = document.getElementById('auditLog');
    const time = new Date().toLocaleTimeString('ar-SA');
    logBox.innerHTML += `<div>[${time}] ${msg}</div>`;
    logBox.scrollTop = logBox.scrollHeight;
}
