import tkinter as tk
from tkinter import ttk, messagebox
import json
from main_pipeline import run_nyaybot

# ── COLORS ─────────────────────────────────────────────────────────
BG = "#0f1117"
CARD = "#1a1d27"
ACCENT = "#4f46e5"
GREEN = "#22c55e"
RED = "#ef4444"
AMBER = "#f59e0b"
WHITE = "#f8fafc"
GRAY = "#94a3b8"

class NyayBotDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("NyayBot — AI Judicial Case Management")
        self.root.geometry("900x700")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)
        self.build_ui()

    def build_ui(self):
        # ── HEADER ──
        header = tk.Frame(self.root, bg=ACCENT, pady=15)
        header.pack(fill="x")
        tk.Label(header, text="⚖️  NyayBot", font=("Segoe UI", 22, "bold"),
                 bg=ACCENT, fg=WHITE).pack()
        tk.Label(header, text="AI Judicial Case Management System — India",
                 font=("Segoe UI", 11), bg=ACCENT, fg="#c7d2fe").pack()

        # ── MAIN FRAME ──
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=20, pady=15)

        # ── LEFT — INPUT FORM ──
        left = tk.Frame(main, bg=CARD, padx=20, pady=20)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left, text="File New Case", font=("Segoe UI", 14, "bold"),
                 bg=CARD, fg=WHITE).pack(anchor="w", pady=(0, 15))

        # Petitioner Name
        tk.Label(left, text="Petitioner Name", font=("Segoe UI", 10),
                 bg=CARD, fg=GRAY).pack(anchor="w")
        self.name_entry = tk.Entry(left, font=("Segoe UI", 11), bg="#2d3748",
                                   fg=WHITE, insertbackground=WHITE,
                                   relief="flat", bd=8)
        self.name_entry.pack(fill="x", pady=(2, 12))
        self.name_entry.insert(0, "Rajesh Kumar")

        # Case Type
        tk.Label(left, text="Case Type", font=("Segoe UI", 10),
                 bg=CARD, fg=GRAY).pack(anchor="w")
        self.case_type = ttk.Combobox(left, font=("Segoe UI", 11),
                                       values=["Civil", "Criminal", "Family",
                                               "Property", "Labour", "Consumer"],
                                       state="readonly")
        self.case_type.pack(fill="x", pady=(2, 12))
        self.case_type.set("Civil")

        # Description
        tk.Label(left, text="Case Description", font=("Segoe UI", 10),
                 bg=CARD, fg=GRAY).pack(anchor="w")
        self.desc_entry = tk.Text(left, font=("Segoe UI", 11), bg="#2d3748",
                                   fg=WHITE, insertbackground=WHITE,
                                   relief="flat", bd=8, height=4)
        self.desc_entry.pack(fill="x", pady=(2, 12))
        self.desc_entry.insert("1.0", "Property dispute with neighbour over land boundary")

        # Urgency
        tk.Label(left, text="Urgency Score (1-10)", font=("Segoe UI", 10),
                 bg=CARD, fg=GRAY).pack(anchor="w")
        self.urgency = tk.Scale(left, from_=1, to=10, orient="horizontal",
                                bg=CARD, fg=WHITE, highlightthickness=0,
                                activebackground=ACCENT, troughcolor="#2d3748")
        self.urgency.pack(fill="x", pady=(2, 12))
        self.urgency.set(5)

        # Undertrial checkbox
        self.undertrial_var = tk.BooleanVar()
        tk.Checkbutton(left, text="Undertrial Prisoner",
                       variable=self.undertrial_var,
                       bg=CARD, fg=WHITE, selectcolor=ACCENT,
                       activebackground=CARD, font=("Segoe UI", 10)).pack(anchor="w")

        # Language
        tk.Label(left, text="Petition Language", font=("Segoe UI", 10),
                 bg=CARD, fg=GRAY).pack(anchor="w", pady=(10, 0))
        self.language = ttk.Combobox(left, font=("Segoe UI", 11),
                                      values=["English", "Hindi", "Tamil",
                                              "Telugu", "Marathi", "Bengali"],
                                      state="readonly")
        self.language.pack(fill="x", pady=(2, 15))
        self.language.set("English")

        # Submit button
        tk.Button(left, text="⚡  File Case & Run NyayBot",
                  font=("Segoe UI", 12, "bold"),
                  bg=ACCENT, fg=WHITE, relief="flat",
                  activebackground="#4338ca", cursor="hand2",
                  pady=10, command=self.run_case).pack(fill="x")

        # ── RIGHT — OUTPUT ──
        right = tk.Frame(main, bg=CARD, padx=20, pady=20)
        right.pack(side="right", fill="both", expand=True)

        tk.Label(right, text="Case Result", font=("Segoe UI", 14, "bold"),
                 bg=CARD, fg=WHITE).pack(anchor="w", pady=(0, 10))

        # Status badge
        self.status_label = tk.Label(right, text="Awaiting submission...",
                                      font=("Segoe UI", 11, "bold"),
                                      bg=CARD, fg=GRAY)
        self.status_label.pack(anchor="w", pady=(0, 10))

        # Result text box
        self.result_text = tk.Text(right, font=("Consolas", 10),
                                    bg="#0d1117", fg=GREEN,
                                    insertbackground=WHITE,
                                    relief="flat", bd=8,
                                    wrap="word")
        self.result_text.pack(fill="both", expand=True)

    def run_case(self):
        name = self.name_entry.get()
        case_type = self.case_type.get()
        description = self.desc_entry.get("1.0", "end-1c")
        urgency = self.urgency.get()
        language = self.language.get()
        is_undertrial = self.undertrial_var.get()

        if not name or not description:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        self.status_label.config(text="⏳ Processing case...", fg=AMBER)
        self.result_text.delete("1.0", "end")
        self.root.update()

        params = {
            "submitted_docs": ["Petition", "Identity Proof", "Evidence Documents",
                                "FIR", "Witness Statement"],
            "accused_found": True,
            "fraud_score": 0.1,
            "petition_language": language,
            "is_undertrial": is_undertrial,
            "days_in_custody": 220 if is_undertrial else 0
        }

        try:
            case = run_nyaybot(name, case_type, description, urgency, params)

            # Display result
            self.result_text.delete("1.0", "end")
            self.result_text.insert("end", f"CASE ID: {case['case_id']}\n\n")
            self.result_text.insert("end", f"Petitioner: {case['petitioner_name']}\n")
            self.result_text.insert("end", f"Type: {case['case_type']}\n")
            self.result_text.insert("end", f"Priority: {case.get('priority', 'N/A')}\n")
            self.result_text.insert("end", f"Status: {case['status']}\n")
            self.result_text.insert("end", f"Court: {case['assigned_court']}\n")
            self.result_text.insert("end", f"Judge: {case.get('assigned_judge', 'PENDING')}\n")
            self.result_text.insert("end", f"Escalated: {case['escalated']}\n")
            if case.get("fast_track_court"):
                self.result_text.insert("end", f"\n⚠️ Fast Track: {case['fast_track_court']}\n")
            if case.get("exception"):
                self.result_text.insert("end", f"\n⚠️ Exception: {case['exception']}\n")
                self.result_text.insert("end", f"Action: {case.get('action')}\n")

            # Update status badge color
            priority = case.get("priority", "")
            if priority == "CRITICAL":
                self.status_label.config(text="🔴 CRITICAL CASE", fg=RED)
            elif priority == "HIGH":
                self.status_label.config(text="🟡 HIGH PRIORITY", fg=AMBER)
            else:
                self.status_label.config(text="🟢 CASE PROCESSED", fg=GREEN)

        except Exception as e:
            self.result_text.insert("end", f"Error: {str(e)}")
            self.status_label.config(text="❌ Error occurred", fg=RED)

if __name__ == "__main__":
    root = tk.Tk()
    app = NyayBotDashboard(root)
    root.mainloop()
    