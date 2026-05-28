import random

def chat_with_nyaybot(messages):
    # Get the last user message
    last_message = messages[-1]["content"].lower()

    # Smart response matching
    if any(w in last_message for w in ["murder", "violence", "assault", "criminal"]):
        return random.choice([
            "A murder case in NyayBot gets classified as CRITICAL priority immediately. It's routed to Sessions Court, assigned to the judge with the least current caseload, and flagged for urgent hearing scheduling. If the accused is absconding, a non-bailable warrant is auto-issued and the case is paused until the accused is produced.",
            "Criminal cases involving violence are scored 8-10 on our urgency scale. NyayBot routes them to Sessions Court, triggers warrant issuance if accused is missing, and escalates to fast track if no hearing happens within 90 days."
        ])

    elif any(w in last_message for w in ["escalat", "fast track", "90 days", "pending", "stall"]):
        return random.choice([
            "NyayBot's stall detector runs continuously. Any case idle for more than 90 days gets automatically escalated — CRITICAL cases go to Supreme Court Fast Track Bench, HIGH priority to High Court Fast Track Division, others to District Fast Track Court. This directly addresses India's 40 million pending case backlog.",
            "Cases get escalated when they exceed the 90-day idle threshold. Our stall detection engine checks every case daily and flags ones with no hearing activity. The registrar gets an alert and the case is fast-tracked within 7 days."
        ])

    elif any(w in last_message for w in ["judge", "assign", "court"]):
        return random.choice([
            "NyayBot assigns judges based on two factors: court type matching and current caseload. CRITICAL cases always go to the judge with the fewest active cases to ensure fastest resolution. If no judge is available, the case is flagged as PENDING_JUDGE and the registrar is alerted immediately.",
            "Judge assignment is automatic in NyayBot. We match the case type to the right court — Criminal goes to Sessions Court, Civil to Civil District Court, Family to Family Court — then pick the most available judge. For critical cases we always pick the judge with the lightest workload."
        ])

    elif any(w in last_message for w in ["undertrial", "custody", "jail", "prison"]):
        return random.choice([
            "Undertrial prisoners are a serious human rights concern in India. NyayBot automatically flags any undertrial in custody for more than 180 days as CRITICAL and triggers mandatory bail review within 7 days. This is one of our most important features — thousands of people sit in jail for years awaiting trial.",
            "When a case is marked as undertrial, NyayBot tracks days in custody. Beyond 180 days, it becomes CRITICAL automatically and gets escalated to fast track court with a mandatory bail review order. No undertrial should wait indefinitely for justice."
        ])

    elif any(w in last_message for w in ["stage", "pipeline", "how does", "how it work", "process"]):
        return random.choice([
            "NyayBot has 7 stages: 1) Filing — case submitted with all details. 2) AI Triage — urgency scored 1-10, priority set. 3) Exception Check — 12 checks run automatically. 4) Judge Assignment — right court and judge assigned. 5) Stall Detection — idle cases flagged. 6) Human Checkpoint — registrar approval. 7) Verdict & Archive — judgment recorded and parties notified.",
            "The NyayBot pipeline has 7 stages. Filing → AI Triage (urgency scoring) → Exception Handling (12 real world checks) → Judge Assignment → Stall Detection (90 day rule) → Human Registrar Checkpoint → Final Verdict & Case Closure. Each stage has automatic escalation if something goes wrong."
        ])

    elif any(w in last_message for w in ["fraud", "fake", "false"]):
        return random.choice([
            "NyayBot has a fraud detection engine that scores every filing from 0 to 1. A score above 0.7 triggers FRAUD_SUSPECTED status — the case is flagged for human review, the filing party is notified, and the IP address is logged. This prevents the system from being abused with false complaints.",
            "Fraudulent filings are a real problem in India's courts. Our fraud score algorithm analyzes filing patterns and flags suspicious cases automatically. Anything above 70% fraud probability goes to human review before processing."
        ])

    elif any(w in last_message for w in ["missing", "document", "incomplete"]):
        return random.choice([
            "Each case type in NyayBot has required documents — Criminal cases need FIR, Identity Proof and Witness Statement. Civil cases need Petition, Identity Proof and Evidence Documents. If any are missing, the case gets INCOMPLETE status and the petitioner is automatically notified with exactly what's needed and a 30-day deadline.",
            "NyayBot checks documents at Stage 3. Missing documents trigger an automatic notification to the petitioner listing exactly what's needed. The case is put on hold until documents are received. This prevents cases from being filed incompletely and wasting court time."
        ])

    elif any(w in last_message for w in ["language", "hindi", "tamil", "telugu", "marathi", "bengali"]):
        return random.choice([
            "India's linguistic diversity is a real barrier to justice. NyayBot detects when a petition is filed in a regional language and automatically requests a certified translation. The case is put on TRANSLATION_PENDING hold until the translation is received. We support Hindi, Tamil, Telugu, Marathi, Bengali and English.",
            "When a petition arrives in a regional language, NyayBot flags it as TRANSLATION_PENDING and requests a certified translation before processing. This ensures the case details are accurately understood by the court."
        ])

    elif any(w in last_message for w in ["appeal", "verdict", "judgment", "high court", "supreme"]):
        return random.choice([
            "When a verdict is appealed, NyayBot automatically escalates the case up the court hierarchy — Civil District Court appeals go to High Court, High Court appeals go to Supreme Court. The original case is archived and a new case record is created at the higher court level with full history attached.",
            "Appeals are handled automatically. NyayBot tracks the court hierarchy and routes appeals to the next level — District → High Court → Supreme Court. All previous case history travels with the appeal so the higher court has full context."
        ])

    elif any(w in last_message for w in ["backlog", "40 million", "india", "problem", "crisis"]):
        return random.choice([
            "India's judicial backlog is a national crisis — 40 million pending cases, average resolution time of 10-15 years, and only 20,000 judges for a population of 1.4 billion. NyayBot directly attacks the administrative chaos — automated triage, instant assignment, stall detection — so judges can focus on what only they can do: deliver justice.",
            "The numbers are staggering — 40 million cases pending, judges handling 10x their recommended caseload, and citizens waiting decades for resolution. NyayBot automates everything except the actual judgment, cutting administrative delay from weeks to seconds."
        ])

    elif any(w in last_message for w in ["hello", "hi", "namaste", "hey"]):
        return "Namaste! I'm NyayBot, your AI judicial case management assistant. I can explain how cases flow through our 7-stage pipeline, why cases get escalated, what happens in different exception scenarios, or anything about India's judicial system. What would you like to know?"

    elif any(w in last_message for w in ["thank", "thanks", "great", "good", "amazing", "wow"]):
        return "Happy to help! Justice delayed is justice denied — that's exactly why NyayBot exists. Is there anything else you'd like to know about how the system works?"

    else:
        return random.choice([
            "That's a great question about India's judicial system. NyayBot handles this through our intelligent pipeline — cases are triaged by AI, assigned to the right court and judge, monitored for delays, and escalated automatically when needed. Could you be more specific about which aspect you'd like to understand better?",
            "NyayBot is designed to handle exactly these kinds of complex scenarios. Our 7-stage pipeline with 12 exception handlers ensures no case falls through the cracks. Can you tell me more about what specifically you'd like to know?",
            "India's judicial system faces enormous challenges — 40 million pending cases, understaffed courts, and administrative bottlenecks. NyayBot tackles this by automating everything that doesn't require a judge's wisdom. What aspect would you like me to explain further?"
        ])


