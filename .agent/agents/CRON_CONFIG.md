# Weddingfinder Cron Configuration

## OpenClaw Gateway Cron Jobs

Copy this to apply via `openclaw cron add` or config file:

```json
{
  "jobs": [
    {
      "id": "ceo-30min-check",
      "name": "CEO Priority Check - Every 30 Minutes",
      "schedule": {
        "kind": "every",
        "everyMs": 1800000
      },
      "payload": {
        "kind": "agentTurn",
        "message": "Review TASKS.md, identify next priority task, delegate to appropriate agent. If no tasks need attention, report 'All clear'."
      },
      "sessionTarget": "main",
      "delivery": {
        "mode": "announce",
        "channel": "telegram",
        "to": "868619775"
      },
      "enabled": true
    },
    {
      "id": "ceo-morning-check",
      "name": "CEO Morning Priority Check",
      "schedule": {
        "kind": "cron",
        "expr": "0 8 * * 1-7",
        "tz": "Europe/Amsterdam"
      },
      "payload": {
        "kind": "agentTurn",
        "message": "Full daily priority check: Review all agent progress from TASKS.md. Delegate highest priority pending task. Provide daily summary."
      },
      "sessionTarget": "main",
      "delivery": {
        "mode": "announce",
        "channel": "telegram",
        "to": "868619775"
      },
      "enabled": true
    },
    {
      "id": "scraper-daily",
      "name": "Scraper Agent - Daily Batch",
      "schedule": {
        "kind": "cron",
        "expr": "0 10 * * 1-7",
        "tz": "Europe/Amsterdam"
      },
      "payload": {
        "kind": "agentTurn",
        "message": "Run daily scraping batch. Review TASKS.md task 2.1-2.5. Prioritize: trouwlocaties first, then fotografen, bruidsmode, trouwpakken. Verify non-traceable before storing."
      },
      "sessionTarget": "main",
      "delivery": {
        "mode": "announce",
        "channel": "telegram",
        "to": "868619775"
      },
      "enabled": true
    },
    {
      "id": "devops-health-check",
      "name": "DevOps Daily Health Check",
      "schedule": {
        "kind": "cron",
        "expr": "0 12 * * 1-7",
        "tz": "Europe/Amsterdam"
      },
      "payload": {
        "kind": "agentTurn",
        "message": "Perform health check: API latency, app stability, uptime. Report to CEO. If any metric red, suggest fix."
      },
      "sessionTarget": "main",
      "delivery": {
        "mode": "announce",
        "channel": "telegram",
        "to": "868619775"
      },
      "enabled": true
    },
    {
      "id": "daily-summary",
      "name": "Daily Summary to CEO",
      "schedule": {
        "kind": "cron",
        "expr": "0 18 * * 1-7",
        "tz": "Europe/Amsterdam"
      },
      "payload": {
        "kind": "agentTurn",
        "message": "Compile daily summary: Tasks completed today, current progress on TASKS.md, any blockers. Report to CEO."
      },
      "sessionTarget": "main",
      "delivery": {
        "mode": "announce",
        "channel": "telegram",
        "to": "868619775"
      },
      "enabled": true
    }
  ]
}
```

## Apply Commands

### Via OpenClaw CLI

```bash
# View current cron jobs
openclaw cron list

# Add a job (from the JSON above, extract each job)
openclaw cron add --job '{"id": "ceo-30min-check", ...}'

# Or apply all from config file
openclaw config.patch --baseHash "..." --raw "[...jobs array...]"
```

### Manual Application

1. Run `openclaw cron list` to get current baseHash
2. Update config with new jobs array
3. Apply via `openclaw config.patch`

## Cron Schedule Summary

| Job | Schedule | Purpose |
|-----|----------|---------|
| CEO 30-min check | Every 30 min | Main delegation loop |
| CEO morning check | 08:00 daily | Full review + delegation |
| Scraper daily | 10:00 daily | Vendor data collection |
| DevOps health | 12:00 daily | System health check |
| Daily summary | 18:00 daily | Progress report |

## Expected Behavior

### Morning (08:00)
```
CEO wakes → Full TASKS.md review → Delegates priority tasks → Agents start working
```

### Every 30 Minutes
```
CEO checks → If tasks pending → Delegate to agent → Agent works → Reports back
```

### Daily (10:00)
```
Scraper Agent wakes → Runs scraping batch → Anonymizes data → Stores in Supabase
```

### Daily (12:00)
```
DevOps checks → API latency, uptime, errors → Reports status → Fix if needed
```

### Evening (18:00)
```
Daily summary → Report to CEO → Update on TASKS.md → Plan tomorrow
```

## Monitoring

CEO will receive Telegram notifications for:
- Task completions
- Blockers detected
- Daily summaries
- Emergency alerts

This keeps Ricky informed without needing to run cron jobs manually.