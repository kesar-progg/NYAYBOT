import json
from datetime import datetime
from case_model import create_case
from triage_agent import triage_case
from court_assigner import assign_judge
from stall_detector import detect_stall
from exception_handler import run_all_exception_checks

def run_nyaybot(name, case_type, description, urgency, params={}):
    print("\n" + "="*60)
    print("⚖️  NYAYBOT — AI Judicial Case Management System")
    print("="*60)

    # STAGE 1 — File the case
    print("\n📋 STAGE 1: Filing case...")
    case = create_case(name, case_type, description, urgency)
    print(f"✅ Case filed: {case['case_id']}")

    # STAGE 2 — AI Triage
    print("\n🤖 STAGE 2: AI Triage...")
    case = triage_case(case)
    print(f"✅ Priority: {case['priority']} | Court: {case['assigned_court']}")

    # STAGE 3 — Exception Checks
    print("\n🔍 STAGE 3: Running exception checks...")
    case = run_all_exception_checks(case, params)

    # STAGE 4 — Judge Assignment
    print("\n👨‍⚖️ STAGE 4: Assigning judge...")
    case = assign_judge(case)
    if case.get("assigned_judge"):
        print(f"✅ Assigned to: {case['assigned_judge']}")
    else:
        print(f"⚠️  No judge available: {case.get('assignment_note')}")

    # STAGE 5 — Stall Detection
    print("\n⏱️  STAGE 5: Checking for stalls...")
    case = detect_stall(case)

    # STAGE 6 — Human Checkpoint
    print("\n👤 STAGE 6: Human checkpoint — Registrar review required")
    print(f"   Case ID: {case['case_id']}")
    print(f"   Petitioner: {case['petitioner_name']}")
    print(f"   Priority: {case.get('priority', 'UNKNOWN')}")
    print(f"   Status: {case['status']}")
    print(f"   Assigned Judge: {case.get('assigned_judge', 'PENDING')}")
    if case.get("escalated"):
        print(f"   ⚠️  Fast Track Court: {case.get('fast_track_court')}")
    print("\n   ➡️  Awaiting registrar approval to proceed...")

    # STAGE 7 — Final Summary
    print("\n📊 FINAL CASE SUMMARY:")
    print("="*60)
    summary = {
        "case_id": case["case_id"],
        "petitioner": case["petitioner_name"],
        "type": case["case_type"],
        "priority": case.get("priority"),
        "status": case["status"],
        "assigned_court": case["assigned_court"],
        "assigned_judge": case.get("assigned_judge"),
        "escalated": case["escalated"],
        "filed_on": case["filed_on"]
    }
    print(json.dumps(summary, indent=4))
    return case


# ── TEST ALL SCENARIOS ─────────────────────────────────────────────
if __name__ == "__main__":

    # Scenario 1 — Normal civil case
    run_nyaybot(
        name="Rajesh Kumar",
        case_type="Civil",
        description="Property dispute with neighbour over land boundary",
        urgency=5,
        params={
            "submitted_docs": ["Petition", "Identity Proof", "Evidence Documents"],
            "accused_found": True,
            "fraud_score": 0.1,
            "petition_language": "English"
        }
    )

    # Scenario 2 — Critical criminal case
    run_nyaybot(
        name="Sunita Devi",
        case_type="Criminal",
        description="Murder case involving violence and assault on family",
        urgency=9,
        params={
            "submitted_docs": ["FIR", "Identity Proof", "Witness Statement"],
            "accused_found": False,
            "fraud_score": 0.05,
            "petition_language": "English"
        }
    )

    # Scenario 3 — Stalled undertrial case
    run_nyaybot(
        name="Amit Singh",
        case_type="Criminal",
        description="Theft case with undertrial prisoner",
        urgency=6,
        params={
            "submitted_docs": ["FIR", "Identity Proof", "Witness Statement"],
            "accused_found": True,
            "is_undertrial": True,
            "days_in_custody": 220,
            "fraud_score": 0.1,
            "petition_language": "English"
        }
    )