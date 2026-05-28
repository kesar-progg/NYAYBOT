import sqlite3
from datetime import datetime

DB_NAME = "nyaybot.db"

def init_notifications():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            message TEXT,
            type TEXT,
            case_id TEXT,
            created_at TEXT,
            is_read INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_notification(title, message, notif_type, case_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO notifications (title, message, type, case_id, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, message, notif_type, case_id,
          datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_notifications(limit=20):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM notifications ORDER BY created_at DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_unread_count():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM notifications WHERE is_read=0')
    count = c.fetchone()[0]
    conn.close()
    return count

def mark_all_read():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('UPDATE notifications SET is_read=1')
    conn.commit()
    conn.close()

def generate_notifications_from_case(case):
    """Auto generate notifications based on case state"""
    case_id = case.get("case_id", "")
    name = case.get("petitioner_name", "Unknown")
    priority = case.get("priority", "")

    # Critical case
    if priority == "CRITICAL":
        add_notification(
            "🔴 Critical Case Filed",
            f"{name}'s case has been classified as CRITICAL priority and assigned to fast-track processing.",
            "critical", case_id
        )

    # Escalated
    if case.get("escalated"):
        add_notification(
            "⚡ Case Escalated to Fast Track",
            f"{name}'s case has been idle too long and escalated to {case.get('fast_track_court', 'Fast Track Court')}.",
            "escalation", case_id
        )

    # Warrant issued
    if case.get("warrant_issued"):
        add_notification(
            "🚨 Warrant Issued",
            f"Non-bailable warrant issued in {name}'s case — accused not found at given address.",
            "warrant", case_id
        )

    # Fraud suspected
    if case.get("status") == "FRAUD_SUSPECTED":
        add_notification(
            "⚠️ Fraud Suspected",
            f"High fraud probability detected in {name}'s filing. Case flagged for human review.",
            "fraud", case_id
        )

    # Undertrial
    if case.get("undertrial") and case.get("days_in_custody", 0) > 180:
        add_notification(
            "🔒 Undertrial Alert",
            f"{name}'s case involves an undertrial prisoner in custody for {case.get('days_in_custody')} days — mandatory bail review triggered.",
            "undertrial", case_id
        )

    # Translation needed
    if case.get("status") == "TRANSLATION_PENDING":
        add_notification(
            "🌐 Translation Required",
            f"{name}'s petition filed in {case.get('original_language', 'regional language')} — certified translation requested.",
            "translation", case_id
        )

    # Missing documents
    if case.get("missing_documents"):
        docs = ", ".join(case["missing_documents"])
        add_notification(
            "📋 Incomplete Filing",
            f"{name}'s case is missing: {docs}. Petitioner notified to submit within 30 days.",
            "incomplete", case_id
        )

    # Judge assigned successfully
    if case.get("assigned_judge") and priority not in ["CRITICAL"]:
        add_notification(
            "✅ Judge Assigned",
            f"{name}'s case assigned to {case['assigned_judge']} at {case.get('assigned_court', 'court')}.",
            "assigned", case_id
        )

# Initialize on import
init_notifications()


NOTIFICATIONS_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NyayBot — Notifications</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #050508; --surface: #0d0d14; --card: #12121c;
    --border: #1e1e30; --accent: #6c63ff; --accent2: #ff6584;
    --green: #00f5a0; --amber: #ffb347; --red: #ff4d6d;
    --text: #e8e8f0; --muted: #6b6b8a;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: var(--bg); color: var(--text); font-family: "Syne", sans-serif; min-height: 100vh; }
  body::before {
    content: ""; position: fixed; inset: 0;
    background-image: linear-gradient(rgba(108,99,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(108,99,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px; pointer-events: none; z-index: 0;
  }
  .wrapper { position: relative; z-index: 1; max-width: 900px; margin: 0 auto; padding: 0 24px; }
  header { padding: 28px 0 20px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border); margin-bottom: 32px; }
  .logo { display: flex; align-items: center; gap: 12px; }
  .logo-icon { width: 40px; height: 40px; background: linear-gradient(135deg, var(--accent), var(--accent2)); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 18px; }
  .logo h1 { font-size: 18px; font-weight: 800; background: linear-gradient(135deg, #fff, var(--accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .nav { display: flex; gap: 8px; }
  .nav a { padding: 8px 16px; border-radius: 8px; font-size: 13px; color: var(--muted); text-decoration: none; transition: all 0.2s; border: 1px solid transparent; position: relative; }
  .nav a:hover { color: var(--text); border-color: var(--border); }
  .nav a.active { color: var(--accent); border-color: var(--accent); background: rgba(108,99,255,0.1); }
  .badge { position: absolute; top: 4px; right: 4px; width: 8px; height: 8px; background: var(--red); border-radius: 50%; }

  .page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; }
  .page-title { font-size: 24px; font-weight: 800; background: linear-gradient(135deg, #fff, var(--accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .mark-read-btn { padding: 8px 16px; background: var(--card); border: 1px solid var(--border); border-radius: 8px; color: var(--muted); font-family: "Syne", sans-serif; font-size: 13px; cursor: pointer; transition: all 0.2s; }
  .mark-read-btn:hover { color: var(--accent); border-color: var(--accent); }

  .notif-list { display: flex; flex-direction: column; gap: 12px; }

  .notif-card {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 14px; padding: 18px 20px;
    display: flex; gap: 16px; align-items: flex-start;
    transition: border-color 0.2s;
    animation: slideIn 0.3s ease;
  }

  @keyframes slideIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .notif-card.unread { border-color: rgba(108,99,255,0.3); }
  .notif-card:hover { border-color: var(--accent); }

  .notif-icon {
    width: 42px; height: 42px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0;
  }

  .icon-critical { background: rgba(255,77,109,0.15); }
  .icon-escalation { background: rgba(255,179,71,0.15); }
  .icon-warrant { background: rgba(255,77,109,0.15); }
  .icon-fraud { background: rgba(255,179,71,0.15); }
  .icon-undertrial { background: rgba(255,77,109,0.15); }
  .icon-translation { background: rgba(108,99,255,0.15); }
  .icon-incomplete { background: rgba(255,179,71,0.15); }
  .icon-assigned { background: rgba(0,245,160,0.15); }

  .notif-body { flex: 1; }
  .notif-title { font-size: 14px; font-weight: 700; margin-bottom: 4px; }
  .notif-message { font-size: 13px; color: var(--muted); line-height: 1.6; margin-bottom: 8px; }
  .notif-meta { display: flex; gap: 12px; align-items: center; }
  .notif-time { font-size: 11px; color: var(--muted); font-family: "JetBrains Mono", monospace; }
  .notif-case { font-size: 11px; color: var(--accent); font-family: "JetBrains Mono", monospace; }
  .unread-dot { width: 6px; height: 6px; background: var(--accent); border-radius: 50%; margin-left: auto; flex-shrink: 0; margin-top: 6px; }

  .empty { text-align: center; padding: 80px; color: var(--muted); }
  .empty-icon { font-size: 48px; margin-bottom: 16px; opacity: 0.3; }
  .empty-text { font-size: 16px; font-weight: 600; margin-bottom: 8px; }
  .empty-sub { font-size: 13px; }

  .live-badge {
    display: flex; align-items: center; gap: 6px;
    background: rgba(0,245,160,0.08); border: 1px solid rgba(0,245,160,0.2);
    border-radius: 100px; padding: 6px 12px;
    font-size: 11px; color: var(--green);
    font-family: "JetBrains Mono", monospace;
  }
  .pulse { width: 6px; height: 6px; background: var(--green); border-radius: 50%; animation: pulse 2s ease-in-out infinite; }
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

  footer { text-align: center; padding: 40px 0 24px; color: var(--muted); font-size: 11px; font-family: "JetBrains Mono", monospace; border-top: 1px solid var(--border); margin-top: 40px; }
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
      <a href="/analytics">📊 Analytics</a>
      <a href="/chat">💬 AI Chat</a>
      <a href="/notifications" class="active">🔔 Alerts <span class="badge" id="nav-badge" style="display:none"></span></a>
    </nav>
  </header>

  <div class="page-header">
    <div class="page-title">🔔 Live Alerts</div>
    <div style="display:flex; gap:12px; align-items:center;">
      <div class="live-badge"><div class="pulse"></div> LIVE</div>
      <button class="mark-read-btn" onclick="markAllRead()">Mark all read</button>
    </div>
  </div>

  <div class="notif-list" id="notif-list">
    <div class="empty">
      <div class="empty-icon">🔔</div>
      <div class="empty-text">No alerts yet</div>
      <div class="empty-sub">File a case to see live notifications appear here</div>
    </div>
  </div>

  <footer>NYAYBOT v1.0 · LIVE ALERTS · UIPATH AGENTHACK 2026</footer>
</div>

<script>
const TYPE_ICONS = {
  critical: '🔴',
  escalation: '⚡',
  warrant: '🚨',
  fraud: '⚠️',
  undertrial: '🔒',
  translation: '🌐',
  incomplete: '📋',
  assigned: '✅'
};

async function loadNotifications() {
  const res = await fetch('/api/notifications');
  const notifs = await res.json();
  const list = document.getElementById('notif-list');

  if (notifs.length === 0) {
    list.innerHTML = `
      <div class="empty">
        <div class="empty-icon">🔔</div>
        <div class="empty-text">No alerts yet</div>
        <div class="empty-sub">File a case to see live notifications appear here</div>
      </div>`;
    return;
  }

  list.innerHTML = notifs.map(n => `
    <div class="notif-card ${n.is_read ? '' : 'unread'}">
      <div class="notif-icon icon-${n.type}">${TYPE_ICONS[n.type] || '🔔'}</div>
      <div class="notif-body">
        <div class="notif-title">${n.title}</div>
        <div class="notif-message">${n.message}</div>
        <div class="notif-meta">
          <span class="notif-time">${n.created_at}</span>
          <span class="notif-case">${n.case_id}</span>
        </div>
      </div>
      ${n.is_read ? '' : '<div class="unread-dot"></div>'}
    </div>
  `).join('');
}

async function markAllRead() {
  await fetch('/api/notifications/read', { method: 'POST' });
  loadNotifications();
}

async function updateUnreadCount() {
  const res = await fetch('/api/notifications/unread');
  const data = await res.json();
  const badge = document.getElementById('nav-badge');
  if (data.count > 0) {
    badge.style.display = 'block';
  } else {
    badge.style.display = 'none';
  }
}

// Poll every 3 seconds for live updates
loadNotifications();
setInterval(() => {
  loadNotifications();
  updateUnreadCount();
}, 3000);
</script>
</body>
</html>
'''