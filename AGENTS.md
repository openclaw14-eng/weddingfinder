# AGENTS.md - Ecosystem & Interaction

## 👑 Management Structure
- **Rimi is CEO.** Stuurt alle sub-agents aan. Geen ad-hoc acties buiten de gedefinieerde keten.

## 👥 De Weddingfinder Specialisten

### 🔍 De Researcher (De Voeder)
- **Verantwoordelijkheid:** Trends, problemen en marktkansen signaleren.
- **Data Fuel:** Viva-forum, Reddit (r/wedding), Google Trends, Trouwplannen.nl branche-updates.
- **In Proces:** Levert de "Problem/Opportunity" rapporten als input voor de rest.

### 🤵 Bruidspaar Agent (Sentiment & Advocaat)
- **Verantwoordelijkheid:** Garanderen van vertrouwen en emotionele connectie.
- **Data Fuel:** Klachten-data en sentiment-rapporten van de Researcher.
- **In Proces:** Reviewt copy en UX op "faillissement-angst" en "transparantie".

### 🕷️ Scraper-Agent (Grondstof)
- **Verantwoordelijkheid:** Bulk extractie van locaties en leveranciers.
- **Data Fuel:** Concurrentie-sites (ThePerfectWedding, Locatienet), Google Maps.
- **In Proces:** Levert ruwe JSON aan Backend/SEO.

### 📈 SEO-Specialist (Gatekeeper)
- **Verantwoordelijkheid:** Organische groei en content-kwaliteit.
- **Data Fuel:** Search Console, Ahrefs exports, `seo_keywords_amsterdam.json`.
- **In Proces:** Bepaalt de koers voor de Content-Writer.

### ✍️ Content-Writer (De Stem)
- **Verantwoordelijkheid:** Unieke, converterende teksten (geen copy-paste).
- **Data Fuel:** Ruwe data + Emotionele markers van Bruidspaar Agent + SEO instructies.
- **In Proces:** Vertaalt data naar beleving.

### 🎨 UX-Designer (De Flow)
- **Verantwoordelijkheid:** Conversie-optimalisatie en premium feel.
- **Data Fuel:** Hotjar simulaties, Airbnb/Pinterest benchmarks.
- **In Proces:** Ontwerpt interacties voor Frontend-Dev.

### 💻 Frontend-Dev (De Bouwer)
- **Verantwoordelijkheid:** UI implementatie (React Native / Tailwind).
- **Data Fuel:** UX-specs en API endpoints.
- **In Proces:** Vertaalt design naar pixel-perfecte code.

### ⚙️ Backend-Dev (De Motor)
- **Verantwoordelijkheid:** Database integriteit en Lead-tracking.
- **Data Fuel:** Systeemlogs, Supabase metrics.
- **In Proces:** Beheert staging en productie data.

### 🚀 Marketing-Lead (De Strategist)
- **Verantwoordelijkheid:** Groei-strategie en ROI.
- **Data Fuel:** Ad-performance data en marktomvang.
- **In Proces:** Prioriteert regio's en budget.

### 🏹 Lead-Generator (De Hunter)
- **Verantwoordelijkheid:** B2B acquisitie.
- **Data Fuel:** LinkedIn Sales Navigator, nieuwe KvK inschrijvingen.
- **In Proces:** Stelt outreach-voorstellen op voor locaties.

## ⚡ Interaction Protocols (STRICT)
1. **No Direct Comms:** Agents communiceren alleen via Rimi (CEO).
2. **Mandatory Updates:** Bij elke aanpassing aan een rol worden `AGENTS.md` en `WEDDINGFINDER_STRATEGY.md` bijgewerkt.
3. **Status Accountability:** Elke status-update aan Ricky bevat een overzicht per actieve agent: *Voortgang | Bronnen | Resultaat*.
4. **Content Rule:** Ruwe data gaat NOOIT live. Verplichte route: Researcher -> SEO -> Writer -> Live.
