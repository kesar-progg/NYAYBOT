from flask import Flask, request, jsonify, render_template_string
from main_pipeline import run_nyaybot
from database import save_case, get_all_cases, get_stats, get_case_by_id
from tracker import TRACKER_HTML
from analytics import ANALYTICS_HTML
from chat import chat_with_nyaybot, CHAT_HTML
from notifications import generate_notifications_from_case, get_notifications, get_unread_count, mark_all_read, NOTIFICATIONS_HTML
app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NyayBot — AI Judicial System</title>
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

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Syne', sans-serif;
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* Animated background grid */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(rgba(108,99,255,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(108,99,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
  }

  /* Glow orbs */
  .orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(120px);
    pointer-events: none;
    z-index: 0;
    animation: float 8s ease-in-out infinite;
  }
  .orb1 { width: 400px; height: 400px; background: rgba(108,99,255,0.12); top: -100px; left: -100px; }
  .orb2 { width: 300px; height: 300px; background: rgba(255,101,132,0.08); bottom: -50px; right: -50px; animation-delay: -4s; }

  @keyframes float {
    0%, 100% { transform: translateY(0px) scale(1); }
    50% { transform: translateY(-20px) scale(1.05); }
  }

  /* Layout */
  .wrapper { position: relative; z-index: 1; max-width: 1300px; margin: 0 auto; padding: 0 24px; }

  /* Header */
  header {
    padding: 32px 0 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border);
    margin-bottom: 40px;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 14px;
  }

  .logo-icon {
    width: 48px; height: 48px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    box-shadow: 0 0 30px rgba(108,99,255,0.4);
  }

  .logo-text h1 {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #fff 0%, var(--accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .logo-text p {
    font-size: 11px;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.05em;
  }

  .header-badge {
    display: flex; align-items: center; gap: 8px;
    background: rgba(0,245,160,0.08);
    border: 1px solid rgba(0,245,160,0.2);
    border-radius: 100px;
    padding: 8px 16px;
    font-size: 12px;
    color: var(--green);
    font-family: 'JetBrains Mono', monospace;
  }

  .pulse {
    width: 8px; height: 8px;
    background: var(--green);
    border-radius: 50%;
    animation: pulse 2s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.8); }
  }

  /* Stats bar */
  .stats-bar {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 40px;
  }

  .stat-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
  }

  .stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    opacity: 0;
    transition: opacity 0.3s;
  }

  .stat-card:hover { border-color: var(--accent); }
  .stat-card:hover::before { opacity: 1; }

  .stat-label {
    font-size: 11px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 8px;
  }

  .stat-value {
    font-size: 32px;
    font-weight: 800;
    background: linear-gradient(135deg, #fff, var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    counter-reset: none;
  }

  .stat-sub {
    font-size: 11px;
    color: var(--muted);
    margin-top: 4px;
  }

  /* Main grid */
  .main-grid {
    display: grid;
    grid-template-columns: 420px 1fr;
    gap: 24px;
    align-items: start;
  }

  /* Form card */
  .form-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 32px;
    position: sticky;
    top: 24px;
  }

  .card-title {
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .card-title span {
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .field { margin-bottom: 20px; }

  .field label {
    display: block;
    font-size: 11px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 8px;
  }

  .field input,
  .field select,
  .field textarea {
    width: 100%;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 16px;
    color: var(--text);
    font-family: 'Syne', sans-serif;
    font-size: 14px;
    transition: border-color 0.2s, box-shadow 0.2s;
    outline: none;
    appearance: none;
  }

  .field input:focus,
  .field select:focus,
  .field textarea:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(108,99,255,0.15);
  }

  .field textarea { resize: none; height: 90px; }

  /* Urgency slider */
  .urgency-wrap { position: relative; }

  .urgency-wrap input[type=range] {
    -webkit-appearance: none;
    width: 100%;
    height: 6px;
    background: linear-gradient(90deg, var(--green), var(--amber), var(--red));
    border-radius: 3px;
    outline: none;
    border: none;
    padding: 0;
    cursor: pointer;
  }

  .urgency-wrap input[type=range]::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 20px; height: 20px;
    background: white;
    border-radius: 50%;
    box-shadow: 0 0 10px rgba(108,99,255,0.5);
    cursor: pointer;
  }

  .urgency-labels {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    margin-top: 6px;
  }

  .urgency-val {
    text-align: center;
    font-size: 28px;
    font-weight: 800;
    color: var(--accent);
    margin-bottom: 8px;
    font-family: 'JetBrains Mono', monospace;
  }

  /* Checkboxes */
  .checks { display: flex; gap: 12px; }

  .check-item {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 10px 14px;
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 13px;
  }

  .check-item input { display: none; }

  .check-item.active {
    border-color: var(--accent);
    background: rgba(108,99,255,0.1);
    color: var(--accent);
  }

  /* Submit button */
  .submit-btn {
    width: 100%;
    padding: 16px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border: none;
    border-radius: 12px;
    color: white;
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.3s;
    position: relative;
    overflow: hidden;
    margin-top: 8px;
    letter-spacing: 0.02em;
  }

  .submit-btn::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, var(--accent2), var(--accent));
    opacity: 0;
    transition: opacity 0.3s;
  }

  .submit-btn:hover::before { opacity: 1; }
  .submit-btn:hover { transform: translateY(-1px); box-shadow: 0 8px 30px rgba(108,99,255,0.4); }
  .submit-btn:active { transform: translateY(0); }

  .submit-btn span { position: relative; z-index: 1; }

  /* Results panel */
  .results-panel { display: flex; flex-direction: column; gap: 20px; }

  .empty-state {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 60px;
    text-align: center;
    color: var(--muted);
  }

  .empty-icon { font-size: 48px; margin-bottom: 16px; opacity: 0.5; }
  .empty-text { font-size: 16px; font-weight: 600; margin-bottom: 8px; }
  .empty-sub { font-size: 13px; line-height: 1.6; }

  /* Result card */
  .result-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 20px;
    overflow: hidden;
    animation: slideIn 0.4s ease;
  }

  @keyframes slideIn {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .result-header {
    padding: 20px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border);
  }

  .result-id {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: var(--muted);
  }

  .priority-badge {
    padding: 6px 14px;
    border-radius: 100px;
    font-size: 12px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.05em;
  }

  .priority-CRITICAL { background: rgba(255,77,109,0.15); color: var(--red); border: 1px solid rgba(255,77,109,0.3); }
  .priority-HIGH { background: rgba(255,179,71,0.15); color: var(--amber); border: 1px solid rgba(255,179,71,0.3); }
  .priority-MEDIUM { background: rgba(108,99,255,0.15); color: var(--accent); border: 1px solid rgba(108,99,255,0.3); }
  .priority-LOW { background: rgba(0,245,160,0.15); color: var(--green); border: 1px solid rgba(0,245,160,0.3); }

  .result-body { padding: 24px; }

  .result-name {
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 4px;
  }

  .result-type {
    font-size: 13px;
    color: var(--muted);
    margin-bottom: 20px;
    font-family: 'JetBrains Mono', monospace;
  }

  .result-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 20px;
  }

  .result-field {
    background: var(--surface);
    border-radius: 10px;
    padding: 14px;
  }

  .result-field-label {
    font-size: 10px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 6px;
  }

  .result-field-value {
    font-size: 14px;
    font-weight: 600;
    color: var(--text);
  }

  /* Alert box */
  .alert {
    border-radius: 10px;
    padding: 14px 16px;
    font-size: 13px;
    margin-top: 12px;
    line-height: 1.6;
  }

  .alert-red { background: rgba(255,77,109,0.08); border: 1px solid rgba(255,77,109,0.2); color: #ff8fa3; }
  .alert-amber { background: rgba(255,179,71,0.08); border: 1px solid rgba(255,179,71,0.2); color: var(--amber); }
  .alert-green { background: rgba(0,245,160,0.08); border: 1px solid rgba(0,245,160,0.2); color: var(--green); }

  /* Pipeline stages */
  .pipeline {
    display: flex;
    align-items: center;
    gap: 0;
    margin-top: 20px;
    overflow-x: auto;
    padding-bottom: 4px;
  }

  .stage {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
    min-width: 70px;
  }

  .stage-dot {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px;
    margin-bottom: 6px;
    position: relative;
    z-index: 1;
  }

  .stage-dot.done { background: rgba(0,245,160,0.2); border: 2px solid var(--green); }
  .stage-dot.warn { background: rgba(255,179,71,0.2); border: 2px solid var(--amber); }
  .stage-dot.err { background: rgba(255,77,109,0.2); border: 2px solid var(--red); }

  .stage-line {
    flex: 1;
    height: 2px;
    background: var(--border);
    margin-top: -19px;
    position: relative;
    z-index: 0;
  }

  .stage-line.done { background: var(--green); }

  .stage-label {
    font-size: 9px;
    color: var(--muted);
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.04em;
    max-width: 64px;
  }

  /* Loading */
  .loading {
    display: none;
    text-align: center;
    padding: 40px;
    color: var(--muted);
  }

  .spinner {
    width: 40px; height: 40px;
    border: 3px solid var(--border);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin: 0 auto 16px;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  /* Footer */
  footer {
    text-align: center;
    padding: 40px 0 24px;
    color: var(--muted);
    font-size: 12px;
    font-family: 'JetBrains Mono', monospace;
    border-top: 1px solid var(--border);
    margin-top: 60px;
  }

  select option { background: #1a1a2e; }
</style>
</head>
<body>

<div class="orb orb1"></div>
<div class="orb orb2"></div>

<div class="wrapper">
  <header>
    <div class="logo">
      <div class="logo-icon">⚖️</div>
      <div class="logo-text">
        <h1>NyayBot</h1>
        <p>AI JUDICIAL CASE MANAGEMENT · INDIA</p>
      </div>
    </div>
    <div class="header-badge">
      <div class="pulse"></div>
      SYSTEM ONLINE
    </div>
  </header>

  <div class="stats-bar">
    <div class="stat-card">
      <div class="stat-label">Pending Cases</div>
      <div class="stat-value">40M+</div>
      <div class="stat-sub">Across Indian courts</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Avg Resolution Time</div>
      <div class="stat-value">10yr</div>
      <div class="stat-sub">Without NyayBot</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Cases Processed</div>
      <div class="stat-value" id="processed-count">0</div>
      <div class="stat-sub">This session</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Critical Escalations</div>
      <div class="stat-value" id="critical-count">0</div>
      <div class="stat-sub">Fast-tracked today</div>
    </div>
  </div>

  <div class="main-grid">
    <!-- FORM -->
    <div class="form-card">
      <div class="card-title">⚡ <span>File New Case</span></div>

      <div class="field">
        <label>Petitioner Name</label>
        <input type="text" id="name" placeholder="Full legal name" value="Rajesh Kumar">
      </div>

      <div class="field">
        <label>Case Type</label>
        <select id="case_type">
          <option>Civil</option>
          <option>Criminal</option>
          <option>Family</option>
          <option>Property</option>
          <option>Labour</option>
          <option>Consumer</option>
        </select>
      </div>

      <div class="field">
        <label>Case Description</label>
        <textarea id="description" placeholder="Describe the case...">Property dispute with neighbour over land boundary</textarea>
      </div>

      <div class="field">
        <label>Urgency Level</label>
        <div class="urgency-wrap">
          <div class="urgency-val" id="urgency-display">5</div>
          <input type="range" id="urgency" min="1" max="10" value="5"
                 oninput="document.getElementById('urgency-display').textContent = this.value">
          <div class="urgency-labels"><span>Low</span><span>Medium</span><span>Critical</span></div>
        </div>
      </div>

      <div class="field">
        <label>Petition Language</label>
        <select id="language">
          <option>English</option>
          <option>Hindi</option>
          <option>Tamil</option>
          <option>Telugu</option>
          <option>Marathi</option>
          <option>Bengali</option>
        </select>
      </div>

      <div class="field">
        <label>Special Conditions</label>
        <div class="checks">
          <label class="check-item" id="undertrial-label">
            <input type="checkbox" id="undertrial"
                   onchange="this.closest('.check-item').classList.toggle('active', this.checked)">
            🔒 Undertrial
          </label>
          <label class="check-item" id="fraud-label">
            <input type="checkbox" id="fraud_flag"
                   onchange="this.closest('.check-item').classList.toggle('active', this.checked)">
            🚨 Fraud Risk
          </label>
        </div>
      </div>

      <button class="submit-btn" onclick="fileCase()">
        <span>⚡ &nbsp;Process Case Through NyayBot</span>
      </button>
    </div>

    <!-- RESULTS -->
    <div class="results-panel" id="results-panel">
      <div class="empty-state" id="empty-state">
        <div class="empty-icon">⚖️</div>
        <div class="empty-text">No cases processed yet</div>
        <div class="empty-sub">Fill in the form and submit a case<br>to see NyayBot's AI pipeline in action</div>
      </div>
      <div class="loading" id="loading">
        <div class="spinner"></div>
        <div>Processing case through NyayBot pipeline...</div>
      </div>
    </div>
  </div>

  <footer>NYAYBOT v1.0 · BUILT FOR UIPATH AGENTHACK 2026 · JUSTICE THROUGH INTELLIGENCE</footer>
</div>

<script>
let processedCount = 0;
let criticalCount = 0;

async function fileCase() {
  const name = document.getElementById('name').value;
  const caseType = document.getElementById('case_type').value;
  const description = document.getElementById('description').value;
  const urgency = document.getElementById('urgency').value;
  const language = document.getElementById('language').value;
  const isUndertrial = document.getElementById('undertrial').checked;
  const isFraud = document.getElementById('fraud_flag').checked;

  if (!name || !description) { alert('Please fill in all required fields!'); return; }

  // Show loading
  document.getElementById('empty-state').style.display = 'none';
  document.getElementById('loading').style.display = 'block';

  try {
    const res = await fetch('/process_case', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name, case_type: caseType, description,
        urgency: parseInt(urgency), language,
        is_undertrial: isUndertrial,
        fraud_score: isFraud ? 0.85 : 0.1
      })
    });

    const data = await res.json();
    document.getElementById('loading').style.display = 'none';

    processedCount++;
    document.getElementById('processed-count').textContent = processedCount;
    if (data.priority === 'CRITICAL') {
      criticalCount++;
      document.getElementById('critical-count').textContent = criticalCount;
    }

    renderResult(data);
  } catch(e) {
    document.getElementById('loading').style.display = 'none';
    alert('Error processing case: ' + e.message);
  }
}

