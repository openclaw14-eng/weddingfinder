#!/usr/bin/env python3
"""
AGENT TASK COMPLETION SYSTEM
============================
Agents call this to report task completion back to orchestrator.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("C:/Users/eami/.openclaw/workspace")
QUEUE_FILE = WORKSPACE / "orchestrator_queue.json"
COMM_LOG = WORKSPACE / "agent_comm_log.md"

def log_action(agent, action, details=""):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n## {ts} - {agent}\n**Action:** {action}\n"
    if details:
        entry += f"**Details:** {details}\n"
    entry += "---\n"
    with open(COMM_LOG, "a", encoding="utf-8") as f:
        f.write(entry)

def mark_task_complete(task_id, agent, result_summary=""):
    """Mark a task as completed in the orchestrator queue."""
    print(f"[{agent}] Marking task {task_id} as COMPLETED")
    
    if not QUEUE_FILE.exists():
        print(f"[ERROR] Queue file not found")
        return False
    
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            queue = json.load(f)
        
        found = False
        for task in queue.get("tasks", []):
            if task["id"].startswith(task_id) or task_id.startswith(task["id"]):
                task["status"] = "completed"
                task["completed"] = datetime.now().isoformat()
                task["result_summary"] = result_summary[:200] if result_summary else "Task completed successfully"
                found = True
                print(f"  [OK] Task {task['id']} marked completed")
                log_action(agent, "TASK_COMPLETED", f"Task {task['id']}: {result_summary[:100]}")
                break
        
        if not found:
            print(f"  [WARN] Task {task_id} not found in queue")
            # Add completion entry anyway
            log_action(agent, "TASK_COMPLETED", f"Task {task_id} (orphaned): {result_summary[:100]}")
        
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=2)
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def create_followup_task(for_agent, description, parent_task_id=""):
    """Create a new task for another agent."""
    import hashlib
    
    task_id = hashlib.md5(f"{for_agent}:{description}".encode()).hexdigest()[:10]
    
    if not QUEUE_FILE.exists():
        queue = {"tasks": []}
    else:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            queue = json.load(f)
    
    task = {
        "id": task_id,
        "desc": description,
        "agent": for_agent,
        "status": "pending",
        "created": datetime.now().isoformat(),
        "started": None,
        "completed": None,
        "parent_task": parent_task_id
    }
    
    queue["tasks"].append(task)
    
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2)
    
    log_action("ORCHESTRATOR", "FOLLOWUP_CREATED", f"For {for_agent}: {description[:60]}")
    print(f"  [OK] Created followup task {task_id} for {for_agent}")
    return task_id

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: agent_complete.py <task_id> <agent_name> [result_summary]")
        print("Example: agent_complete.py abf7d6bf72 scraper-agent 'Scraped 20 venues'")
        sys.exit(1)
    
    task_id = sys.argv[1]
    agent = sys.argv[2]
    result = sys.argv[3] if len(sys.argv) > 3 else ""
    
    success = mark_task_complete(task_id, agent, result)
    sys.exit(0 if success else 1)
