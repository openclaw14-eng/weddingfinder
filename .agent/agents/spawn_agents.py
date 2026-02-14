#!/usr/bin/env python3
"""
Weddingfinder Agent Startup Script
Spawns all isolated agent sessions for autonomous operation.
"""

import subprocess
import json
from datetime import datetime

# Agent configurations - each gets isolated session
AGENTS = {
    "scraper": {
        "agentId": "main",  # Using main with custom prompt
        "sessionKey": "scraper",
        "prompt_file": ".agent/agents/scraper-agent.md",
        "description": "Vendor data collection & anonymization"
    },
    "backend": {
        "agentId": "main",
        "sessionKey": "backend",
        "prompt_file": ".agent/agents/backend-dev.md",
        "description": "API & database development"
    },
    "frontend": {
        "agentId": "main",
        "sessionKey": "frontend",
        "prompt_file": ".agent/agents/frontend-dev.md",
        "description": "App & UI development"
    },
    "ux-designer": {
        "agentId": "main",
        "sessionKey": "ux-designer",
        "prompt_file": ".agent/agents/ux-designer.md",
        "description": "Design & research"
    },
    "seo": {
        "agentId": "main",
        "sessionKey": "seo",
        "prompt_file": ".agent/agents/seo-specialist.md",
        "description": "Search optimization"
    },
    "content": {
        "agentId": "main",
        "sessionKey": "content",
        "prompt_file": ".agent/agents/content-writer.md",
        "description": "Blog & copywriting"
    },
    "marketing": {
        "agentId": "main",
        "sessionKey": "marketing",
        "prompt_file": ".agent/agents/marketing-lead.md",
        "description": "Growth & campaigns"
    },
    "lead-gen": {
        "agentId": "main",
        "sessionKey": "lead-gen",
        "prompt_file": ".agent/agents/lead-generator.md",
        "description": "Vendor outreach"
    },
    "biz-dev": {
        "agentId": "main",
        "sessionKey": "biz-dev",
        "prompt_file": ".agent/agents/business-developer.md",
        "description": "Partnerships"
    },
    "devops": {
        "agentId": "main",
        "sessionKey": "devops",
        "prompt_file": ".agent/agents/devops-engineer.md",
        "description": "Infrastructure"
    }
}

def spawn_agent(name: str, config: dict):
    """Spawn an isolated agent session."""
    # Read the agent prompt file
    with open(config["prompt_file"], "r") as f:
        system_prompt = f.read()
    
    # Create isolated session
    cmd = [
        "openclaw",
        "sessions_spawn",
        "--agentId", config["agentId"],
        "--sessionKey", config["sessionKey"],
        "--task", f"You are the {name}. Follow your spec in {config['prompt_file']}. Wait for instructions from CEO. Report completion back.",
        "--cleanup", "keep"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

def main():
    print("🚀 Spawning Weddingfinder Agent Sessions")
    print(f"⏰ Time: {datetime.now().isoformat()}")
    print("-" * 50)
    
    spawned = []
    failed = []
    
    for name, config in AGENTS.items():
        print(f"📦 Spawning {name} ({config['description']})...")
        result = spawn_agent(name, config)
        
        if result.returncode == 0:
            print(f"   ✅ {name} spawned")
            spawned.append(name)
        else:
            print(f"   ❌ {name} failed: {result.stderr}")
            failed.append(name)
    
    print("-" * 50)
    print(f"✅ Success: {len(spawned)}/{len(AGENTS)} agents spawned")
    
    if failed:
        print(f"❌ Failed: {failed}")
    
    # Save status
    status = {
        "timestamp": datetime.now().isoformat(),
        "spawned": spawned,
        "failed": failed,
        "total": len(AGENTS)
    }
    
    with open(".agent/agents/agent-sessions.json", "w") as f:
        json.dump(status, f, indent=2)
    
    print("📁 Status saved to .agent/agents/agent-sessions.json")

if __name__ == "__main__":
    main()