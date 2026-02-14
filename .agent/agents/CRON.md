# Weddingfinder Cron Jobs & Triggers

## Philosophy

**Wake every 30 minutes** to check if work needs to be done.  
**CEO determines priorities** based on GOALS.md metrics.  
**Agents only work when needed** (token efficient).

---

## Cron Schedule

### Every 30 Minutes (Priority Check & Delegation)

| Time | Trigger | Action | Agent |
|------|---------|--------|-------|
| :00 | CEO priority check | Review TASKS.md, delegate next task | CEO |
| :30 | CEO priority check | Review TASKS.md, delegate next task | CEO |

**What happens at each check:**
1. CEO reads TASKS.md to check progress
2. CEO identifies next task from priority list
3. CEO delegates to appropriate agent via `sessions_send` or `message`
4. Agent completes task, reports back to CEO
5. CEO updates TASKS.md progress
6. If all tasks for agent done → assign next
7. If all tasks complete → celebrate!

**CEO Decision Flow:**
```
READ TASKS.md → Check what's done/not done →
DECIDE: Which task needs work now? →
DELEGATE: Wake specific agent with task →
WAIT: Agent reports back →
UPDATE: Mark task complete or escalate →
SLEEP: Until next check (30 min later)
```

---

### Daily Triggers

| Time | Trigger | Action | Agent |
|------|---------|--------|-------|
| 08:00 | Daily start | CEO reviews overnight metrics | CEO |
| 09:00 | Content check | Publish scheduled content | Content Writer |
| 10:00 | Data sync | Scraper Agent - daily batch | Scraper Agent |
| 12:00 | Performance check | API/frontend health check | DevOps |
| 18:00 | Daily summary | Report to CEO | All active agents |

---

### Weekly Triggers

| Day | Time | Trigger | Action | Agent |
|-----|------|---------|--------|-------|
| Monday | 09:00 | Weekly review | KPI dashboard update | CEO |
| Monday | 10:00 | Outreach | Follow-up leads | Lead Generator |
| Tuesday | 09:00 | Content planning | Plan week's posts | Content Writer |
| Wednesday | 10:00 | Technical debt | Fixes and improvements | Dev Team |
| Thursday | 09:00 | Partnership check | Review pipeline | Business Developer |
| Friday | 16:00 | Sprint end | Report completion | All agents |
| Sunday | 22:00 | Weekly backup | Full database backup | DevOps |

---

### Monthly Triggers

| Day | Trigger | Action | Agent |
|-----|---------|--------|-------|
| Day 1 | Monthly planning | Set monthly OKRs | CEO |
| Day 5 | SEO report | Monthly keyword rankings | SEO Specialist |
| Day 10 | Financial review | Revenue metrics | Business Developer |
| Day 15 | Performance review | Slow queries, optimization | Backend Dev |
| Day 20 | Content audit | SEO content gap analysis | SEO Specialist |
| Day 25 | Partnership review | Pipeline status | Business Developer |
| Last day | Monthly review | Goal adjustment | CEO |

---

## Event-Based Triggers

### Scraper Triggers

| Event | Condition | Action |
|-------|-----------|--------|
| Batch complete | >50 new records | Notify Backend Dev to verify |
| Block detected | >3 errors in row | Reduce rate limit, backoff |
| Data quality check | Accuracy <90% | Alert CEO, pause scraping |

### Backend Triggers

| Event | Condition | Action |
|-------|-----------|--------|
| API error spike | >5% errors 5min | Alert DevOps, auto-rollback |
| High latency | p95 >500ms | Scale resources, alert |
| New endpoint | PR merged | Run tests, deploy preview |

### Frontend Triggers

| Event | Condition | Action |
|-------|-----------|--------|
| Crash rate | >1% in 1 hour | Alert Frontend Dev, rollback |
| Performance score | Lighthouse <80 | Notify for optimization |
| New release | PR merged | Deploy preview, test |

### Marketing Triggers