CHAT_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NyayBot — AI Chat</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #050508; --surface: #0d0d14; --card: #12121c;
    --border: #1e1e30; --accent: #6c63ff; --accent2: #ff6584;
    --green: #00f5a0; --amber: #ffb347; --red: #ff4d6d;
    --text: #e8e8f0; --muted: #6b6b8a;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: var(--bg); color: var(--text); font-family: "Syne", sans-serif; min-height: 100vh; display: flex; flex-direction: column; }
  body::before {
    content: ""; position: fixed; inset: 0;
    background-image: linear-gradient(rgba(108,99,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(108,99,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px; pointer-events: none; z-index: 0;
  }
  .wrapper { position: relative; z-index: 1; max-width: 900px; margin: 0 auto; padding: 0 24px; width: 100%; flex: 1; display: flex; flex-direction: column; }
  header { padding: 28px 0 20px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border); margin-bottom: 24px; flex-shrink: 0; }
  .logo { display: flex; align-items: center; gap: 12px; }
  .logo-icon { width: 40px; height: 40px; background: linear-gradient(135deg, var(--accent), var(--accent2)); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 18px; }
  .logo h1 { font-size: 18px; font-weight: 800; background: linear-gradient(135deg, #fff, var(--accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .nav { display: flex; gap: 8px; }
  .nav a { padding: 8px 16px; border-radius: 8px; font-size: 13px; color: var(--muted); text-decoration: none; transition: all 0.2s; border: 1px solid transparent; }
  .nav a:hover { color: var(--text); border-color: var(--border); }
  .nav a.active { color: var(--accent); border-color: var(--accent); background: rgba(108,99,255,0.1); }
  .chat-container { flex: 1; background: var(--card); border: 1px solid var(--border); border-radius: 20px; display: flex; flex-direction: column; overflow: hidden; margin-bottom: 24px; min-height: 500px; }
  .chat-header { padding: 16px 24px; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 12px; flex-shrink: 0; }
  .bot-avatar { width: 36px; height: 36px; background: linear-gradient(135deg, var(--accent), var(--accent2)); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }
  .bot-info h3 { font-size: 14px; font-weight: 700; }
  .bot-info p { font-size: 11px; color: var(--muted); font-family: "JetBrains Mono", monospace; }
  .online-dot { width: 8px; height: 8px; background: var(--green); border-radius: 50%; margin-left: auto; animation: pulse 2s ease-in-out infinite; }
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
  .messages { flex: 1; overflow-y: auto; padding: 24px; display: flex; flex-direction: column; gap: 16px; }
  .messages::-webkit-scrollbar { width: 4px; }
  .messages::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
  .message { display: flex; gap: 10px; max-width: 80%; animation: fadeIn 0.3s ease; }
  .message.user { align-self: flex-end; flex-direction: row-reverse; }
  .message.bot { align-self: flex-start; }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
  .msg-avatar { width: 32px; height: 32px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0; }
  .bot .msg-avatar { background: linear-gradient(135deg, var(--accent), var(--accent2)); }
  .user .msg-avatar { background: var(--surface); border: 1px solid var(--border); }
  .msg-bubble { padding: 12px 16px; border-radius: 14px; font-size: 14px; line-height: 1.6; }
  .bot .msg-bubble { background: var(--surface); border: 1px solid var(--border); border-top-left-radius: 4px; color: var(--text); }
  .user .msg-bubble { background: linear-gradient(135deg, var(--accent), var(--accent2)); border-top-right-radius: 4px; color: white; }
  .msg-time { font-size: 10px; color: var(--muted); font-family: "JetBrains Mono", monospace; margin-top: 4px; }
  .bot .msg-time { text-align: left; }
  .user .msg-time { text-align: right; }
  .typing { display: none; align-self: flex-start; }
  .typing .msg-bubble { background: var(--surface); border: 1px solid var(--border); padding: 14px 18px; }
  .typing-dots { display: flex; gap: 4px; }
  .typing-dots span { width: 6px; height: 6px; background: var(--muted); border-radius: 50%; animation: bounce 1.2s ease-in-out infinite; }
  .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
  .typing-dots span:nth-child(3) { animation-delay: 0.4s; }
  @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-4px); } }
  .suggestions { padding: 0 24px 16px; display: flex; gap: 8px; flex-wrap: wrap; flex-shrink: 0; }
  .suggestion { background: var(--surface); border: 1px solid var(--border); border-radius: 20px; padding: 6px 14px; font-size: 12px; color: var(--muted); cursor: pointer; transition: all 0.2s; font-family: "JetBrains Mono", monospace; }
  .suggestion:hover { color: var(--accent); border-color: var(--accent); background: rgba(108,99,255,0.1); }
  .input-area { padding: 16px 24px; border-top: 1px solid var(--border); display: flex; gap: 12px; align-items: center; flex-shrink: 0; }
  .input-area input { flex: 1; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 12px 18px; color: var(--text); font-family: "Syne", sans-serif; font-size: 14px; outline: none; transition: border-color 0.2s; }
  .input-area input:focus { border-color: var(--accent); }
  .input-area input::placeholder { color: var(--muted); }
  .send-btn { width: 44px; height: 44px; background: linear-gradient(135deg, var(--accent), var(--accent2)); border: none; border-radius: 12px; color: white; font-size: 18px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s; flex-shrink: 0; }
  .send-btn:hover { transform: scale(1.05); box-shadow: 0 4px 20px rgba(108,99,255,0.4); }
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
      <a href="/chat" class="active">💬 AI Chat</a>
    </nav>
  </header>

  <div class="chat-container">
    <div class="chat-header">
      <div class="bot-avatar">⚖️</div>
      <div class="bot-info">
        <h3>NyayBot Assistant</h3>
        <p>AI-powered judicial case advisor</p>
      </div>
      <div class="online-dot"></div>
    </div>

    <div class="messages" id="messages">
      <div class="message bot">
        <div class="msg-avatar">⚖️</div>
        <div>
          <div class="msg-bubble">Namaste! I'm NyayBot, your AI judicial case management assistant. I can explain how cases are processed, why cases get escalated, what happens in exception scenarios, and answer anything about India's judicial system. How can I help you today?</div>
          <div class="msg-time">Just now</div>
        </div>
      </div>
      <div class="message typing" id="typing">
        <div class="msg-avatar">⚖️</div>
        <div class="msg-bubble">
          <div class="typing-dots"><span></span><span></span><span></span></div>
        </div>
      </div>
    </div>

    <div class="suggestions" id="suggestions">
      <div class="suggestion" onclick="sendSuggestion(this)">What happens to a murder case?</div>
      <div class="suggestion" onclick="sendSuggestion(this)">Why do cases get escalated?</div>
      <div class="suggestion" onclick="sendSuggestion(this)">How are judges assigned?</div>
      <div class="suggestion" onclick="sendSuggestion(this)">What is an undertrial prisoner?</div>
      <div class="suggestion" onclick="sendSuggestion(this)">Explain the 7 stages of NyayBot</div>
    </div>

    <div class="input-area">
      <input type="text" id="user-input" placeholder="Ask anything about NyayBot or India's judicial system..."
             onkeydown="if(event.key==='Enter') sendMessage()">
      <button class="send-btn" onclick="sendMessage()">↑</button>
    </div>
  </div>
</div>

<script>
let conversationHistory = [];

function getTime() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function addMessage(text, role) {
  const messages = document.getElementById("messages");
  const typing = document.getElementById("typing");
  const div = document.createElement("div");
  div.className = `message ${role}`;
  div.innerHTML = `
    <div class="msg-avatar">${role === "bot" ? "⚖️" : "👤"}</div>
    <div>
      <div class="msg-bubble">${text}</div>
      <div class="msg-time">${getTime()}</div>
    </div>
  `;
  messages.insertBefore(div, typing);
  messages.scrollTop = messages.scrollHeight;
}

function sendSuggestion(el) {
  document.getElementById("user-input").value = el.textContent;
  document.getElementById("suggestions").style.display = "none";
  sendMessage();
}

async function sendMessage() {
  const input = document.getElementById("user-input");
  const text = input.value.trim();
  if (!text) return;
  input.value = "";
  document.getElementById("suggestions").style.display = "none";
  addMessage(text, "user");
  conversationHistory.push({ role: "user", content: text });
  document.getElementById("typing").style.display = "flex";
  document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;

  setTimeout(async () => {
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: conversationHistory })
      });
      const data = await res.json();
      document.getElementById("typing").style.display = "none";
      addMessage(data.response, "bot");
      conversationHistory.push({ role: "assistant", content: data.response });
    } catch(e) {
      document.getElementById("typing").style.display = "none";
      addMessage("Sorry, I encountered an error. Please try again.", "bot");
    }
  }, 1200);
}
</script>
</body>
</html>
'''