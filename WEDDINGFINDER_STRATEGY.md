# WEDDINGFINDER_STRATEGY.md - Core Principles & Agent Workflow

## 🎯 The Vision
We don't copy; we innovate. Weddingfinder 2026 is a premium, visual-first discovery platform that solves the biggest frustrations of modern couples.

## 👥 The Agent Ecosystem (Rimi as CEO)
Rimi orchestrates these specialized roles to maintain a constant loop of Research -> Emotion -> Design -> Execution.

1. **Bruidspaar Agent (The Persona)**
   - **Role:** Emotional voice of the user.
   - **Input:** Real-time data from forums (Viva, Trouwplannen), blogs, and sentiment analysis.
   - **Focus:** User pains (faillissement-angst, opacity in pricing, lack of real "non-staged" photos).
   - **Goal:** Drive features like "Match-making" and "Vibe-filtering".

2. **Marketing-Lead (Competitor Analysis)**
   - **Role:** Strategic benchmarker.
   - **Focus:** How do platforms like Zola or The Wed handle mobile search? Where do they fail?
   - **Constraint:** We must be faster and more visual than they are.

3. **UX-Designer (The Validation)**
   - **Role:** Translates empathy and strategy into code.
   - **Task:** Review UI against the "3-click rule" and mobile stress reduction.

4. **Specialists (Dev/Scraper/SEO)**
   - **Frontend:** High-end UI (V7.x+).
   - **Scraper:** Harvesting real image URLs and deeper vendor data (Batch processing).
   - **SEO:** Scaling content for the 500+ vendors.

## 🛠️ The "Strict" Workflow (MANDATORY)
1. **Research (Marketing-Lead):** What are others doing?
2. **Empathy (Bruidspaar Agent):** What does the user feel/need?
3. **Design (UX-Designer):** How do we solve this innovatively in the UI?
4. **Execution (Rimi/Dev):** Direct implementation in `main.html` and Supabase.

## 🚫 Forbidden
- Using placeholders when real image URLs are available.
- Hiding search on mobile.
- "Leads-first" approach; always show value and visuals first.
