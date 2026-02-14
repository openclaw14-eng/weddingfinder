#!/usr/bin/env python3
"""
Multi-Agent Task Orchestrator

Main controller that:
- Reads TASKS.md continuously
- Maintains a task queue
- Spawns specialized agents for tasks
- Receives results from agents
- Updates task status
- Never stops until all tasks done
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
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional, List, Dict, Any
import threading
import signal

# Configuration
WORKSPACE = Path("C:/Users/eami/.openclaw/workspace/orchestrator")
TASKS_FILE = WORKSPACE / "TASKS.md"
QUEUE_FILE = WORKSPACE / "task_queue.json"
AGENTS_DIR = WORKSPACE / "agents"
RESULTS_DIR = WORKSPACE / "results"
LOG_FILE = WORKSPACE / "orchestrator.log"

# Ensure directories exist
AGENTS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


class TaskStatus(Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


@dataclass
class Task:
    id: str
    type: str  # scrape, code, research
    description: str
    status: str
    created_at: str
    assigned_to: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[str] = None
    error: Optional[str] = None
    retry_count: int = 0


class Orchestrator:
    def __init__(self):
        self.running = True
        self.active_agents: Dict[str, subprocess.Popen] = {}
        self.task_queue: List[Task] = []
        self.last_tasks_md_hash: Optional[str] = None
        self.check_interval = 5  # seconds
        self.max_retries = 3
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self._log("Orchestrator initialized")
    
    def _signal_handler(self, signum, frame):
        self._log(f"Received signal {signum}, initiating shutdown...")
        self.running = False
    
    def _log(self, message: str):
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    
    def _hash_file(self, filepath: Path) -> str:
        """Compute MD5 hash of file contents."""
        if not filepath.exists():
            return ""
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def _load_task_queue(self) -> List[Task]:
        """Load task queue from JSON file."""
        if not QUEUE_FILE.exists():
            return []
        try:
            with open(QUEUE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Task(**t) for t in data.get("tasks", [])]
        except Exception as e:
            self._log(f"Error loading task queue: {e}")
            return []
    
    def _save_task_queue(self):
        """Save task queue to JSON file."""
        try:
            data = {
                "updated_at": datetime.now().isoformat(),
                "tasks": [asdict(t) for t in self.task_queue]
            }
            with open(QUEUE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self._log(f"Error saving task queue: {e}")
    
    def _parse_tasks_md(self) -> List[Dict[str, Any]]:
        """Parse TASKS.md for new tasks.
        
        Format:
        ## Task: task_type
        Description of what needs to be done.
        [Optional metadata]
        """
        if not TASKS_FILE.exists():
            return []
        
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        tasks = []
        # Parse tasks with pattern: ## Task: <type>\n<description>
        pattern = r'##\s*Task:\s*(\w+)\s*\n\s*([^#]+?)(?=##|$)'
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        
        for task_type, description in matches:
            task_id = hashlib.md5(f"{task_type}:{description}".encode()).hexdigest()[:12]
            tasks.append({
                "id": task_id,
                "type": task_type.strip().lower(),
                "description": description.strip()
            })
        
        return tasks
    
    def _merge_new_tasks(self, parsed_tasks: List[Dict[str, Any]]):
        """Add new tasks from TASKS.md to the queue."""
        existing_ids = {t.id for t in self.task_queue}
        
        for pt in parsed_tasks:
            if pt["id"] not in existing_ids:
                task = Task(
                    id=pt["id"],
                    type=pt["type"],
                    description=pt["description"],
                    status=TaskStatus.PENDING.value,
                    created_at=datetime.now().isoformat()
                )
                self.task_queue.append(task)
                self._log(f"New task added: {task.id} ({task.type})")
    
    def _get_pending_tasks(self) -> List[Task]:
        """Get all pending or retrying tasks."""
        return [t for t in self.task_queue 
                if t.status in (TaskStatus.PENDING.value, TaskStatus.RETRYING.value)]
    
    def _find_agent_config(self, task_type: str) -> Optional[Path]:
        """Find agent configuration file for task type."""
        config_file = AGENTS_DIR / f"{task_type}_agent.json"
        if config_file.exists():
            return config_file
        # Try generic agent
        generic = AGENTS_DIR / "generic_agent.json"
        if generic.exists():
            return generic
        return None
    
    def _spawn_agent(self, task: Task):
        """Spawn an agent process to handle the task."""
        # Update task status
        task.status = TaskStatus.ASSIGNED.value
        task.assigned_to = f"agent_{task.type}_{task.id}"
        task.started_at = datetime.now().isoformat()
        self._save_task_queue()
        
        agent_config = self._find_agent_config(task.type)
        if not agent_config:
            task.status = TaskStatus.FAILED.value
            task.error = f"No agent configuration found for type: {task.type}"
            task.completed_at = datetime.now().isoformat()
            self._save_task_queue()
            self._log(f"Failed to spawn agent for task {task.id}: {task.error}")
            return
        
        # Create result directory for this task
        task_result_dir = RESULTS_DIR / task.id
        task_result_dir.mkdir(exist_ok=True)
        
        # Prepare agent command
        task_file = task_result_dir / "task.json"
        with open(task_file, "w", encoding="utf-8") as f:
            json.dump(asdict(task), f, indent=2)
        
        # Build agent command
        cmd = [
            sys.executable,
            "-c",
            f'''
import sys
sys.path.insert(0, r"{WORKSPACE}")
from agent_communication import AgentRunner
import json

with open(r"{task_file}", "r") as f:
    task = json.load(f)

runner = AgentRunner(task, r"{task_result_dir}")
runner.execute()
'''
        ]
        
        self._log(f"Spawning agent for task {task.id} ({task.type})")
        
        try:
            # Start agent process
            if sys.platform == "win32":
                proc = subprocess.Popen(
                    cmd,
                    stdout=open(task_result_dir / "stdout.log", "w"),
                    stderr=open(task_result_dir / "stderr.log", "w"),
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                )
            else:
                proc = subprocess.Popen(
                    cmd,
                    stdout=open(task_result_dir / "stdout.log", "w"),
                    stderr=open(task_result_dir / "stderr.log", "w"),
                    preexec_fn=os.setsid
                )
            
            self.active_agents[task.id] = proc
            task.status = TaskStatus.RUNNING.value
            self._save_task_queue()
            
        except Exception as e:
            task.status = TaskStatus.FAILED.value
            task.error = f"Failed to spawn agent: {str(e)}"
            task.completed_at = datetime.now().isoformat()
            self._save_task_queue()
            self._log(f"Error spawning agent: {e}")
    
    def _check_agent_results(self):
        """Check for completed agent results."""
        completed_tasks = []
        
        for task_id, proc in list(self.active_agents.items()):
            task = next((t for t in self.task_queue if t.id == task_id), None)
            if not task:
                continue
            
            # Check if process has finished
            retcode = proc.poll()
            
            if retcode is not None:
                # Process finished
                result_file = RESULTS_DIR / task_id / "result.json"
                
                if result_file.exists():
                    try:
                        with open(result_file, "r", encoding="utf-8") as f:
                            result_data = json.load(f)
                        
                        task.status = TaskStatus.COMPLETED.value if result_data.get("success") else TaskStatus.FAILED.value
                        task.result = result_data.get("result")
                        task.error = result_data.get("error")
                        task.completed_at = datetime.now().isoformat()
                        
                        self._log(f"Task {task_id} completed: {task.status}")
                        
                    except Exception as e:
                        task.status = TaskStatus.FAILED.value
                        task.error = f"Error reading result: {str(e)}"
                        task.completed_at = datetime.now().isoformat()
                        self._log(f"Error reading result for {task_id}: {e}")
                else:
                    # No result file - agent probably crashed
                    if task.retry_count < self.max_retries:
                        task.status = TaskStatus.RETRYING.value
                        task.retry_count += 1
                        self._log(f"Task {task_id} failed, retrying ({task.retry_count}/{self.max_retries})")
                    else:
                        task.status = TaskStatus.FAILED.value
                        task.error = f"Agent exited with code {retcode}, no result file"
                        task.completed_at = datetime.now().isoformat()
                        self._log(f"Task {task_id} failed after {self.max_retries} retries")
                
                completed_tasks.append(task_id)
                self._save_task_queue()
        
        # Remove completed from active agents
        for task_id in completed_tasks:
            del self.active_agents[task_id]
    
    def _cleanup_old_results(self):
        """Clean up results older than 7 days."""
        cutoff = datetime.now().timestamp() - (7 * 24 * 3600)
        for result_dir in RESULTS_DIR.iterdir():
            if result_dir.is_dir():
                mtime = result_dir.stat().st_mtime
                if mtime < cutoff:
                    import shutil
                    shutil.rmtree(result_dir)
                    self._log(f"Cleaned up old results: {result_dir.name}")
    
    def _all_tasks_done(self) -> bool:
        """Check if all tasks are completed or failed."""
        if not self.task_queue:
            return False  # Keep running to check for new tasks
        
        active_states = {TaskStatus.PENDING.value, TaskStatus.ASSIGNED.value, 
                        TaskStatus.RUNNING.value, TaskStatus.RETRYING.value}
        
        return not any(t.status in active_states for t in self.task_queue)
    
    def _get_stats(self) -> Dict[str, int]:
        """Get task statistics."""
        stats = {
            "pending": 0, "assigned": 0, "running": 0,
            "completed": 0, "failed": 0, "retrying": 0,
            "total": len(self.task_queue)
        }
        for t in self.task_queue:
            stats[t.status] = stats.get(t.status, 0) + 1
        return stats
    
    def run(self):
        """Main orchestrator loop."""
        self._log("=" * 60)
        self._log("Orchestrator started")
        self._log("=" * 60)
        
        # Load existing queue
        self.task_queue = self._load_task_queue()
        self._log(f"Loaded {len(self.task_queue)} tasks from queue")
        
        empty_cycles = 0
        max_empty_cycles = 12  # ~1 minute of idle before considering shutdown
        
        while self.running:
            try:
                # Check if TASKS.md has changed
                current_hash = self._hash_file(TASKS_FILE)
                if current_hash != self.last_tasks_md_hash:
                    self._log("TASKS.md changed, parsing...")
                    parsed_tasks = self._parse_tasks_md()
                    self._merge_new_tasks(parsed_tasks)
                    self.last_tasks_md_hash = current_hash
                
                # Check for completed agent results
                self._check_agent_results()
                
                # Spawn agents for pending tasks
                pending = self._get_pending_tasks()
                
                if pending:
                    empty_cycles = 0
                    for task in pending[:5]:  # Limit concurrent tasks
                        if task.id not in self.active_agents:
                            self._spawn_agent(task)
                else:
                    empty_cycles += 1
                
                # Periodic cleanup
                if empty_cycles % 60 == 0:
                    self._cleanup_old_results()
                
                # Log status periodically
                if empty_cycles % 6 == 0:
                    stats = self._get_stats()
                    self._log(f"Status: {stats}")
                
                # Check if we should exit (no pending tasks and no active agents)
                if self._all_tasks_done() and not self.active_agents:
                    if empty_cycles >= max_empty_cycles:
                        self._log("No pending tasks, shutting down")
                        break
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                self._log(f"Error in main loop: {e}")
                time.sleep(self.check_interval)
        
        # Cleanup
        self._log("Shutting down, cleaning up active agents...")
        for task_id, proc in self.active_agents.items():
            try:
                if sys.platform == "win32":
                    proc.terminate()
                else:
                    import signal
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except Exception as e:
                self._log(f"Error terminating agent {task_id}: {e}")
        
        self._log("Orchestrator stopped")


def main():
    orchestrator = Orchestrator()
    orchestrator.run()


if __name__ == "__main__":
    main()