| Event | Condition | Action |
|-------|-----------|--------|
| Social milestone | +100 followers | Celebrate, report |
| Email campaign | Open rate <20% | A/B test subject lines |
| Content published | New post | Share on social channels |

---

## Agent Wake Logic

### Default State: SLEEPING

Agents only wake when triggered. This saves tokens and resources.

### Wake Conditions by Agent

| Agent | Wake Trigger | Wake For |
|-------|--------------|----------|
| CEO | Every 30 min | Priority evaluation |
| Scraper Agent | Daily 10:00 | New vendor data |
| Backend Dev | On data arrival | Store vendor data |
| Frontend Dev | On API ready | UI updates |
| UX Designer | Weekly | New design needs |
| SEO Specialist | Monday, Day 20 | Audit, optimization |
| Content Writer | Daily 09:00, Tuesday | Publish, plan |
| Marketing Lead | Monday, content publish | Social, campaigns |
| Lead Generator | Monday, Thursday | Outreach, follow-up |
| Business Developer | Thursday, Day 25 | Pipeline, review |
| DevOps | On deployment, Daily 12:00 | Health, deploys |

---

## Message Templates

### 1. Wake Signal
```markdown
[@agent-name]
Task: [brief description]
Context: [link to relevant docs]
Priority: [P0/P1/P2]
Deadline: [optional]

Complete task, report back, then sleep.
```

### 2. Task Complete
```markdown
[@ceo-weddingfinder]
Task: [task name]
Status: ✅ Complete
Result: [summary of output]
Next: [optional - what should happen next]
```

### 3. Blocker Report
```markdown
[@ceo-weddingfinder]
Blocker: [description]
Severity: [P0/P1/P2]
Can Continue: [yes/no - workaround]
```

---

## Monitoring Dashboard

### What CEO Checks Every 30 Minutes

| Metric | Green | Yellow | Red |
|--------|-------|--------|-----|
| Scraper progress | On schedule | <1 day behind | >1 day behind |
| Vendor count | At target | 20% below | 50% below |
| API latency | <200ms | <500ms | >500ms |
| App stability | >99.5% | 99-99.5% | <99% |
| Content schedule | On track | 1 post behind | 2+ posts behind |
| Outreach pace | On schedule | <20% behind | >20% behind |

---

## Cron Job Configuration

### For OpenClaw Gateway

```json
{
  "jobs": [
    {
      "id": "ceo-morning-check",
      "schedule": { "kind": "cron", "expr": "0 8 * * 1-5", "tz": "Europe/Amsterdam" },
      "payload": { "kind": "agentTurn", "message": "Run daily priority check from GOALS.md" },
      "sessionTarget": "main",
      "enabled": true
    },
    {
      "id": "scraper-daily",
      "schedule": { "kind": "cron", "expr": "0 10 * * 1-7", "tz": "Europe/Amsterdam" },
      "payload": { "kind": "agentTurn", "message": "Run daily scraping batch from Scraper Agent spec" },
      "sessionTarget": "main",
      "enabled": true
    },
    {
      "id": "content-morning",
      "schedule": { "kind": "cron", "expr": "0 9 * * 1-7", " "tz": "Europe/Amsterdam" },
      "payload": { "kind": "agentTurn", "message": "Publish scheduled content from Content Writer spec" },
      "sessionTarget": "main",
      "enabled": true
    }
  ]
}
```

---

## Priority Levels

| Priority | Description | Response Time | Examples |
|----------|-------------|---------------|----------|
| P0 | Critical - blocks launch | Immediate | App crashes, data loss |
| P1 | High - important feature | <4 hours | Search broken, auth fails |
| P2 | Medium - enhancement | <24 hours | New vendor field, polish |
| P3 | Low - nice to have | <1 week | Design tweaks, optimization |

---

## Emergency Protocol

**If P0 detected:**
1. DevOps alerted immediately
2. Frontend/Backend Dev woken
3. CEO monitors resolution
4. Rollback if needed
5. Post-mortem within 24 hours
