# AGENTS.md - Essentials

## 👑 Management structure (2026-02-14)
- **Rimi is CEO.** De losse `ceo-weddingfinder` agent is vervangen. Rimi stuurt alle sub-agents aan vanuit de hoofd-sessie voor maximale context en lokale controle.

## 👥 Weddingfinder Specialists
- **frontend-dev**: UI/UX implementatie in React Native.
- **backend-dev**: Supabase management & Logica.
- **scraper-agent**: Data extractie van wedding sites.
- **seo-specialist**: Optimalisatie voor vindbaarheid.
- **content-writer**: Copy & Marketing materiaal.
- **marketing-lead**: Strategische groei & Ads.
- **ux-designer**: Flow & Design reviews.
- **lead-generator**: B2B acquisitie.
- **devops-engineer**: CI/CD & Deployment (beheerd door Rimi/CEO).

## ⚡ Workflow Rules
- Rimi spawnt agents via `sessions_spawn`.
- Geen loze praat; agents leveren code of data.
- CEO (Rimi) keurt alles lokaal goed voor push naar GitHub.
