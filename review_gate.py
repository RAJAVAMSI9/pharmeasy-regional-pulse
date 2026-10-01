import json
import uuid
from datetime import datetime, timezone

def review_gate_v1(report, decision, reviewer_note=""):

    # Rule 1: decision must be one of these 3 -- reject anything else
    if decision != "approve" and decision != "edit" and decision != "reject":
        raise ValueError("Invalid decision: " + decision)

    # Rule 2: build the log entry -- must have exactly these 5 fields
    timestamp = str(datetime.now(timezone.utc))
    run_id = str(uuid.uuid4())
    region = report.get("region", "UNKNOWN")

    log_entry = {
        "timestamp": timestamp,
        "run_id": run_id,
        "region": region,
        "decision": decision,
        "reviewer_note": reviewer_note
    }

    # Rule 3: append this entry as one line to the audit log file
    f = open('audit_log.jsonl', 'a')
    f.write(json.dumps(log_entry))
    f.write("\n")
    f.close()

    # Rule 4: return an updated copy, showing the decision was recorded
    updated_report = dict(report)
    updated_report["decision"] = decision
    updated_report["reviewer_note"] = reviewer_note
    updated_report["downstream_allowed"] = (decision == "approve")

    return updated_report

test1 = review_gate_v1({"region": "Guntur"}, "approve", "Numbers verified, ready for dashboard.")
print(test1)

test2 = review_gate_v1({"region": "Bengaluru"}, "edit", "Wording needs softening.")
print(test2)

test3 = review_gate_v1({"region": "Karimnagar"}, "reject", "Sample size too small.")
print(test3)

try:
    review_gate_v1({"region": "Nellore"}, "maybe", "testing bad input")
except ValueError as e:
    print("Correctly rejected:", e)
