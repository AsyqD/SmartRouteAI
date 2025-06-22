import json
from datetime import datetime

def log_classification(user_name, department, prompt, response_json, response_time):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",  # UTC time
        "user_name": user_name,
        "department": department,
        "prompt": prompt,
        "response_time": response_time,
        "response": response_json
    }

    # Save to JSONL file
    with open("logs/classification_logs.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False, indent=4) + "\n")