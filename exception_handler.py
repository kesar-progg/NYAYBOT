import json
from datetime import datetime

# ── 1. JURISDICTION CHECK ──────────────────────────────────────────
def check_jurisdiction(case):
    valid_mapping = {
        "Civil": ["Civil District Court"],
        "Criminal": ["Sessions Court"],
        "Family": ["Family Court"],
        "Property": ["Civil District Court"],
        "Labour": ["Labour Court"],
        "Consumer": ["Consumer Disputes Court"]
    }
    valid_courts = valid_mapping.get(case["case_type"], [])
    if case["assigned_court"] not in valid_courts:
        case["status"] = "JURISDICTION_ERROR"
        case["exception"] = f"Wrong court! {case['case_type']} case cannot go to {case['assigned_court']}"
        case["action"] = "Redirected to correct court automatically"
        case["assigned_court"] = valid_courts[0] if valid_courts else "General Court"
    return case

# ── 2. MISSING DOCUMENTS CHECK ─────────────────────────────────────
def check_documents(case, submitted_docs):
    required_docs = {
        "Criminal": ["FIR", "Identity Proof", "Witness Statement"],
        "Civil": ["Petition", "Identity Proof", "Evidence Documents"],
        "Family": ["Marriage Certificate", "Identity Proof", "Petition"],
        "Property": ["Land Records", "Identity Proof", "Survey Map"],
        "Labour": ["Employment Contract", "Identity Proof", "Complaint Letter"],
        "Consumer": ["Purchase Receipt", "Identity Proof", "Complaint Form"]
    }
    required = required_docs.get(case["case_type"], ["Identity Proof", "Petition"])
    missing = [doc for doc in required if doc not in submitted_docs]
    if missing:
        case["status"] = "INCOMPLETE"
        case["missing_documents"] = missing
        case["exception"] = f"Missing documents: {', '.join(missing)}"
        case["action"] = "Notified petitioner to submit missing documents within 30 days"
    else:
        case["documents_verified"] = True
    return case

