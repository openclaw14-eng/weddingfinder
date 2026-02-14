# Weddingfinder Self-Healing & Error Protocol

## Philosophy

**No task should fail silently.**  
**Errors should trigger automatic recovery.**  
**CEO should only escalate P0 issues to Ricky.**

---

## Error Levels

| Level | Type | Auto-Action | Report To |
|-------|------|-------------|-----------|
| L1 | Minor (typo, formatting) | Fix silently | None |
| L2 | Recoverable (retry works) | Retry 3x, then fix | None |
| L3 | Blocking (dependency missing) | Escalate to CEO | CEO only |
| L4 | Critical (data loss, security) | Alert CEO, pause | Ricky + CEO |
| L5 | System (crash, infra) | Emergency protocol | Ricky + CEO |

---

## Self-Healing Actions

### L1: Minor Errors (Auto-Fix)
```
Examples: Typo, formatting, missing import, lint error

Auto-Action:
1. Detect error
2. Fix the issue
3. Continue work
4. Log fix in ERROR_LOG.md
5. No report needed
```

### L2: Recoverable Errors (Retry + Fix)
```
Examples: Network timeout, API rate limit, file not found

Auto-Action:
1. Detect error
2. Wait 30 seconds (exponential backoff)
3. Retry operation
4. If still fails → Try alternative approach
5. If still fails → Mark as L3, escalate to CEO
```

### L3: Blocking Errors (CEO Escalation)
```
Examples: Missing dependency, contradictory requirements, 
          permission denied, API key missing

CEO Auto-Action:
1. Receive L3 error
2. Analyze the blocker
3. Try 2 resolution approaches
4. If resolved → Continue task
5. If still blocked → Create ISSUE.md entry
6. If impacts timeline → Report to Ricky (next morning)
```

### L4: Critical Errors (Emergency Stop)
```
Examples: Data breach risk, data corruption, security vulnerability

Auto-Action:
1. Pause all tasks immediately
2. Alert CEO (emergency mode)
3. CEO assesses damage
4. If severe → Alert Ricky (SMS/priority)
5. Fix before any other work
```

### L5: System Errors (Full Recovery)
```
Examples: Gateway crash, total session loss, database corruption

Emergency Protocol:
1. DevOps mode activates
2. Assess system health
3. Restore from backup if needed
4. Resume from last checkpoint
5. Full report to Ricky + CEO
```

---

## Checkpoint System

Every task creates a checkpoint:

```markdown
# Checkpoint: [Task ID] - [Timestamp]

**Status:** IN_PROGRESS / COMPLETE / FAILED
**Agent Mode:** [Frontend/Backend/etc]
**Files Modified:** [list]
**Data Saved:** [summary]
**Last Action:** [what was being done]
**Next Step:** [what would happen next]

**Resume From Here If:**
- Session crashed
- Task interrupted
- Need to continue later
```

### Resume Protocol
```
If session crashes:
1. New session starts
2. CEO reads TASKS.md → sees Task X is IN_PROGRESS
3. CEO reads Checkpoint X
4. CEO determines: continue or restart
5. Agent continues from checkpoint
```

---

## Dependency Checker

Before starting any task, agent checks:

```python
dependency_check(task_id):
    """
    Returns: (ready: bool, missing: list, alternatives: list)
    """
    if task == "1.1 Project Setup":
        required = ["Expo SDK", "Supabase connection"]
        missing = check_dependencies(required)
        alternatives = provide_alternatives(missing)
        return (len(missing) == 0, missing, alternatives)
    
    if task == "3.1 Search":
        required = ["Backend API", "Database with vendors"]
        missing = check_dependencies(required)
        return (len(missing) == 0, missing, alternatives)
```

---

## Error Logging

All errors logged to `.agent/agents/ERROR_LOG.md`:

```markdown
# Error Log - Weddingfinder

## 2026-02-13 01:30
- Task: 1.1 Project Setup
- Agent: Frontend Mode
- Error: Supabase connection timeout
- Level: L2 (Recoverable)
- Action: Retried 3x, succeeded on 2nd attempt
- Resolved: Yes

## 2026-02-13 02:15
- Task: 2.1 Scraper Setup
- Agent: Scraper Mode
- Error: robots.txt blocked scraping
- Level: L3 (Blocking)
- Action: Escalated to CEO
- Resolution: CEO decided to respect robots.txt, switch source
- Resolved: Yes
```

---

## CEO Error Handling

CEO checks for errors every cycle:

```
CEO Error Check:
1. Read ERROR_LOG.md
2. Count unresolved L3+ errors
3. If L4/L5 detected → Emergency mode
4. If L3 exists → Assign to appropriate agent
5. If all clear → Continue normal delegation
```

---

## Telegram Alert Thresholds

| Issue Type | Alert Ricky? | Timing |
|------------|--------------|--------|
| L1 Error | No | Never |
| L2 Error | No | Never |
| L3 Error | No | Only if blocked >24h |
| L4 Error | Yes | Immediate |
| L5 Error | Yes | Immediate |

**Summary:** Ricky wordt alleen gebeld bij Critical (L4/L5) of langdurige blockers (L3 >24h).

---

## Daily Error Report (08:00)

At 08:00, CEO includes in daily report:

```
📊 **Ochtend Update**

**Errors Last 24h:**
- L1: 3 (all auto-fixed)
- L2: 2 (retried, resolved)
- L3: 1 (resolved by CEO)
- L4/L5: 0 ✅

**Currently Blocked:**
- Task 3.1: Waiting for API (estimated: 2 hours)

**System Health:** ✅ All systems operational
```

---

## Test Protocol

Every new task should have:

```markdown
## Test Criteria
- [ ] Task completes without L3+ errors
- [ ] L1/L2 errors are self-healed
- [ ] Checkpoint created on completion
- [ ] ERROR_LOG.md updated
- [ ] TASKS.md status updated
```

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| L3+ Error Rate | <1 per day | 0 |
| Self-Heal Rate | >90% of L1/L2 | 0% (measuring) |
| Mean Time to Recovery | <30 min | - |
| Blocked Tasks | 0 | 0 |

---

## No User Intervention Required

**The System Handles:**
- ✅ Minor errors (auto-fix)
- ✅ Network retries (exponential backoff)
- ✅ Dependency checking (before starting)
- ✅ Checkpoints (resume after crash)
- ✅ Error logging (for analysis)
- ✅ CEO escalation (for blocking issues)

**Only Escalates to Ricky:**
- Critical data/security issues (L4/L5)
- Blocking issues >24 hours (L3)
- System-wide failures (L5)

---

## Command Reference (For Ricky)

If something goes seriously wrong:

```bash
# View all errors
cat .agent/agents/ERROR_LOG.md

# Force a health check
openclaw cron run [devops-job-id] --force

# View current status
openclaw cron list

# Check TASKS.md progress
cat .agent/agents/TASKS.md
```

**Otherwise:** The system handles everything. Ricky only intervenes on L4/L5 issues.