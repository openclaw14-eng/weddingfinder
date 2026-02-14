# Weddingfinder Autonomous System

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MAIN SESSION                             │
│  (All agents share this session, different modes)          │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      CEO MODE                               │
│  - Reads TASKS.md for progress                              │
│  - Decides next priority                                    │
│  - Delegates to other modes                                 │
│  - Reports to Ricky                                        │
│  Activated: Every 30 min by cron                           │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   AGENT MODES                               │
│                                                             │
│  SCRAPER MODE   → Vendor data collection                    │
│  BACKEND MODE  → API & database                            │
│  FRONTEND MODE → App & UI                                  │
│  UX MODE       → Design & research                         │
│  SEO MODE      → Search optimization                       │
│  CONTENT MODE  → Blog & copywriting                        │
│  MARKETING MODE→ Growth & campaigns                        │
│  LEAD-GEN MODE → Vendor outreach                           │
│  BIZ-DEV MODE  → Partnerships                              │
│  DEVOPS MODE   → Infrastructure                            │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      TASKS.md                               │
│  (Single source of truth for all progress)                 │
└─────────────────────────────────────────────────────────────┘
```

---

## How It Works

### Every 30 Minutes (Cron Trigger)
```
System Event: "CEO Priority Check"
    ↓
CEO Mode Activated
    ↓
1. Read TASKS.md
2. Identify next priority
3. Decide which agent mode should work
4. Switch to that agent mode (set system prompt)
5. Agent works on task
6. Report back to CEO
7. CEO updates TASKS.md
8. CEO reports to Ricky (Telegram)
```

### Mode Switching
```
CEO Mode (coordination)
    ↓ switch_context(agent_mode)
SCRAPER MODE (focus on scraping)
    ↓ switch_context(agent_mode)
BACKEND MODE (focus on API)
    ↓ switch_context(agent_mode)
...
```

---

## Agent Mode Specs

### SCRAPER MODE
```markdown
Active when: TASKS.md tasks 2.1-2.5 need work

System Prompt:
"You are the Scraper Agent. Your priorities:
1. Scrape vendor data from wedding platforms
2. Anonymize all data (NO source URLs)
3. Store in Supabase
4. Report completion to CEO

Current focus: [read from TASKS.md]
```

### BACKEND MODE
```markdown
Active when: TASKS.md tasks 1.3, 3.1, 3.2 need work

System Prompt:
"You are the Backend Developer. Your priorities:
1. Build APIs for the app
2. Design database schema
3. Implement search endpoints
4. Handle authentication
5. Report completion to CEO

Current focus: [read from TASKS.md]"
```

### FRONTEND MODE
```markdown
Active when: TASKS.md tasks 1.1, 1.2, 1.4, 1.5, 3.1-3.5 need work

System Prompt:
"You are the Frontend Developer. Your priorities:
1. Build the Expo/React Native app
2. Implement screens (search, profiles, favorites)
3. Connect to Supabase
4. Optimize for performance
5. Report completion to CEO

Current focus: [read from TASKS.md]"
```

### UX MODE
```markdown
Active when: TASKS.md needs design work

System Prompt:
"You are the UX Designer. Your priorities:
1. Create user flows
2. Design components
3. Research user needs
4. Maintain design system
5. Report completion to CEO

Current focus: [read from TASKS.md]"
```

### And so on for all modes...
(See individual agent files for full specs)
```

---

## Cron Schedule (All in Main Session)

| Time | Trigger | Mode | Task |
|------|---------|------|------|
| */30 | CEO check | CEO | Review TASKS.md, delegate |
| 08:00 | Morning | CEO | Full daily review + delegate |
| 10:00 | Scraper | SCRAPER | Daily scraping batch |
| 12:00 | DevOps | DEVOPS | Health check |
| 18:00 | Summary | CEO | Daily summary + report |

---

## Delegation Flow (Within Main Session)

```
CEO Mode:
  "I need to assign Task 1.1 (Project Setup)"
  "This is Frontend work"
  → Switch to FRONTEND MODE
  → Agent reads TASKS.md, completes task
  → Agent reports: "Task 1.1 complete"
  → Switch back to CEO MODE
  → CEO updates TASKS.md
```

---

## TASKS.md (Single Source of Truth)

```markdown
# Weddingfinder Tasks

## Priority 1: APP FOUNDATION
- [ ] 1.1 Project setup (Frontend Mode)
- [ ] 1.2 User authentication (Frontend Mode)
- [ ] 1.3 Database schema (Backend Mode)
- [ ] 1.4 Navigation (Frontend Mode)
- [ ] 1.5 Basic components (Frontend/UX Mode)

## Priority 2: VENDOR DATA
- [ ] 2.1 Scraper setup (Scraper Mode)
- [ ] 2.2 Anonymization (Scraper Mode)
- [ ] 2.3 Data storage (Backend Mode)
- [ ] 2.4 500 records (Scraper Mode)
- [ ] 2.5 1000 records (Scraper Mode)

## Priority 3: CORE FEATURES
- [ ] 3.1 Search (Backend + Frontend Mode)
- [ ] 3.2 Profiles (Frontend Mode)
- [ ] 3.3 Favorites (Backend + Frontend Mode)
- [ ] 3.4 User profile (Frontend Mode)
- [ ] 3.5 Contact (Backend Mode)

## Priority 4: SEO OPTIMIZATION
- [ ] 4.1 Audit (SEO Mode)
- [ ] 4.2 Meta tags (Frontend + SEO Mode)
- [ ] 4.3 Schema markup (Backend + SEO Mode)
- [ ] 4.4 Sitemap (Backend Mode)
- [ ] 4.5 Robots.txt (Backend Mode)
- [ ] 4.6 Performance (Frontend + DevOps Mode)

## Priority 5: POLISH & LAUNCH
- [ ] 5.1 Accessibility (UX Mode)
- [ ] 5.2 Error handling (All Dev Modes)
- [ ] 5.3 Loading states (Frontend Mode)
- [ ] 5.4 Dark mode (Frontend Mode)
- [ ] 5.5 Production (DevOps Mode)
- [ ] 5.6 Launch (CEO Mode)
```

---

## Benefits of This Architecture

1. **Token Efficient**: Single session, mode switching
2. **Simple**: No complex session management
3. **Clear Progress**: TASKS.md is single source of truth
4. **Scalable**: Easy to add new modes
5. **Autonomous**: Runs without manual intervention

---

## Telegram Integration

CEO reports to Ricky after each delegation cycle:

```
📊 **Weddingfinder Update**

**Today:**
- ✅ Task 1.1: Project setup (Frontend)
- ✅ Task 2.3: Data storage (Backend)

**In Progress:**
- 🔄 Task 1.2: Authentication (Frontend)
- 🔄 Task 2.1: Scraper setup (Scraper)

**Next:**
- Assigning Task 3.1: Search → Frontend Mode

**Progress:** 5/27 tasks (18%)
```

---

## Startup

When OpenClaw starts:
1. Main session initializes
2. Cron jobs start (every 30 min, daily)
3. CEO mode activates first
4. CEO reads TASKS.md, begins delegation

No manual agent spawning needed - mode switching happens within the main session.