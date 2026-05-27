import json
from datetime import datetime
from case_model import create_case
from triage_agent import triage_case

# Available judges and their courts
judges = [
    {"judge_id": "J001", "name": "Justice Mehta", "court": "Civil District Court", "available": True, "current_cases": 12},
    {"judge_id": "J002", "name": "Justice Sharma", "court": "Civil District Court", "available": True, "current_cases": 8},
    {"judge_id": "J003", "name": "Justice Rao", "court": "Sessions Court", "available": True, "current_cases": 15},
    {"judge_id": "J004", "name": "Justice Khan", "court": "Sessions Court", "available": False, "current_cases": 20},
    {"judge_id": "J005", "name": "Justice Verma", "court": "Family Court", "available": True, "current_cases": 6},
    {"judge_id": "J006", "name": "Justice Iyer", "court": "Labour Court", "available": True, "current_cases": 9},
]

def assign_judge(case):
    assigned_court = case["assigned_court"]
    priority = case["priority"]

    # Filter judges by court and availability
    eligible_judges = [
        j for j in judges
        if j["court"] == assigned_court and j["available"]
    ]

    if not eligible_judges:
        case["status"] = "PENDING_JUDGE"
        case["assigned_judge"] = None
        case["assignment_note"] = "No available judges in this court — escalating"
        return case

    # For CRITICAL cases pick judge with least cases
    # For others pick randomly from eligible
    if priority == "CRITICAL":
        assigned = min(eligible_judges, key=lambda j: j["current_cases"])
    else:
        assigned = eligible_judges[0]

    case["assigned_judge"] = assigned["name"]
    case["judge_id"] = assigned["judge_id"]
    case["status"] = "ASSIGNED"
    case["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return case

# Test it
test_case = create_case(
    name="Priya Patel",
    case_type="Criminal",
    description="Murder case involving violence and assault",
    urgency=8
)

triaged = triage_case(test_case)
assigned = assign_judge(triaged)
print(json.dumps(assigned, indent=4))