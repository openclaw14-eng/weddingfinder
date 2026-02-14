#!/usr/bin/env python3
"""
WeddingFinder Task Delegation System

Reads TASKS.md and delegates tasks to the appropriate WeddingFinder agent.
"""

import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime

AGENTS = {
    "seo-specialist": ["seo", "keyword", "search", "ranking", "backlink", "analytics"],
    "frontend-dev": ["frontend", "ui", "react", "javascript", "css", "html", "web"],
    "backend-dev": ["backend", "api", "database", "supabase", "server", "python"],
    "scraper-agent": ["scrape", "crawl", "data collection", "vendor", "extract"],
    "content-writer": ["content", "blog", "copy", "write", "article", "marketing copy"],
    "ux-designer": ["ux", "design", "wireframe", "prototype", "user experience"],
    "lead-generator": ["lead", "outreach", "vendor acquisition", "partnership", "sales"],
    "devops-engineer": ["deploy", "ci/cd", "infrastructure", "server", "netlify", "hosting"],
    "business-developer": ["business", "revenue", "partnership", "growth", "strategy"],
    "marketing-lead": ["marketing", "campaign", "social media", "ads", "branding"],
    "ceo-weddingfinder": ["strategy", "planning", "coordination", "roadmap", "vision"]
}

WORKSPACE = Path("C:/Users/eami/.openclaw/workspace")
AGENTS_DIR = Path("C:/Users/eami/.openclaw/agents")

def detect_agent(task_description: str) -> str:
    """Detect which agent should handle a task based on keywords."""
    task_lower = task_description.lower()
    scores = {}
    
    for agent, keywords in AGENTS.items():
        score = sum(1 for kw in keywords if kw in task_lower)
        if score > 0:
            scores[agent] = score
    
    if not scores:
        return "ceo-weddingfinder"
    
    return max(scores, key=scores.get)

def spawn_agent(agent_id: str, task: str, task_id: str = None):
    """Spawn an agent to execute a task."""
    if task_id is None:
        task_id = datetime.now().strftime("wf-%Y%m%d-%H%M%S")
    
    agent_dir = AGENTS_DIR / agent_id
    if not agent_dir.exists():
        print(f"[ERROR] Agent {agent_id} not found")
        return False
    
    print(f">> Spawning {agent_id} for task: {task_id}")
    print(f"   Task: {task[:80]}...")
    
    # Create task context
    context = f"""TASK ID: {task_id}
AGENT: {agent_id}
ASSIGNED: {datetime.now().isoformat()}

YOUR TASK:
{task}

INSTRUCTIONS:
1. Execute this task completely
2. Report progress via Telegram to user 868619775
3. Log results to task_execution_log.md
4. Mark task as completed when done

Start working immediately."""

    # Write context to agent's directory
    task_file = agent_dir / "current_task.txt"
    task_file.write_text(context, encoding="utf-8")
    
    print(f"   [OK] Task assigned to {agent_id}")
    print(f"   Context saved to: {task_file}")
    
    return True

def parse_tasks_md():
    """Parse TASKS.md and return list of pending tasks."""
    tasks_file = WORKSPACE / "TASKS.md"
    if not tasks_file.exists():
        print("No TASKS.md found")
        return []
    
    content = tasks_file.read_text(encoding="utf-8")
    
    # Simple parsing - look for unchecked tasks
    pending = []
    for line in content.split("\n"):
        if line.strip().startswith("- [ ]") or line.strip().startswith("* [ ]"):
            task_text = line.split("]", 1)[1].strip()
            pending.append(task_text)
    
    return pending

def main():
    print("=" * 60)
    print("WeddingFinder Task Delegation System")
    print("=" * 60)
    
    # Get pending tasks
    tasks = parse_tasks_md()
    
    if not tasks:
        print("\n[OK] No pending tasks found in TASKS.md")
        return
    
    print(f"\nFound {len(tasks)} pending task(s)\n")
    
    # Delegate each task
    for i, task in enumerate(tasks, 1):
        print(f"\n--- Task {i}/{len(tasks)} ---")
        agent = detect_agent(task)
        print(f"   Detected agent: {agent}")
        spawn_agent(agent, task, f"wf-{datetime.now().strftime('%Y%m%d')}-{i:03d}")
    
    print("\n" + "=" * 60)
    print(f"Delegation complete. Check task_execution_log.md for results.")
    print("=" * 60)

if __name__ == "__main__":
    main()
