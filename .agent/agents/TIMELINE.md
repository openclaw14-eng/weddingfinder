# Weddingfinder MVP Timeline

## Phase 1: Foundation (Week 1-2)
**Focus:** Build the skeleton, collect data, design core flows

### Week 1: Setup & Skeleton

| Agent | Tasks | Deliverable | Status |
|-------|-------|-------------|--------|
| CEO | Define requirements, priorities | Requirements doc | ⏳ |
| UX Designer | User research, core flows | Figma wireframes | ⏳ |
| Scraper Agent | Setup scraper, first 100 vendors | JSON data | ⏳ |
| Backend Dev | Project setup, Supabase schema | Repo initialized | ⏳ |
| Frontend Dev | Expo setup, navigation | App skeleton | ⏳ |
| DevOps | CI/CD pipeline | GitHub Actions | ⏳ |

**Parallel Work:**
- UX Designer + Frontend Dev (coordinate on component structure)
- Scraper Agent runs independently (no dependencies)

**End of Week 1 Deliverables:**
- [ ] Figma wireframes for search, profile, favorites
- [ ] 100 vendor records in Supabase
- [ ] App builds and runs locally
- [ ] CI/CD pipeline configured

---

### Week 2: Core Infrastructure

| Agent | Tasks | Deliverable | Status |
|-------|-------|-------------|--------|
| Backend Dev | Auth APIs, CRUD endpoints | 10 APIs | ⏳ |
| Frontend Dev | Auth screens, API integration | Login/signup | ⏳ |
| UX Designer | Design system, components | Component library | ⏳ |
| Scraper Agent | Scrape 200 more vendors | 300 total | ⏳ |
| SEO Specialist | Technical SEO audit | Audit report | ⏳ |
| Content Writer | Blog post #1 | Published post | ⏳ |

**Parallel Work:**
- Backend Dev + Frontend Dev (API-first, parallel development)
- UX Designer provides components → Frontend implements
- Scraper Agent continues (independent)

**End of Week 2 Deliverables:**
- [ ] User authentication working
- [ ] Basic vendor CRUD (create, read)
- [ ] 300 vendor records
- [ ] Design system with 20+ components
- [ ] 1 blog post published
- [ ] Technical SEO audit complete

---

## Phase 2: Core Features (Week 3-4)
**Focus:** Search, profiles, user features

### Week 3: Search & Discovery

| Agent | Tasks | Deliverable | Status |
|-------|-------|-------------|--------|
| Backend Dev | Search API, filtering | Search endpoints | ⏳ |
| Frontend Dev | Search screen, filters | Search UI | ⏳ |
| UX Designer | Search usability test | Test results | ⏳ |
| Scraper Agent | Scrape 300 more vendors | 600 total | ⏳ |
| Content Writer | Blog posts #2-4 | 3 posts | ⏳ |
| SEO Specialist | Optimize for keywords | 10 rankings | ⏳ |

**Dependencies:**
- Backend Dev → Frontend Dev (API first)
- UX Designer → Frontend Dev (after components)

**End of Week 3 Deliverables:**
- [ ] Search functionality (keyword + filter)
- [ ] 600 vendor records
- [ ] 4 blog posts published
- [ ] 10 keywords in top 10

---

### Week 4: Profiles & User Features

| Agent | Tasks | Deliverable | Status |
|-------|-------|-------------|--------|
| Frontend Dev | Vendor profiles, favorites | Profile screens | ⏳ |
| Backend Dev | Profile APIs, favorites table | Profile endpoints | ⏳ |
| UX Designer | Profile mockups, iterate | Final designs | ⏳ |
| Scraper Agent | Scrape 400 more vendors | 1,000 total | ⏳ |
| Marketing Lead | Social media setup | Accounts active | ⏳ |
| Lead Generator | Start outreach | 50 contacted | ⏳ |

**Parallel Work:**
- Frontend Dev + Backend Dev (profile features)
- Marketing Lead + Content Writer (content calendar)

