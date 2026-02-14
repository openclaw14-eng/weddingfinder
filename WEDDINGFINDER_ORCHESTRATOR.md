# WeddingFinder Agent Orchestrator

## Overview

The WeddingFinder platform is managed by a team of 11 specialized AI agents working together under the coordination of the CEO WeddingFinder agent. This document describes the orchestration system, task flow, and communication protocols.

## Agent Hierarchy

```
                    ┌─────────────────────┐
                    │  CEO WeddingFinder  │
                    │    (Orchestrator)   │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
   ┌────▼────┐           ┌────▼────┐           ┌────▼────┐
   │ Product │           │ Growth  │           │  Ops    │
   │  Team   │           │  Team   │           │  Team   │
   └────┬────┘           └────┬────┘           └────┬────┘
        │                      │                      │
   ┌────┴────┐            ┌───┴───┐            ┌───┴───┐
   │UX       │            │SEO    │            │DevOps │
   │Designer │            │Special│            │Engine│
   │Frontend │            │Content│            │       │
   │Developer│            │Writer │            │       │
   │Backend  │            │Lead   │            │       │
   │Developer│            │Gen    │            │       │
   │Scraper  │            │Business│            │       │
   │Agent    │            │Developer│            │       │
   │         │            │Marketing│            │       │
   │         │            │Lead     │            │       │
   └─────────┘            └─────────┘            └─────────┘
```

## Agent Roles Summary

| Agent | Team | Primary Function |
|-------|------|------------------|
| CEO WeddingFinder | Leadership | Orchestration, strategy, delegation |
| UX Designer | Product | User research, wireframes, usability |
| Frontend Developer | Product | UI implementation, client-side code |
| Backend Developer | Product | APIs, databases, server logic |
| Scraper Agent | Product | Data extraction, vendor data collection |
| SEO Specialist | Growth | Search optimization, rankings |
| Content Writer | Growth | Copy, blog posts, descriptions |
| Lead Generator | Growth | Vendor acquisition, outreach |
| Business Developer | Growth | Partnerships, revenue strategy |
| Marketing Lead | Growth | Campaigns, user acquisition |
| DevOps Engineer | Operations | Infrastructure, CI/CD, monitoring |

## Task Flow

### 1. Task Intake
- New tasks are written to `TASKS.md` in the workspace
- Tasks include: title, description, priority, required skills, dependencies

### 2. CEO Analysis
- CEO WeddingFinder reads `TASKS.md`
- Analyzes task requirements and complexity
- Determines which agent(s) are best suited
- Checks for dependencies and prerequisites

### 3. Task Delegation
- CEO assigns tasks to appropriate agents
- For complex tasks: breaks down into subtasks
- For multi-agent tasks: coordinates handoffs
- Sets deadlines and deliverable expectations

### 4. Execution
- Individual agents work on their assigned tasks
- Agents use their specialized skills
- Progress updates logged to workspace
- Blockers reported immediately to CEO

### 5. Review & Integration
- Completed work reviewed by CEO or senior agent
- Code reviewed by relevant developers
- Content reviewed for brand consistency
- Changes integrated into main codebase

### 6. Reporting
- Results written to `RESULTS.md`
- CEO updates task status
- Lessons learned documented
- Next steps identified

## Communication Protocol

### Message Format
```yaml
type: task | update | question | completion | blocker
from: agent_name
to: agent_name | all | ceo
timestamp: ISO8601
subject: brief description
body: detailed message
data:
  task_id: optional
  priority: low | medium | high | critical
  attachments: []
```

### Communication Rules
1. **Direct Communication**: Agents can communicate directly for clarifications
2. **Escalation**: Blockers and conflicts escalate to CEO
3. **Broadcasts**: Use `all` for announcements affecting multiple teams
4. **Documentation**: All decisions affecting architecture must be documented
5. **Async First**: Prefer written communication over meetings

### Status Updates
- **Daily**: Brief progress update to CEO
- **On Completion**: Full report with deliverables
- **On Blocker**: Immediate escalation with context
- **Weekly**: Team summary of accomplishments

## Task Assignment Logic

### Assignment Algorithm
```python
def assign_task(task):
    # 1. Extract required skills from task
    required_skills = task.skills_required
    
    # 2. Find agents with matching skills
    candidates = [agent for agent in agents 
                  if agent.has_skills(required_skills)]
    
    # 3. Filter by availability
    available = [agent for agent in candidates 
                 if agent.workload < agent.capacity]
    
    # 4. Score by skill match depth
    scored = [(agent, agent.skill_match_score(required_skills)) 
              for agent in available]
    
    # 5. Assign to highest scorer
    return max(scored, key=lambda x: x[1])[0]
```

### Skill-to-Agent Mapping
| Skill Category | Primary Agents | Secondary Agents |
|----------------|----------------|------------------|
| Web Development | Frontend Dev, Backend Dev | DevOps Engineer |
| Data Collection | Scraper Agent | Backend Dev |
| Content | Content Writer | SEO Specialist |
| Design | UX Designer | Frontend Dev |
| Growth | Marketing Lead | SEO Specialist, Lead Generator |
| Business | CEO, Business Developer | Marketing Lead |
| Operations | DevOps Engineer | Backend Dev |

## Conflict Resolution

### When Agents Disagree
1. **Technical Disagreements**: Senior agent decides (CEO or most experienced)
2. **Resource Conflicts**: CEO prioritizes based on business impact
3. **Design vs Technical**: UX Designer has final say on UX; Backend Dev on architecture
4. **Timeline Conflicts**: CEO adjusts deadlines or scope

### Escalation Path
```
Agent → Team Lead (if exists) → CEO → External (if needed)
```

## Success Metrics

### Team Metrics
- **Velocity**: Tasks completed per week
- **Quality**: Bug rate, review feedback scores
- **Collaboration**: Cross-team task completion rate
- **Innovation**: New ideas implemented

### Individual Agent Metrics
- **Completion Rate**: % of tasks completed on time
- **Quality Score**: Peer review ratings
- **Skill Growth**: New capabilities acquired
- **Collaboration**: Help provided to other agents

## Onboarding New Agents

When adding a new agent to the WeddingFinder team:
1. Create agent directory in `~/.openclaw/agents/{agent-name}/`
2. Write `agent.yaml` with name, role, skills, model
3. Add agent to this orchestrator documentation
4. Assign to appropriate team
5. CEO introduces new agent to relevant team members
6. Start with small tasks to build familiarity

---

*Last Updated: 2026-02-13*
*Version: 1.0*
*Maintainer: CEO WeddingFinder*