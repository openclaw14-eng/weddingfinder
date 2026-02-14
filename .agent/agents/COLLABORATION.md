# Agent Workflows & Collaboration

## Trigger-Based Collaboration

### Workflow 1: New Vendor Data
```
Scraper Agent → Backend Dev → Frontend Dev → UX Designer
     ↓                ↓               ↓
  (collect)      (store in DB)   (update UI)   (verify design)
                            ↓
                      Notify CEO (via message)
```

**Trigger:** Scraper completes new batch  
**Action:** Auto-notify relevant agents via OpenClaw messaging

---

### Workflow 2: New Content Campaign
```
Marketing Lead → Content Writer → SEO Specialist → CEO
     ↓                ↓                ↓           ↓
  (plan)           (write)       (optimize)   (approve)
```

**Trigger:** Monthly content calendar update  
**Action:** Marketing Lead assigns topics, SEO provides keywords

---

### Workflow 3: Vendor Partnership
```
Lead Generator → Business Developer → CEO → Backend Dev
     ↓                   ↓               ↓          ↓
  (qualify)          (negotiate)    (approve)  (onboard)
```

**Trigger:** Lead converts to opportunity  
**Action:** Auto-create task for Business Developer

---

### Workflow 4: Technical Release
```
Frontend/Backend Dev → DevOps → All Teams
        ↓                ↓          ↓
    (develop)       (deploy)    (notify)
```

**Trigger:** PR merged to main  
**Action:** DevOps runs CI/CD, notifies teams

---

## Agent Communication Protocol

### Message Templates

**1. Request for Info**
```markdown
[@agent-name]
Request: [what you need]
Context: [relevant background]
Deadline: [optional]
```

**2. Handoff**
```markdown
[@next-agent]
From: [@previous-agent]
Completed: [what was done]
Next Step: [what needs to happen]
Notes: [important context]
```

**3. Blocker Report**
```markdown
[@ceo-weddingfinder]
Blocker: [description]
Blocked By: [who/what]
Impact: [severity]
Suggested Resolution: [optional]
```

---

## Collaboration Rules

| Situation | Primary Agent | Supporting Agents |
|-----------|---------------|-------------------|
| New vendor data | Scraper Agent | Backend Dev, UX Designer |
| Content planning | Marketing Lead | SEO Specialist, Content Writer |
| Partnership outreach | Lead Generator | Business Developer |
| Design system | UX Designer | Frontend Dev, Marketing Lead |
| API changes | Backend Dev | Frontend Dev, DevOps |
| Performance issues | DevOps | Backend Dev, Frontend Dev |
| SEO audit | SEO Specialist | Content Writer |
| Vendor onboarding | Business Developer | Backend Dev |

---

## Session Context Protocol

### Rule: Only load relevant agent files

**Main Context (always loaded - ~200 tokens):**
```
CONTEXT.md - Contains:
- All agent names and roles (1 line each)
- Current active agent
- Recent collaborations (last 3)
- Ongoing tasks
```

**Full Agent Files (lazy load - only when needed):**
```
.agent/agents/[agent-name].md
Loaded when:
- Agent is explicitly mentioned
- Task is in agent's domain
- CEO requests agent input
```

---

## Cross-Agent Messaging

Use OpenClaw `sessions_send` or `message` tool:

```markdown
To: lead-generator
Message: New venue data scraped from Amsterdam. 15 new entries. 
         Priority: high-value venues (>100 capacity). 
         Context: wedding-season-2026
```

---

## Review Cadence

| Meeting | Frequency | Attendees |
|---------|-----------|-----------|
| Standup | Weekly | All agents (rotating) |
| Strategy | Monthly | CEO + Leads |
| Handoff | Per-event | Relevant agents only |
