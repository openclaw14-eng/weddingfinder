# Weddingfinder Agent Organization

## Organizational Hierarchy

```
                    ┌─────────────────────┐
                    │  CEO Weddingfinder  │
                    │  (Strategy & Lead)  │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Marketing   │    │ Business Dev   │    │ Technology &    │
│   & Growth    │    │                 │    │ Data            │
└───────┬───────┘    └────────┬────────┘    └───────┬─────────┘
        │                      │                      │
   ┌────┴────┐            ┌────┴────┐         ┌──────┴──────┐
   │         │            │         │         │             │
   ▼         ▼            ▼         ▼         ▼             ▼
SEO       Marketing    Lead      Business  Scraper         UX
Spec.     Lead        Generator Developer  Agent           Designer

                                              │
                                              ▼
                                     ┌────────┴────────┐
                                     │                 │
                                     ▼                 ▼
                               Frontend Dev       Backend Dev
                                     │
                                     ▼
                               DevOps Engineer
```

## Division Responsibilities

### Marketing & Growth (reports to CEO)
- **SEO Specialist**: Organic search, content optimization, technical SEO
- **Marketing Lead**: Paid ads, social media, email, brand building
- **Content Writer**: Blog posts, marketing copy, localization

### Business Development (reports to CEO)
- **Lead Generator**: Prospecting, outreach, pipeline building
- **Business Developer**: Strategic partnerships, negotiations, revenue

### Technology & Data (reports to CEO)
- **Scraper Agent**: Vendor data collection, ETL pipelines
- **UX Designer**: User research, design system, prototypes
- **Frontend Dev**: React Native app, web dashboard
- **Backend Dev**: APIs, database, authentication
- **DevOps Engineer**: CI/CD, monitoring, infrastructure

## Collaboration Flows

### 1. Vendor Onboarding Flow
```
Scraper Agent → Backend Dev → Frontend Dev → UX Designer
   (collect)      (store)        (display)      (design)
                            ↑
                   Lead Generator (quality check)
```

### 2. Content Creation Flow
```
SEO Specialist → Content Writer → Marketing Lead
  (keywords)      (writing)        (publish)
                            ↑
                      CEO (strategy)
```

### 3. Partnership Flow
```
Lead Generator → Business Developer → CEO
 (prospect)       (negotiate)      (approve)
```

### 4. Marketing Campaign Flow
```
Marketing Lead → Content Writer → SEO Specialist
 (strategy)        (copy)           (optimize)
         ↓              ↓
    Social/Email    Analytics
```

## Data Flows

### Vendor Data Pipeline
```
Web Scraper → Validation → Supabase → API → Frontend
                                    ↓
                              DevOps (monitoring)
```

### User Data Flow
```
Frontend App → Auth → Backend API → Supabase
                    ↓
             Analytics → Marketing Lead
```

## Cross-Functional Meetings (Monthly)

| Meeting | Attendees | Purpose |
|---------|-----------|---------|
| Strategy Review | CEO + All Leads | QOKR review, priorities |
| Marketing Sync | SEO + Content + Marketing | Campaign planning |
| Tech Sync | All Devs + DevOps | Sprint planning, blockers |
| Partnership Review | Lead Gen + Business Dev | Pipeline status |

## Skills Directory

| Agent | Primary Skills |
|-------|---------------|
| CEO | strategic-planning, project-management, leadership |
| SEO Specialist | seo-fundamentals, analytics, content-strategy |
| Marketing Lead | growth-marketing, paid-ads, social-media |
| Content Writer | copywriting, i18n-localization, seo-fundamentals |
| Lead Generator | sales, crm, outreach |
| Business Developer | negotiation, strategic-thinking, revenue-management |
| Scraper Agent | python-patterns, database-design, bash-linux |
| UX Designer | mobile-design, user-research, design-systems |
| Frontend Dev | nextjs-react-expert, typescript, mobile-design |
| Backend Dev | python-patterns, database-design, security |
| DevOps Engineer | deployment-procedures, bash-linux, monitoring |

## KPI Dashboard

| Division | Key Metrics |
|----------|-------------|
| CEO | MAU, Revenue, LTV/CAC, Agent efficiency |
| Marketing | CAC, ROAS, Email CTR, Brand awareness |
| Business Dev | Partnership revenue, Vendor LTV, Renewal rate |
| Technology | Uptime, Response time, Crash-free rate |

## File Locations
All agent files: `.agent/agents/[agent-name].md`