# ── 3. ACCUSED ABSCONDING ──────────────────────────────────────────
def check_accused_status(case, accused_found):
    if not accused_found:
        case["status"] = "WARRANT_ISSUED"
        case["exception"] = "Accused not found at given address"
        case["action"] = "Non-bailable warrant issued. Case paused until accused is produced."
        case["warrant_issued"] = True
        case["warrant_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return case

# ── 4. LAWYER NO-SHOW ──────────────────────────────────────────────
def handle_lawyer_noshow(case, hearing_date):
    case["status"] = "HEARING_ADJOURNED"
    case["exception"] = f"Lawyer did not appear for hearing on {hearing_date}"
    case["action"] = "Hearing adjourned. New date assigned. Strike recorded against advocate."
    case["adjournment_count"] = case.get("adjournment_count", 0) + 1
    if case["adjournment_count"] >= 3:
        case["action"] = "3 adjournments exceeded. Court proceeding ex-parte."
        case["status"] = "EX_PARTE"
    return case

# ── 5. JUDGE RECUSAL ───────────────────────────────────────────────
def handle_judge_recusal(case, reason):
    case["exception"] = f"Judge recused: {reason}"
    case["action"] = "Case reassigned to next available judge in same court"
    case["previous_judge"] = case.get("assigned_judge", "Unknown")
    case["assigned_judge"] = None
    case["status"] = "REASSIGNMENT_NEEDED"
    return case

# ── 6. APPEAL FILED ────────────────────────────────────────────────
def handle_appeal(case, appeal_by):
    case["status"] = "APPEALED"
    case["exception"] = f"Verdict appealed by: {appeal_by}"
    court_hierarchy = {
        "Civil District Court": "High Court",
        "Sessions Court": "High Court",
        "Family Court": "High Court",
        "High Court": "Supreme Court",
        "Labour Court": "High Court",
        "Consumer Disputes Court": "State Consumer Commission"
    }
    case["previous_court"] = case["assigned_court"]
    case["assigned_court"] = court_hierarchy.get(case["assigned_court"], "Supreme Court")
    case["action"] = f"Case escalated to {case['assigned_court']} for appeal hearing"
    return case

# ── 7. EVIDENCE TAMPERING ──────────────────────────────────────────
def check_evidence_tampering(case, tampering_detected):
    if tampering_detected:
        case["status"] = "EVIDENCE_FLAGGED"
        case["exception"] = "Potential evidence tampering detected in submitted documents"
        case["action"] = "Case flagged for forensic review. Human judge must review before proceeding."
        case["priority"] = "CRITICAL"
        case["human_review_required"] = True
    return case

# ── 8. DUPLICATE CASE ──────────────────────────────────────────────
def check_duplicate(case, existing_case_id):
    if existing_case_id:
        case["status"] = "DUPLICATE_DETECTED"
        case["exception"] = f"Similar case already exists: {existing_case_id}"
        case["action"] = "Cases merged. Original case takes precedence. Petitioner notified."
        case["merged_with"] = existing_case_id
    return case

# ── 9. UNDERTRIAL PRISONER ─────────────────────────────────────────
def check_undertrial(case, is_undertrial, days_in_custody):
    if is_undertrial:
        case["undertrial"] = True
        case["days_in_custody"] = days_in_custody
        if days_in_custody > 180:
            case["priority"] = "CRITICAL"
            case["status"] = "URGENT_BAIL_REVIEW"
            case["exception"] = f"Undertrial prisoner in custody for {days_in_custody} days — human rights violation risk"
            case["action"] = "Immediately escalated to fast track court. Bail review mandatory within 7 days."
    return case

# ── 10. DEATH OF PARTY ─────────────────────────────────────────────
def handle_party_death(case, deceased_party):
    case["exception"] = f"{deceased_party} has passed away during proceedings"
    if deceased_party == "Petitioner":
        case["action"] = "Legal heirs notified. 90 days given to substitute petitioner."
        case["status"] = "SUBSTITUTION_PENDING"
    elif deceased_party == "Accused":
        case["action"] = "Criminal case closed. Civil claims transferred to legal heirs."
        case["status"] = "CLOSED_DEATH"
    return case

# ── 11. LANGUAGE BARRIER ───────────────────────────────────────────
def handle_language(case, petition_language):
    official_language = "English"
    if petition_language != official_language:
        case["exception"] = f"Petition submitted in {petition_language}"
        case["action"] = f"Auto-translation requested. Case on hold until certified translation received."
        case["status"] = "TRANSLATION_PENDING"
        case["original_language"] = petition_language
    return case

# ── 12. FRAUDULENT FILING ──────────────────────────────────────────
def check_fraud(case, fraud_score):
    # fraud_score between 0-1, above 0.7 is suspicious
    case["fraud_score"] = fraud_score
    if fraud_score > 0.7:
        case["status"] = "FRAUD_SUSPECTED"
        case["exception"] = f"High fraud probability detected: {fraud_score * 100:.0f}%"
        case["action"] = "Case flagged for human review. Filing party notified. IP logged."
        case["human_review_required"] = True
        case["priority"] = "CRITICAL"
    return case


# ── RUN ALL CHECKS ─────────────────────────────────────────────────
def run_all_exception_checks(case, params):
    print(f"\n🔍 Running exception checks for case: {case['case_id']}")
    print("=" * 55)

    case = check_jurisdiction(case)
    case = check_documents(case, params.get("submitted_docs", []))
    case = check_accused_status(case, params.get("accused_found", True))
    case = check_evidence_tampering(case, params.get("tampering_detected", False))
    case = check_duplicate(case, params.get("duplicate_case_id", None))
    case = check_undertrial(case, params.get("is_undertrial", False), params.get("days_in_custody", 0))
    case = handle_language(case, params.get("petition_language", "English"))
    case = check_fraud(case, params.get("fraud_score", 0.1))

    exceptions = [k for k in ["exception", "missing_documents", "warrant_issued"] if k in case]
    if exceptions:
        print(f"⚠️  Exceptions found: {case.get('exception', 'See case details')}")
        print(f"📋 Action taken: {case.get('action', 'Manual review required')}")
    else:
        print("✅ All checks passed — case is clean!")

    print(f"📁 Final Status: {case['status']}")
    return case


# ── TEST IT ────────────────────────────────────────────────────────
if __name__ == "__main__":
    from case_model import create_case
    from triage_agent import triage_case
    from court_assigner import assign_judge

    # Test 1 — Undertrial prisoner
    print("\n🧪 TEST 1: Undertrial Prisoner (220 days in custody)")
    case1 = create_case("Mohammed Rafiq", "Criminal",
                        "Theft case, accused in custody", 6)
    case1 = triage_case(case1)
    case1 = assign_judge(case1)
    case1 = run_all_exception_checks(case1, {
        "submitted_docs": ["FIR", "Identity Proof", "Witness Statement"],
        "accused_found": True,
        "is_undertrial": True,
        "days_in_custody": 220,
        "fraud_score": 0.1
    })

    # Test 2 — Missing documents + fraud suspicion
    print("\n🧪 TEST 2: Missing Documents + Fraud Suspected")
    case2 = create_case("Fake Filer", "Civil",
                        "Property dispute", 4)
    case2 = triage_case(case2)
    case2 = assign_judge(case2)
    case2 = run_all_exception_checks(case2, {
        "submitted_docs": ["Petition"],
        "accused_found": True,
        "fraud_score": 0.85
    })

    # Test 3 — Language barrier
    print("\n🧪 TEST 3: Petition in Regional Language")
    case3 = create_case("Ravi Shankar", "Family",
                        "Divorce proceedings", 3)
    case3 = triage_case(case3)
    case3 = assign_judge(case3)
    case3 = run_all_exception_checks(case3, {
        "submitted_docs": ["Marriage Certificate", "Identity Proof", "Petition"],
        "petition_language": "Tamil",
        "fraud_score": 0.05
    })