import json
from datetime import datetime

def create_case(name, case_type, description, urgency):
    case = {
        "case_id": "NYC" + str(datetime.now().strftime("%Y%m%d%H%M%S")),
        "petitioner_name": name,
        "case_type": case_type,
        "description": description,
        "urgency_score": urgency,
        "status": "FILED",
        "assigned_court": None,
        "filed_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hearing_dates": [],
        "days_pending": 0,
        "escalated": False
    }
    return case

# Test it
new_case = create_case(
    name="Rajesh Kumar",
    case_type="Civil",
    description="Property dispute with neighbour over land boundary",
    urgency=7
)

print(json.dumps(new_case, indent=4))