function getPriorityClass(p) {
  return 'priority-' + (p || 'LOW');
}

function getStageStatus(status, escalated) {
  const stages = [
    { label: 'FILED', icon: '📋' },
    { label: 'TRIAGED', icon: '🤖' },
    { label: 'CHECKED', icon: '🔍' },
    { label: 'ASSIGNED', icon: '👨‍⚖️' },
    { label: 'MONITORED', icon: '⏱️' },
    { label: 'REVIEW', icon: '👤' },
  ];

  const doneStatuses = ['FILED','TRIAGED','ASSIGNED','ESCALATED','URGENT_BAIL_REVIEW',
                        'FRAUD_SUSPECTED','INCOMPLETE','WARRANT_ISSUED','TRANSLATION_PENDING'];
  const allDone = doneStatuses.includes(status);

  return stages.map((s, i) => ({
    ...s,
    done: allDone,
    warn: escalated && i === 4
  }));
}

function renderResult(data) {
  const panel = document.getElementById('results-panel');

  const stages = getStageStatus(data.status, data.escalated);
  const stagesHTML = stages.map((s, i) => `
    <div class="stage">
      <div class="stage-dot ${s.warn ? 'warn' : 'done'}">${s.icon}</div>
      <div class="stage-label">${s.label}</div>
    </div>
    ${i < stages.length - 1 ? `<div class="stage-line done"></div>` : ''}
  `).join('');

  const alertHTML = data.exception ? `
    <div class="alert ${data.priority === 'CRITICAL' ? 'alert-red' : 'alert-amber'}">
      ⚠️ <strong>Exception:</strong> ${data.exception}<br>
      <strong>Action:</strong> ${data.action || 'Manual review required'}
    </div>
  ` : `<div class="alert alert-green">✅ All exception checks passed — case is clean</div>`;

  const escalationHTML = data.escalated ? `
    <div class="alert alert-red">
      🚨 <strong>Escalated to Fast Track:</strong> ${data.fast_track_court || 'Fast Track Court'}
    </div>
  ` : '';

  const card = document.createElement('div');
  card.className = 'result-card';
  card.innerHTML = `
    <div class="result-header">
      <div class="result-id">${data.case_id}</div>
      <div class="priority-badge ${getPriorityClass(data.priority)}">${data.priority || 'LOW'}</div>
    </div>
    <div class="result-body">
      <div class="result-name">${data.petitioner_name}</div>
      <div class="result-type">${data.case_type} Case · Filed ${data.filed_on}</div>
      <div class="result-grid">
        <div class="result-field">
          <div class="result-field-label">Status</div>
          <div class="result-field-value">${data.status}</div>
        </div>
        <div class="result-field">
          <div class="result-field-label">Assigned Court</div>
          <div class="result-field-value">${data.assigned_court}</div>
        </div>
        <div class="result-field">
          <div class="result-field-label">Judge</div>
          <div class="result-field-value">${data.assigned_judge || 'Pending'}</div>
        </div>
        <div class="result-field">
          <div class="result-field-label">Urgency Score</div>
          <div class="result-field-value">${data.urgency_score} / 10</div>
        </div>
      </div>
      <div class="pipeline">${stagesHTML}</div>
      ${alertHTML}
      ${escalationHTML}
    </div>
  `;

  // Insert after loading div
  const loading = document.getElementById('loading');
  panel.insertBefore(card, loading.nextSibling);
}
</script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/process_case', methods=['POST'])
def process_case():
    data = request.json
    params = {
        "submitted_docs": ["Petition", "Identity Proof", "Evidence Documents",
                           "FIR", "Witness Statement", "Marriage Certificate",
                           "Land Records"],
        "accused_found": True,
        "fraud_score": data.get("fraud_score", 0.1),
        "petition_language": data.get("language", "English"),
        "is_undertrial": data.get("is_undertrial", False),
        "days_in_custody": 220 if data.get("is_undertrial") else 0
    }

    case = run_nyaybot(
        data["name"],
        data["case_type"],
        data["description"],
        data["urgency"],
        params
    )

    
    save_case(case)
    generate_notifications_from_case(case)
    return jsonify(case)
@app.route('/tracker')
def tracker():
    cases = get_all_cases()
    return render_template_string(TRACKER_HTML, cases=cases)

@app.route('/api/stats')
def api_stats():
    return jsonify(get_stats())

@app.route('/analytics')
def analytics():
    return render_template_string(ANALYTICS_HTML)

@app.route('/chat')
def chat_page():
    return render_template_string(CHAT_HTML)

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.json
    messages = data.get('messages', [])
    response = chat_with_nyaybot(messages)
    return jsonify({'response': response})

@app.route('/notifications')
def notifications_page():
    return render_template_string(NOTIFICATIONS_HTML)

@app.route('/api/notifications')
def api_notifications():
    return jsonify(get_notifications())

@app.route('/api/notifications/unread')
def api_unread():
    return jsonify({'count': get_unread_count()})

@app.route('/api/notifications/read', methods=['POST'])
def api_mark_read():
    mark_all_read()
    return jsonify({'status': 'ok'})
if __name__ == '__main__':
    app.run(debug=True, port=5000)