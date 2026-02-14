#!/usr/bin/env python3
"""
AUTONOMOUS MULTI-AGENT ORCHESTRATOR
====================================
Main controller for WeddingFinder agent system.
Runs continuously, delegates tasks, enables agent-to-agent collaboration.
"""

import json
import os
import time
import subprocess
import sys
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
import signal

WORKSPACE = Path("C:/Users/eami/.openclaw/workspace")
TASKS_FILE = WORKSPACE / "TASKS.md"
COMM_LOG = WORKSPACE / "agent_comm_log.md"
AGENTS_DIR = Path("C:/Users/eami/.openclaw/agents")
LOG_FILE = WORKSPACE / "orchestrator.log"
QUEUE_FILE = WORKSPACE / "orchestrator_queue.json"

AGENTS = {
    "seo-specialist": {"handles": ["seo", "keyword", "search", "ranking"], "priority": 2},
    "frontend-dev": {"handles": ["frontend", "react", "ui", "component"], "priority": 2},
    "backend-dev": {"handles": ["backend", "api", "database", "supabase"], "priority": 2},
    "scraper-agent": {"handles": ["scrape", "crawl", "extract", "data"], "priority": 1},
    "content-writer": {"handles": ["write", "blog", "content", "article"], "priority": 2},
    "ux-designer": {"handles": ["design", "wireframe", "prototype"], "priority": 2},
    "lead-generator": {"handles": ["outreach", "email", "vendor", "lead"], "priority": 2},
    "devops-engineer": {"handles": ["deploy", "ci/cd", "pipeline", "netlify"], "priority": 3},
    "business-developer": {"handles": ["strategy", "business", "growth"], "priority": 3},
    "marketing-lead": {"handles": ["marketing", "campaign", "social"], "priority": 2},
    "ceo-weddingfinder": {"handles": ["plan", "coordinate", "review"], "priority": 5}
}

class Orchestrator:
    def __init__(self):
        self.running = True
        self.task_queue = []
        signal.signal(signal.SIGINT, self._stop)
        signal.signal(signal.SIGTERM, self._stop)
        self._log("AUTONOMOUS ORCHESTRATOR STARTED")
        self._log(f"Monitoring {TASKS_FILE}")
    
    def _stop(self, *args):
        self.running = False
        self._log("Shutting down...")
    
    def _log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {msg}"
        print(line)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    
    def _comm_log(self, agent, action, details=""):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n## {ts} - {agent}\n**Action:** {action}\n"
        if details:
            entry += f"**Details:** {details}\n"
        entry += "---\n"
        with open(COMM_LOG, "a", encoding="utf-8") as f:
            f.write(entry)
    
    def _detect_agent(self, desc):
        desc_lower = desc.lower()
        scores = {}
        for agent, cfg in AGENTS.items():
            score = sum(10 for kw in cfg["handles"] if kw in desc_lower)
            if score > 0:
                scores[agent] = score
        if scores:
            best = max(scores, key=scores.get)
            return best, scores[best]
        return "ceo-weddingfinder", 0
    
    def _parse_tasks(self):
        if not TASKS_FILE.exists():
            return []
        content = TASKS_FILE.read_text(encoding="utf-8")
        tasks = []
        for line in content.split("\n"):
            if line.strip().startswith("- [ ]"):
                desc = line.split("]", 1)[1].strip()
                tid = hashlib.md5(desc.encode()).hexdigest()[:10]
                tasks.append({"id": tid, "desc": desc})
        return tasks
    
    def _load_queue(self):
        if QUEUE_FILE.exists():
            try:
                with open(QUEUE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {"tasks": []}
        return {"tasks": []}
    
    def _save_queue(self, data):
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    
    def _spawn_agent(self, task_id, agent_id, desc):
        self._log(f"SPAWNING {agent_id} for task {task_id[:8]}")
        
        task_file = AGENTS_DIR / agent_id / "current_task.txt"
        task_file.parent.mkdir(parents=True, exist_ok=True)
        task_file.write_text(f"TASK_ID: {task_id}\nAGENT: {agent_id}\nDESC: {desc}\nTIME: {datetime.now().isoformat()}", encoding="utf-8")
        
        self._comm_log(agent_id, "TASK_ASSIGNED", f"Task: {desc[:60]}")
        
        # In real implementation, this would spawn a process
        # For now, we write the task and an agent session will pick it up
        self._log(f"  Task written to {task_file}")
        return True
    
    def run(self):
        self._log("Starting main loop...")
        while self.running:
            queue = self._load_queue()
            parsed = self._parse_tasks()
            
            existing = {t["id"] for t in queue["tasks"]}
            new_tasks = [p for p in parsed if p["id"] not in existing]
            
            for nt in new_tasks:
                agent, conf = self._detect_agent(nt["desc"])
                task = {
                    "id": nt["id"],
                    "desc": nt["desc"],
                    "agent": agent,
                    "status": "pending",
                    "created": datetime.now().isoformat(),
                    "started": None,
                    "completed": None
                }
                queue["tasks"].append(task)
                self._log(f"NEW TASK: {nt['desc'][:50]}... -> {agent}")
            
            # Process pending tasks
            for task in queue["tasks"]:
                if task["status"] == "pending":
                    if self._spawn_agent(task["id"], task["agent"], task["desc"]):
                        task["status"] = "assigned"
                        task["started"] = datetime.now().isoformat()
            
            self._save_queue(queue)
            
            self._log(f"Loop complete. {len(new_tasks)} new, {len([t for t in queue['tasks'] if t['status'] == 'pending'])} pending.")
            time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    orch = Orchestrator()
    orch.run()
