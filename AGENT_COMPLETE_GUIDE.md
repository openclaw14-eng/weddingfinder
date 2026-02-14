# Auto-Complete Setup Instructions

## For Agents to Auto-Report Completion

Add this to the END of every agent's task execution:

```python
# At end of agent task
import subprocess
subprocess.run([
    "python", 
    "C:\\Users\\eami\\.openclaw\\workspace\\agent_complete.py",
    "TASK_ID_HERE",
    "AGENT_NAME_HERE", 
    "Brief result summary"
])
```

## Manual Usage

```bash
# Mark scraper task complete
python agent_complete.py abf7d6bf72 scraper-agent "Scraped 20 venues successfully"

# Mark content-writer complete  
python agent_complete.py 63842a10ba content-writer "Wrote 7000 word blog post"
```

## Creating Followup Tasks

Agents can create tasks for other agents:

```python
from agent_complete import create_followup_task

# After scraping, create task for writer
create_followup_task(
    "content-writer",
    "Write blog post based on scraped venue data",
    parent_task_id="abf7d6bf72"
)
```

## Current Queue Status

Check: `orchestrator_queue.json`

Status values:
- pending: Waiting to start
- assigned: Currently running
- completed: Done ✓
- failed: Error occurred
- blocked: Waiting on dependency
