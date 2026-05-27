TRACKER_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NyayBot — Case Tracker</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
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
  .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 28px; }
  .stat {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 14px; padding: 18px 20px;
  }
  .stat-label { font-size: 10px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.1em; font-family: "JetBrains Mono", monospace; margin-bottom: 6px; }
  .stat-val { font-size: 28px; font-weight: 800; background: linear-gradient(135deg, #fff, var(--accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

  /* Controls */
  .controls {
    display: flex; gap: 12px; margin-bottom: 20px; align-items: center; flex-wrap: wrap;
  }
  .search-wrap { flex: 1; min-width: 200px; position: relative; }
  .search-wrap input {
    width: 100%; background: var(--card); border: 1px solid var(--border);
    border-radius: 10px; padding: 10px 16px 10px 40px;
    color: var(--text); font-family: "Syne", sans-serif; font-size: 14px;
    outline: none; transition: border-color 0.2s;
  }
  .search-wrap input:focus { border-color: var(--accent); }
  .search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--muted); font-size: 14px; }
  .filter-btn {
    padding: 10px 16px; background: var(--card); border: 1px solid var(--border);
    border-radius: 10px; color: var(--muted); font-family: "Syne", sans-serif;
    font-size: 13px; cursor: pointer; transition: all 0.2s;
  }
  .filter-btn:hover, .filter-btn.active { color: var(--accent); border-color: var(--accent); background: rgba(108,99,255,0.1); }
  select.filter-btn { appearance: none; padding-right: 32px; }

  /* Table */
  .table-wrap {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 16px; overflow: hidden;
  }
  table { width: 100%; border-collapse: collapse; }
  thead { background: var(--surface); }
  th {
    padding: 14px 20px; text-align: left;
    font-size: 10px; color: var(--muted);
    text-transform: uppercase; letter-spacing: 0.1em;
    font-family: "JetBrains Mono", monospace;
    border-bottom: 1px solid var(--border);
    cursor: pointer; user-select: none;
  }
  th:hover { color: var(--text); }
  td { padding: 14px 20px; font-size: 13px; border-bottom: 1px solid var(--border); vertical-align: middle; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: rgba(108,99,255,0.04); }

  .case-id { font-family: "JetBrains Mono", monospace; font-size: 11px; color: var(--muted); }
  .petitioner { font-weight: 600; color: var(--text); }
  .case-type { font-size: 12px; color: var(--muted); }

  .badge {
    display: inline-block; padding: 4px 10px;
    border-radius: 100px; font-size: 11px; font-weight: 600;
    font-family: "JetBrains Mono", monospace;
  }
  .badge-CRITICAL { background: rgba(255,77,109,0.15); color: var(--red); border: 1px solid rgba(255,77,109,0.3); }
  .badge-HIGH { background: rgba(255,179,71,0.15); color: var(--amber); border: 1px solid rgba(255,179,71,0.3); }
  .badge-MEDIUM { background: rgba(108,99,255,0.15); color: var(--accent); border: 1px solid rgba(108,99,255,0.3); }
  .badge-LOW { background: rgba(0,245,160,0.15); color: var(--green); border: 1px solid rgba(0,245,160,0.3); }
  .badge-status { background: rgba(108,99,255,0.1); color: var(--accent); border: 1px solid rgba(108,99,255,0.2); }
  .badge-escalated { background: rgba(255,77,109,0.1); color: var(--red); border: 1px solid rgba(255,77,109,0.2); }

  .judge-name { font-size: 12px; color: var(--text); }
  .no-judge { font-size: 12px; color: var(--muted); font-style: italic; }

  .empty {
    text-align: center; padding: 60px; color: var(--muted);
  }
  .empty-icon { font-size: 40px; margin-bottom: 12px; opacity: 0.4; }

  footer { text-align: center; padding: 32px 0 20px; color: var(--muted); font-size: 11px; font-family: "JetBrains Mono", monospace; border-top: 1px solid var(--border); margin-top: 40px; }
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
      <a href="/tracker" class="active">📋 Case Tracker</a>
      <a href="/analytics">📊 Analytics</a>
    </nav>
  </header>

  <div class="stats" id="stats">
    <div class="stat"><div class="stat-label">Total Cases</div><div class="stat-val" id="s-total">—</div></div>
    <div class="stat"><div class="stat-label">Critical</div><div class="stat-val" id="s-critical">—</div></div>
    <div class="stat"><div class="stat-label">Escalated</div><div class="stat-val" id="s-escalated">—</div></div>
    <div class="stat"><div class="stat-label">Assigned</div><div class="stat-val" id="s-assigned">—</div></div>
  </div>

  <div class="controls">
    <div class="search-wrap">
      <span class="search-icon">🔍</span>
      <input type="text" id="search" placeholder="Search by name, case ID, judge..." oninput="filterTable()">
    </div>
    <select class="filter-btn" id="priority-filter" onchange="filterTable()">
      <option value="">All Priorities</option>
      <option value="CRITICAL">Critical</option>
      <option value="HIGH">High</option>
      <option value="MEDIUM">Medium</option>
      <option value="LOW">Low</option>
    </select>
    <select class="filter-btn" id="type-filter" onchange="filterTable()">
      <option value="">All Types</option>
      <option value="Civil">Civil</option>
      <option value="Criminal">Criminal</option>
      <option value="Family">Family</option>
      <option value="Property">Property</option>
      <option value="Labour">Labour</option>
      <option value="Consumer">Consumer</option>
    </select>
    <select class="filter-btn" id="status-filter" onchange="filterTable()">
      <option value="">All Statuses</option>
      <option value="ASSIGNED">Assigned</option>
      <option value="ESCALATED">Escalated</option>
      <option value="CRITICAL">Critical</option>
      <option value="INCOMPLETE">Incomplete</option>
      <option value="WARRANT_ISSUED">Warrant Issued</option>
    </select>
  </div>

  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Case ID</th>
          <th>Petitioner</th>
          <th>Type</th>
          <th>Priority</th>
          <th>Status</th>
          <th>Court</th>
          <th>Judge</th>
          <th>Filed On</th>
          <th>Escalated</th>
        </tr>
      </thead>
      <tbody id="cases-tbody">
        {% if cases %}
          {% for c in cases %}
          <tr class="case-row"
              data-name="{{ c.petitioner_name }}"
              data-id="{{ c.case_id }}"
              data-judge="{{ c.assigned_judge or '' }}"
              data-priority="{{ c.priority or '' }}"
              data-type="{{ c.case_type or '' }}"
              data-status="{{ c.status or '' }}">
            <td><span class="case-id">{{ c.case_id }}</span></td>
            <td><span class="petitioner">{{ c.petitioner_name }}</span></td>
            <td><span class="case-type">{{ c.case_type }}</span></td>
            <td><span class="badge badge-{{ c.priority or 'LOW' }}">{{ c.priority or 'LOW' }}</span></td>
            <td><span class="badge badge-status">{{ c.status }}</span></td>
            <td style="font-size:12px; color:var(--muted);">{{ c.assigned_court }}</td>
            <td>
              {% if c.assigned_judge %}
                <span class="judge-name">{{ c.assigned_judge }}</span>
              {% else %}
                <span class="no-judge">Pending</span>
              {% endif %}
            </td>
            <td style="font-size:11px; font-family:'JetBrains Mono',monospace; color:var(--muted);">{{ c.filed_on }}</td>
            <td>
              {% if c.escalated %}
                <span class="badge badge-escalated">⚠️ YES</span>
              {% else %}
                <span style="color:var(--muted); font-size:12px;">—</span>
              {% endif %}
            </td>
          </tr>
          {% endfor %}
        {% else %}
          <tr><td colspan="9"><div class="empty"><div class="empty-icon">📭</div>No cases found. File your first case!</div></td></tr>
        {% endif %}
      </tbody>
    </table>
  </div>
  <footer>NYAYBOT v1.0 · CASE TRACKER · UIPATH AGENTHACK 2026</footer>
</div>

<script>
async function loadStats() {
  const res = await fetch('/api/stats');
  const s = await res.json();
  document.getElementById('s-total').textContent = s.total;
  document.getElementById('s-critical').textContent = s.critical;
  document.getElementById('s-escalated').textContent = s.escalated;
  document.getElementById('s-assigned').textContent = s.assigned;
}

function filterTable() {
  const search = document.getElementById('search').value.toLowerCase();
  const priority = document.getElementById('priority-filter').value;
  const type = document.getElementById('type-filter').value;
  const status = document.getElementById('status-filter').value;
  const rows = document.querySelectorAll('.case-row');
  rows.forEach(row => {
    const name = row.dataset.name.toLowerCase();
    const id = row.dataset.id.toLowerCase();
    const judge = row.dataset.judge.toLowerCase();
    const matchSearch = !search || name.includes(search) || id.includes(search) || judge.includes(search);
    const matchPriority = !priority || row.dataset.priority === priority;
    const matchType = !type || row.dataset.type === type;
    const matchStatus = !status || row.dataset.status === status;
    row.style.display = matchSearch && matchPriority && matchType && matchStatus ? '' : 'none';
  });
}

loadStats();
</script>
</body>
</html>
'''