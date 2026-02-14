# Project Plan - Weddingfinder Persistent Agent System

## 📅 Generated
2026-02-11 08:15 GMT+1

---

## 🚀 Nu Bezig (In Progress)

### Task 1: Massa Scraper 3.0
- **Description**: Pagineren door honderden pagina's van ThePerfectWedding.
- **Status**: IN PROGRESS
- **Checkpoints**:
  - [ ] 100 pagina's verwerkt
  - [ ] 500 pagina's verwerkt
  - [ ] 1000+ pagina's verwerkt
  - [ ] Eindevaluatie
- **Resume Point**: `scraper_progress.json` (opslag van laatste offset)
- **Check**: `final_scraper.py` logs controleren op fouten.

### Task 2: Expo App Build
- **Description**: Web-server draaien en UI verfijnen.
- **Status**: IN PROGRESS
- **Checkpoints**:
  - [ ] Lokale build succesvol
  - [ ] API endpoints actief
  - [ ] UI responsiveness getest
- **Resume Point**: `live_dashboard_server.py` PID
- **Check**: Server ping test (`curl localhost`).

### Task 3: Lead Tracking
- **Description**: RPC functies in Supabase finetunen.
- **Status**: IN PROGRESS
- **Checkpoints**:
  - [ ] Functies geïmporteerd
  - [ ] Test data ingevoerd
  - [ ] Performance metrics
- **Resume Point**: Laatste succesvolle RPC call timestamp.
- **Check**: Supabase logs.

---

## 📥 Backlog (To Do)

- [ ] **Partner Dashboard**: Leveranciers self-service portal.
- [ ] **Stripe Integratie**: Automatische betalingen.
- [ ] **AI Image Optimization**: Optimalisatie voor mobiel.

---

## ✅ Voltooid (Done)

- [x] Database Setup
- [x] Portal Systeem
- [x] SEO Agent
- [x] App Prototype

---

## ⚙️ System Tasks (Persistent Agent)

Deze taken worden automatisch beheerd door het persistent agent systeem.

| Taak | Interval | Script | Volgende Run | Status |
|------|----------|--------|--------------|--------|
| Heartbeat | 1 uur | `heartbeat_monitor.py` | TODO | 🔴 Gestopt |
| Vendor Scraping | 6 uur | `scraper_supabase.py` | TODO | 🔴 Gestopt |
| SEO Optimalisatie | 24 uur | `seo_agent.py` | TODO | 🔴 Gestopt |
| Keep Awake | Altijd | `keep_awake.py` | TODO | 🔴 Gestopt |

---

## 📂 Checkpoint Systeem

Locatie: `persistent_agent/checkpoints.json`

**Gebruik:**
1. **Start**: Laad `checkpoints.json`.
2. **Resume**: Als `scraper_supabase` is onderbroken, hervat vanaf `last_offset`.
3. **Opslag**: Schrijf na elke grote taak de timestamp en status weg.

---

## 🔄 Acties voor Systeem Start

1. Start `keep_awake.py` als achtergrondservice.
2. activeer Windows Task Scheduler voor heartbeat (elke uur).
3. activeer Windows Task Scheduler voor scraper (elke 6 uur).
4. activeer Windows Task Scheduler voor SEO (dagelijks).
