import json
from case_model import create_case

def triage_case(case):
    # Classify court type based on case type
    court_mapping = {
        "Civil": "Civil District Court",
        "Criminal": "Sessions Court",
        "Family": "Family Court",
        "Property": "Civil District Court",
        "Labour": "Labour Court",
        "Consumer": "Consumer Disputes Court"
    }

    # Urgency rules
    def calculate_urgency(case):
        score = case["urgency_score"]
        description = case["description"].lower()

        # Bump urgency if keywords detected
        if any(word in description for word in ["murder", "assault", "violence", "death"]):
            score = min(score + 3, 10)
        if any(word in description for word in ["child", "minor", "abuse"]):
            score = min(score + 2, 10)
        if any(word in description for word in ["property", "land", "boundary"]):
            score = max(score - 1, 1)

        return score

    # Assign priority label
    def get_priority(score):
        if score >= 8:
            return "CRITICAL"
        elif score >= 5:
            return "HIGH"
        elif score >= 3:
            return "MEDIUM"
        else:
            return "LOW"

    # Run triage
    case["urgency_score"] = calculate_urgency(case)
    case["priority"] = get_priority(case["urgency_score"])
    case["assigned_court"] = court_mapping.get(case["case_type"], "General Court")
    case["status"] = "TRIAGED"

    return case


# Test it
test_case = create_case(
    name="Rajesh Kumar",
    case_type="Civil",
    description="Murder case involving violence and assault",
    urgency=7
)

triaged = triage_case(test_case)
print(json.dumps(triaged, indent=4))