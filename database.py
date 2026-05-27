import sqlite3
import json
from datetime import datetime

DB_NAME = "nyaybot.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT UNIQUE,
            petitioner_name TEXT,
            case_type TEXT,
            description TEXT,
            priority TEXT,
            status TEXT,
            assigned_court TEXT,
            assigned_judge TEXT,
            urgency_score INTEGER,
            escalated INTEGER DEFAULT 0,
            fast_track_court TEXT,
            exception TEXT,
            action TEXT,
            filed_on TEXT,
            last_updated TEXT,
            days_pending INTEGER DEFAULT 0,
            fraud_score REAL DEFAULT 0.0,
            is_undertrial INTEGER DEFAULT 0,
            petition_language TEXT DEFAULT 'English',
            full_case_json TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_case(case):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute('''
            INSERT OR REPLACE INTO cases (
                case_id, petitioner_name, case_type, description,
                priority, status, assigned_court, assigned_judge,
                urgency_score, escalated, fast_track_court,
                exception, action, filed_on, last_updated,
                days_pending, fraud_score, is_undertrial,
                petition_language, full_case_json
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (
            case.get("case_id"),
            case.get("petitioner_name"),
            case.get("case_type"),
            case.get("description"),
            case.get("priority"),
            case.get("status"),
            case.get("assigned_court"),
            case.get("assigned_judge"),
            case.get("urgency_score"),
            1 if case.get("escalated") else 0,
            case.get("fast_track_court"),
            case.get("exception"),
            case.get("action"),
            case.get("filed_on"),
            case.get("last_updated"),
            case.get("days_pending", 0),
            case.get("fraud_score", 0.1),
            1 if case.get("is_undertrial") else 0,
            case.get("petition_language", "English"),
            json.dumps(case)
        ))
        conn.commit()
    except Exception as e:
        print(f"DB Error: {e}")
    finally:
        conn.close()

def get_all_cases():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM cases ORDER BY filed_on DESC')
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_stats():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    stats = {}
    c.execute('SELECT COUNT(*) FROM cases')
    stats['total'] = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM cases WHERE priority="CRITICAL"')
    stats['critical'] = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM cases WHERE escalated=1')
    stats['escalated'] = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM cases WHERE status="ASSIGNED"')
    stats['assigned'] = c.fetchone()[0]
    c.execute('SELECT case_type, COUNT(*) as count FROM cases GROUP BY case_type')
    stats['by_type'] = [{"type": r[0], "count": r[1]} for r in c.fetchall()]
    c.execute('SELECT priority, COUNT(*) as count FROM cases GROUP BY priority')
    stats['by_priority'] = [{"priority": r[0], "count": r[1]} for r in c.fetchall()]
    c.execute('SELECT status, COUNT(*) as count FROM cases GROUP BY status')
    stats['by_status'] = [{"status": r[0], "count": r[1]} for r in c.fetchall()]
    conn.close()
    return stats

def get_case_by_id(case_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM cases WHERE case_id=?', (case_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

# Initialize DB on import
init_db()
print("✅ NyayBot database initialized")