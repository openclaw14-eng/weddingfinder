# WeddingFinder Multi-Agent System

## Overview
11 gespecialiseerde AI agents werken samen onder leiding van een delegatie systeem.

## Hoe het werkt

### 1. Taken toevoegen
Zet je taak in `TASKS.md` met `- [ ]` voor de taak:
```markdown
- [ ] Schrijf blog post over bruidsmode trends 2026
```

### 2. Delegatie triggeren
Run:
```bash
python delegate.py
```

### 3. Auto-detectie
Het systeem analyseert elke taak en kiest de beste agent:
- "SEO keywords" → seo-specialist
- "React component" → frontend-dev
- "Scrape venues" → scraper-agent
- "Blog post" → content-writer
- etc.

### 4. Agent ontvangt taak
De agent krijgt een `current_task.txt` file in zijn directory met:
- Taak beschrijving
- Deadline
- Wat er verwacht wordt

### 5. Agent voert uit
De agent werkt de taak af en rapporteert via Telegram.

## Agenten Overzicht

| Agent | Skills | Gebruik voor |
|-------|--------|--------------|
| seo-specialist | SEO, keywords, analytics | Zoekmachine optimalisatie |
| frontend-dev | React, JavaScript, UI | Web en app interfaces |
| backend-dev | API, database, Supabase | Server-side logica |
| scraper-agent | Data collection, crawling | Vendor data ophalen |
| content-writer | Copy, blogs, marketing | Content creatie |
| ux-designer | Design, wireframes, research | User experience |
| lead-generator | Outreach, partnerships | Vendor acquisitie |
| devops-engineer | CI/CD, deployment | Infrastructure |
| business-developer | Strategy, growth | Business ontwikkeling |
| marketing-lead | Campaigns, social media | Marketing |
| ceo-weddingfinder | Planning, coordination | Strategie en overzicht |

## Commands

```bash
# Alle taken delegeren
python delegate.py

# Status check
python delegate.py --status

# Specifieke agent forceren
python delegate.py --agent seo-specialist
```

## Logs
- `task_execution_log.md` - Alle taak resultaten
- `delegate.py` output - Real-time delegatie info
