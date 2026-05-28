# ⚖️ NyayBot — AI Judicial Case Management System

> *Justice delayed is justice denied. NyayBot fixes that.*

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![UiPath](https://img.shields.io/badge/UiPath-Maestro_Case-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

---

## 🇮🇳 The Problem

India has **40 million pending court cases**. The average case takes **10–15 years** to resolve. There are only **20,000 judges** for a population of **1.4 billion people**.

The root cause isn't a lack of judges — it's **administrative chaos**. Cases get lost in paperwork. Wrong courts. Missing documents. Accused persons absconding. Undertrial prisoners waiting years without a hearing. Nobody tracking what's stalled and why.

**NyayBot fixes this.**

---

## 💡 What is NyayBot?

NyayBot is an AI-powered judicial case management agent built on **UiPath Maestro Case**. It automates the entire administrative lifecycle of a court case — from intelligent filing through verdict archiving — so judges can focus on what only they can do: deliver justice.

NyayBot doesn't replace judges. It eliminates everything that gets in their way.

---

## 🚀 Features

### 7-Stage AI Pipeline
| Stage | What Happens |
|-------|-------------|
| 1️⃣ Filing | Case submitted with all petitioner details |
| 2️⃣ AI Triage | Urgency scored 1–10, priority set, court type determined |
| 3️⃣ Exception Check | 12 real-world checks run automatically |
| 4️⃣ Judge Assignment | Right judge assigned based on court and availability |
| 5️⃣ Stall Detection | Cases idle 90+ days flagged and escalated |
| 6️⃣ Human Checkpoint | Registrar reviews and approves before proceeding |
| 7️⃣ Verdict & Archive | Judgment recorded, parties notified, case closed |

### 12 Exception Handlers
- ❌ Wrong jurisdiction detection
- 📋 Missing document detection
- 🚨 Absconding accused → auto warrant
- 👨‍⚖️ Lawyer no-show → adjournment tracking
- ⚖️ Judge recusal → auto reassignment
- 📤 Appeal filing → court hierarchy escalation
- 🔍 Evidence tampering detection
- 📑 Duplicate case merging
- 🔒 Undertrial prisoner rights protection
- ☠️ Party death handling
- 🌐 Language barrier → translation request
- 🤖 Fraudulent filing detection

### 5 Pages
- ⚡ **File Case** — Submit and process cases through the full pipeline
- 📋 **Case Tracker** — Live table with search, filters, and real-time stats
- 📊 **Analytics** — Charts showing priority breakdown, case types, escalation rates
- 💬 **AI Chat** — Ask NyayBot anything about cases or India's judicial system
- 🔔 **Live Alerts** — Real-time notifications for critical events

---

## 🏗️ Architecture
User / UiPath Maestro

app.py (Flask API)
│
├── case_model.py       → Case data structure
├── triage_agent.py     → AI urgency scoring
├── court_assigner.py   → Judge assignment engine
├── stall_detector.py   → 90-day idle detection
├── exception_handler.py→ 12 exception handlers
├── main_pipeline.py    → Full 7-stage orchestration
├── database.py         → SQLite persistence
├── notifications.py    → Live alert system
├── tracker.py          → Case tracker UI
├── analytics.py        → Analytics dashboard
└── chat.py             → AI chat assistant
---

## ⚙️ Setup

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/kesar-progg/nyaybot.git
cd nyaybot

# Install dependencies
pip install flask anthropic

# Run NyayBot
python app.py
```

### Access
Open your browser and go to `http://localhost:5000`

---

## 🎯 UiPath Integration

NyayBot is built for **UiPath Maestro Case — Track 1**.

The `main_pipeline.py` exposes a clean API that UiPath agents call at each stage:

- **POST /process_case** — Full pipeline execution
- **GET /api/cases** — Retrieve all cases
- **GET /api/stats** — Dashboard statistics
- **GET /api/notifications** — Live alerts feed

Each Maestro Case stage maps directly to NyayBot's pipeline stages, with human approval checkpoints at Stage 6 handled through UiPath Action Center.

---

## 🏆 Prize Categories Targeting

- 🥇 Best of Track 1 — Maestro Case
- 🎨 Most Creative Use Case
- 🎬 Best Demo
- 💬 Best Product Feedback

---

## 👤 Team

**NyayBot** — Solo submission for UiPath AgentHack 2026

Built with Python, Flask, SQLite, and UiPath Maestro Case.

---

## 📄 License

MIT License — free to use, modify, and build upon.

---

*⚖️ Because in India, 40 million people are still waiting for justice.*