import json
from datetime import datetime, timedelta
from case_model import create_case
from triage_agent import triage_case
from court_assigner import assign_judge

def detect_stall(case, threshold_days=90):
    # Simulate days pending for testing
    case["days_pending"] = 95  # pretend this case has been sitting 95 days

    if case["days_pending"] > threshold_days:
        case["escalated"] = True
        case["escalation_reason"] = f"Case idle for {case['days_pending']} days — exceeds {threshold_days} day threshold"
        case["escalation_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        case["status"] = "ESCALATED"

        # Determine fast track court
        if case["priority"] == "CRITICAL":
            case["fast_track_court"] = "Supreme Court Fast Track Bench"
        elif case["priority"] == "HIGH":
            case["fast_track_court"] = "High Court Fast Track Division"
        else:
            case["fast_track_court"] = "District Fast Track Court"

        print("⚠️  ALERT: Case has been ESCALATED to fast track court!")
        print(f"    Reason: {case['escalation_reason']}")
        print(f"    Fast Track Court: {case['fast_track_court']}")
    else:
        print(f"✅ Case is within acceptable pending time ({case['days_pending']} days)")

    return case

# Test with a stalled case
test_case = create_case(
    name="Amit Singh",
    case_type="Property",
    description="Land boundary dispute pending for years with no hearing",
    urgency=5
)

triaged = triage_case(test_case)
assigned = assign_judge(triaged)
result = detect_stall(assigned)

print("\n--- Final Case State ---")
print(json.dumps(result, indent=4))