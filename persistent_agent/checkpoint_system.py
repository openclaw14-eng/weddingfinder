import json
import os
from datetime import datetime

CHECKPOINT_FILE = "persistent_agent/checkpoints.json"

def load_checkpoints():
    if not os.path.exists(CHECKPOINT_FILE):
        return {}
    try:
        with open(CHECKPOINT_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_checkpoint(task_name, status, data=None):
    checkpoints = load_checkpoints()
    checkpoints[task_name] = {
        "last_run": datetime.now().isoformat(),
        "status": status, # RUNNING, COMPLETED, FAILED
        "data": data or {}
    }
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(checkpoints, f, indent=4)

def get_last_run(task_name):
    checkpoints = load_checkpoints()
    return checkpoints.get(task_name)
