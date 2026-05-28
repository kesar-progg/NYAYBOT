ANALYTICS_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NyayBot — Analytics</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
  :root {
    --bg: #050508;
    --surface: #0d0d14;
    --card: #12121c;
    --border: #1e1e30;
    --accent: #6c63ff;
    --accent2: #ff6584;
    --green: #00f5a0;
    --amber: #ffb347;
    --red: #ff4d6d;
    --text: #e8e8f0;
    --muted: #6b6b8a;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: var(--bg); color: var(--text); font-family: "Syne", sans-serif; min-height: 100vh; }
  body::before {
    content: "";
    position: fixed; inset: 0;
    background-image:
      linear-gradient(rgba(108,99,255,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(108,99,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none; z-index: 0;
  }
  .wrapper { position: relative; z-index: 1; max-width: 1400px; margin: 0 auto; padding: 0 24px; }
  header {
    padding: 28px 0 20px;
    display: flex; align-items: center; justify-content: space-between;
    border-bottom: 1px solid var(--border); margin-bottom: 32px;
  }
  .logo { display: flex; align-items: center; gap: 12px; }
  .logo-icon {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
  }
  .logo h1 { font-size: 18px; font-weight: 800; background: linear-gradient(135deg, #fff, var(--accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .nav { display: flex; gap: 8px; }
  .nav a {
    padding: 8px 16px; border-radius: 8px; font-size: 13px;
    color: var(--muted); text-decoration: none; transition: all 0.2s;
    border: 1px solid transparent;
  }
  .nav a:hover { color: var(--text); border-color: var(--border); }
  .nav a.active { color: var(--accent); border-color: var(--accent); background: rgba(108,99,255,0.1); }

  /* Stats */
  .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 32px; }
  .stat {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 14px; padding: 20px 24px;
    position: relative; overflow: hidden;
  }
  .stat::after {
    content: attr(data-icon);
    position: absolute; right: 16px; top: 16px;
    font-size: 28px; opacity: 0.15;
  }
  .stat-label { font-size: 10px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.1em; font-family: "JetBrains Mono", monospace; margin-bottom: 8px; }
  .stat-val { font-size: 32px; font-weight: 800; }
  .stat-val.purple { background: linear-gradient(135deg, #fff, var(--accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .stat-val.red { background: linear-gradient(135deg, #fff, var(--red)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .stat-val.green { background: linear-gradient(135deg, #fff, var(--green)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .stat-val.amber { background: linear-gradient(135deg, #fff, var(--amber)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .stat-sub { font-size: 11px; color: var(--muted); margin-top: 4px; }

  /* Charts grid */
  .charts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
  .chart-wide { grid-column: 1 / -1; }

  .chart-card {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 16px; padding: 24px;
  }
  .chart-title {
    font-size: 13px; font-weight: 700; margin-bottom: 4px;
    color: var(--text);
  }
  .chart-sub { font-size: 11px; color: var(--muted); margin-bottom: 20px; font-family: "JetBrains Mono", monospace; }
  .chart-wrap { position: relative; height: 240px; }
  .chart-wrap-lg { position: relative; height: 200px; }

  /* Insight cards */
  .insights { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 32px; }
  .insight {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 14px; padding: 20px;
  }
  .insight-icon { font-size: 24px; margin-bottom: 10px; }
  .insight-title { font-size: 13px; font-weight: 700; margin-bottom: 6px; }
  .insight-text { font-size: 12px; color: var(--muted); line-height: 1.6; }
  .insight-val { font-size: 22px; font-weight: 800; margin: 8px 0 4px; }
  .insight-val.red { color: var(--red); }
  .insight-val.green { color: var(--green); }
  .insight-val.amber { color: var(--amber); }

  footer { text-align: center; padding: 32px 0 20px; color: var(--muted); font-size: 11px; font-family: "JetBrains Mono", monospace; border-top: 1px solid var(--border); margin-top: 20px; }
</style>
</head>
<body>
<div class="wrapper">
  <header>
    <div class="logo">
      <div class="logo-icon">⚖️</div>
      <div><h1>NyayBot</h1></div>
    </div>
    <nav class="nav">
      <a href="/">⚡ File Case</a>
      <a href="/tracker">📋 Case Tracker</a>
      <a href="/analytics" class="active">📊 Analytics</a>
    </nav>
  </header>

  <div class="stats">
    <div class="stat" data-icon="⚖️">
      <div class="stat-label">Total Cases</div>
      <div class="stat-val purple" id="s-total">—</div>
      <div class="stat-sub">All time</div>
    </div>
    <div class="stat" data-icon="🚨">
      <div class="stat-label">Critical Cases</div>
      <div class="stat-val red" id="s-critical">—</div>
      <div class="stat-sub">Needs immediate action</div>
    </div>
    <div class="stat" data-icon="⚡">
      <div class="stat-label">Fast Tracked</div>
      <div class="stat-val amber" id="s-escalated">—</div>
      <div class="stat-sub">Escalated cases</div>
    </div>
    <div class="stat" data-icon="✅">
      <div class="stat-label">Assigned</div>
      <div class="stat-val green" id="s-assigned">—</div>
      <div class="stat-sub">Judge assigned</div>
    </div>
  </div>

  <div class="insights" id="insights">
    <div class="insight">
      <div class="insight-icon">🔴</div>
      <div class="insight-title">Critical Rate</div>
      <div class="insight-val red" id="critical-rate">—</div>
      <div class="insight-text">Percentage of cases flagged as critical priority requiring immediate judicial attention</div>
    </div>
    <div class="insight">
      <div class="insight-icon">⚡</div>
      <div class="insight-title">Escalation Rate</div>
      <div class="insight-val amber" id="escalation-rate">—</div>
      <div class="insight-text">Cases automatically fast-tracked due to exceeding 90-day idle threshold</div>
    </div>
    <div class="insight">
      <div class="insight-icon">⚖️</div>
      <div class="insight-title">System Efficiency</div>
      <div class="insight-val green" id="efficiency">100%</div>
      <div class="insight-text">Cases processed successfully through NyayBot pipeline without manual intervention</div>
    </div>
  </div>

  <div class="charts-grid">
    <div class="chart-card">
      <div class="chart-title">Cases by Type</div>
      <div class="chart-sub">Distribution across court categories</div>
      <div class="chart-wrap">
        <canvas id="typeChart"></canvas>
      </div>
    </div>

    <div class="chart-card">
      <div class="chart-title">Priority Breakdown</div>
      <div class="chart-sub">Urgency classification of all cases</div>
      <div class="chart-wrap">
        <canvas id="priorityChart"></canvas>
      </div>
    </div>

    <div class="chart-card chart-wide">
      <div class="chart-title">Case Status Overview</div>
      <div class="chart-sub">Current pipeline stage distribution</div>
      <div class="chart-wrap-lg">
        <canvas id="statusChart"></canvas>
      </div>
    </div>
  </div>

  <footer>NYAYBOT v1.0 · ANALYTICS · UIPATH AGENTHACK 2026</footer>
</div>

<script>
const COLORS = {
  purple: 'rgba(108,99,255,0.8)',
  red: 'rgba(255,77,109,0.8)',
  amber: 'rgba(255,179,71,0.8)',
  green: 'rgba(0,245,160,0.8)',
  pink: 'rgba(255,101,132,0.8)',
  blue: 'rgba(56,189,248,0.8)',
  teal: 'rgba(45,212,191,0.8)',
};

const CHART_DEFAULTS = {
  plugins: {
    legend: {
      labels: { color: '#6b6b8a', font: { family: 'JetBrains Mono', size: 11 }, boxWidth: 12 }
    }
  },
  scales: {
    x: { ticks: { color: '#6b6b8a', font: { family: 'JetBrains Mono', size: 10 } }, grid: { color: '#1e1e30' } },
    y: { ticks: { color: '#6b6b8a', font: { family: 'JetBrains Mono', size: 10 } }, grid: { color: '#1e1e30' } }
  }
};

async function loadAnalytics() {
  const res = await fetch('/api/stats');
  const stats = await res.json();

  // Update stat cards
  document.getElementById('s-total').textContent = stats.total;
  document.getElementById('s-critical').textContent = stats.critical;
  document.getElementById('s-escalated').textContent = stats.escalated;
  document.getElementById('s-assigned').textContent = stats.assigned;

  // Insight calculations
  const total = stats.total || 1;
  const critRate = Math.round((stats.critical / total) * 100);
  const escRate = Math.round((stats.escalated / total) * 100);
  document.getElementById('critical-rate').textContent = critRate + '%';
  document.getElementById('escalation-rate').textContent = escRate + '%';

  // Case by type chart
  const typeLabels = stats.by_type.map(t => t.type);
  const typeCounts = stats.by_type.map(t => t.count);
  new Chart(document.getElementById('typeChart'), {
    type: 'doughnut',
    data: {
      labels: typeLabels,
      datasets: [{
        data: typeCounts,
        backgroundColor: [COLORS.purple, COLORS.red, COLORS.amber, COLORS.green, COLORS.pink, COLORS.blue],
        borderColor: '#12121c',
        borderWidth: 3
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { position: 'right', labels: { color: '#6b6b8a', font: { family: 'JetBrains Mono', size: 11 }, boxWidth: 12 } }
      }
    }
  });

  // Priority chart
  const priorityOrder = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'];
  const priorityColors = [COLORS.red, COLORS.amber, COLORS.purple, COLORS.green];
  const priorityMap = {};
  stats.by_priority.forEach(p => priorityMap[p.priority] = p.count);
  new Chart(document.getElementById('priorityChart'), {
    type: 'bar',
    data: {
      labels: priorityOrder,
      datasets: [{
        label: 'Cases',
        data: priorityOrder.map(p => priorityMap[p] || 0),
        backgroundColor: priorityColors,
        borderRadius: 6,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: CHART_DEFAULTS.scales
    }
  });

  // Status chart
  const statusLabels = stats.by_status.map(s => s.status);
  const statusCounts = stats.by_status.map(s => s.count);
  const statusColors = statusLabels.map(s => {
    if (s.includes('CRITICAL') || s.includes('ESCALAT') || s.includes('WARRANT')) return COLORS.red;
    if (s.includes('ASSIGNED') || s.includes('TRIAGED')) return COLORS.green;
    if (s.includes('PENDING') || s.includes('TRANSLATION')) return COLORS.amber;
    return COLORS.purple;
  });
  new Chart(document.getElementById('statusChart'), {
    type: 'bar',
    data: {
      labels: statusLabels,
      datasets: [{
        label: 'Cases',
        data: statusCounts,
        backgroundColor: statusColors,
        borderRadius: 6,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: { legend: { display: false } },
      scales: {
        x: CHART_DEFAULTS.scales.x,
        y: { ticks: { color: '#6b6b8a', font: { family: 'JetBrains Mono', size: 10 } }, grid: { color: '#1e1e30' } }
      }
    }
  });
}

loadAnalytics();
</script>
</body>
</html>
'''