**End of Week 4 Deliverables:**
- [ ] Vendor profiles (name, photo, category, location)
- [ ] Favorites/save feature
- [ ] 1,000 vendor records
- [ ] Social media active
- [ ] 50 outreach messages sent

---

## Phase 3: Polish & Launch (Week 5-6)
**Focus:** Performance, marketing, launch prep

### Week 5: Hardening & Content

| Agent | Tasks | Deliverable | Status |
|-------|-------|-------------|--------|
| DevOps | Load testing, monitoring | Production ready | ⏳ |
| Backend Dev | Performance optimization | <200ms p95 | ⏳ |
| Frontend Dev | Crash fixes, polish | 99.5% stability | ⏳ |
| UX Designer | Accessibility audit | WCAG compliant | ⏳ |
| Content Writer | Blog posts #5-8 | 4 more posts | ⏳ |
| SEO Specialist | On-page optimization | Lighthouse >90 | ⏳ |
| Business Developer | Partner outreach | 5 contacted | ⏳ |

**End of Week 5 Deliverables:**
- [ ] Performance optimization complete
- [ ] 8 blog posts published
- [ ] Lighthouse score >90
- [ ] Accessibility WCAG AA
- [ ] Monitoring + alerts active

---

### Week 6: Launch & Growth

| Agent | Tasks | Deliverable | Status |
|-------|-------|-------------|--------|
| All | Launch prep checklist | Launch ready | ⏳ |
| Marketing Lead | Launch campaign | Campaign live | ⏳ |
| SEO Specialist | Index 50+ pages | Full index | ⏳ |
| Lead Generator | Follow-up outreach | 25 responses | ⏳ |
| Business Developer | Close first partners | 2 signed | ⏳ |
| DevOps | Deploy to production | Live on Netlify | ⏳ |
| CEO | Launch announcement | Public launch | ⏳ |

**Dependencies:**
- All agents must complete "Must Have" checklist before launch

---

## Milestone Summary

| Milestone | Target Date | Criteria |
|-----------|-------------|----------|
| Week 1 Complete | Feb 20 | Skeleton ready |
| Week 2 Complete | Feb 27 | Auth + 300 vendors |
| Week 3 Complete | Mar 6 | Search + 600 vendors |
| Week 4 Complete | Mar 13 | Profiles + 1,000 vendors |
| Week 5 Complete | Mar 20 | Polished + 8 posts |
| MVP Launch | Mar 27 | All "Must Have" done |

---

## Sprint Schedule

| Sprint | Dates | Focus |
|--------|-------|-------|
| Sprint 1 | Feb 13-20 | Foundation |
| Sprint 2 | Feb 20-27 | Infrastructure |
| Sprint 3 | Mar 6-13 | Core Features |
| Sprint 4 | Mar 13-20 | Polish |
| Sprint 5 | Mar 20-27 | Launch |

---

## Resource Allocation

| Agent | Hours/Week | Priority Tasks |
|-------|------------|---------------|
| CEO | 5 | Strategy, reviews, decisions |
| Scraper Agent | 20 | Data collection (full-time) |
| Backend Dev | 30 | APIs, database |
| Frontend Dev | 30 | App screens, integration |
| UX Designer | 15 | Design, research |
| SEO Specialist | 10 | Technical + content SEO |
| Content Writer | 15 | Blog posts |
| Marketing Lead | 10 | Social, email |
| Lead Generator | 15 | Outreach |
| Business Developer | 10 | Partnerships |
| DevOps | 10 | CI/CD, monitoring |

---

## Blocker Protocol

| Blocker Type | Escalate To | SLA |
|--------------|------------|-----|
| Technical (frontend) | Frontend Lead | 4 hours |
| Technical (backend) | Backend Lead | 4 hours |
| Design decision | UX Designer | 2 hours |
| Data quality | Scraper Agent | 2 hours |
| Priority conflict | CEO | 1 hour |
| Cross-team dependency | CEO | 4 hours |
