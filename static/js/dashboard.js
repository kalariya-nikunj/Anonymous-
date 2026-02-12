document.addEventListener('DOMContentLoaded', function () {
    const scanBtn = document.getElementById('scanBtn');
    const urlInput = document.getElementById('urlInput');
    const resultSection = document.getElementById('resultSection');

    // Initial Load Stats
    loadStats();

    scanBtn.addEventListener('click', async () => {
        const url = urlInput.value.trim();
        if (!url) return alert("Please enter a URL");

        // UI Loading State
        toggleLoading(true);

        try {
            const response = await fetch('/api/scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: url })
            });
            const data = await response.json();

            displayResults(data);
            loadStats(); // Update charts
        } catch (error) {
            console.error("Scan error:", error);
        } finally {
            toggleLoading(false);
        }
    });

    function toggleLoading(isLoading) {
        document.getElementById('btnText').classList.toggle('d-none', isLoading);
        document.getElementById('btnLoader').classList.toggle('d-none', !isLoading);
        scanBtn.disabled = isLoading;
    }

    function displayResults(data) {
        resultSection.classList.remove('d-none');
        document.getElementById('riskScoreText').innerText = data.risk_score + "/100";
        document.getElementById('recommendationText').innerText = data.recommendation;

        const levelBadge = document.getElementById('riskLevelText');
        levelBadge.innerText = data.status.toUpperCase();
        levelBadge.className = 'badge rounded-pill px-3 py-2 mt-2 ' +
            (data.risk_score > 70 ? 'bg-danger' : data.risk_score > 40 ? 'bg-warning text-dark' : 'bg-success');

        // Draw Gauge
        updateGauge(data.risk_score);

        // Populate 6-Layer Grid
        const grid = document.getElementById('layerGrid');
        grid.innerHTML = '';
        data.layers.forEach(layer => {
            const colorClass = layer.status === 'Safe' ? 'text-success' : 'text-danger';
            const icon = layer.status === 'Safe' ? 'bi-check-circle-fill' : 'bi-exclamation-triangle-fill';

            grid.innerHTML += `
                <div class="col-md-4">
                    <div class="card border-0 shadow-sm p-3 text-center h-100">
                        <i class="bi ${icon} ${colorClass} mb-2 fs-4"></i>
                        <h6 class="fw-bold mb-1">${layer.name}</h6>
                        <p class="text-muted small mb-0">${layer.val}</p>
                    </div>
                </div>
            `;
        });
    }

    let gaugeChart;
    function updateGauge(score) {
        const ctx = document.getElementById('riskGauge').getContext('2d');
        if (gaugeChart) gaugeChart.destroy();

        const color = score > 70 ? '#dc3545' : score > 40 ? '#ffc107' : '#198754';

        gaugeChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [score, 100 - score],
                    backgroundColor: [color, '#e9ecef'],
                    circumference: 180,
                    rotation: 270,
                    borderWidth: 0,
                    cutout: '80%'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: { enabled: false } }
            }
        });
    }

    async function loadStats() {
        const res = await fetch('/api/stats');
        const data = await res.json();

        document.getElementById('healthVal').innerText = data.stats.system_health + "%";
        document.getElementById('statThreats').innerText = data.stats.threats_detected;
        document.getElementById('statBar').style.width = data.stats.system_health + "%";

        initTrendsChart(data.chart_data);
    }
});