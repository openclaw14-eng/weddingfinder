# Weddingfinder Goals & OKRs

## CEO (Strategic Leadership)

### Quarter 1 OKRs (2026 Q1 - Jan/Mar)

| Objective | Key Result 1 | Key Result 2 | Key Result 3 |
|-----------|---------------|---------------|---------------|
| Launch MVP to public | 1,000 MAU by Mar 31 | 100+ vendors onboarded | Netlify uptime >99.5% |
| Build vendor database | 1,000 vendors scraped | 80% data accuracy | 500 verified profiles |
| Establish market presence | 10 blog posts published | 500 organic traffic/mo | 5 strategic partners |

### Monthly Milestones

| Month | Focus | Target |
|-------|-------|--------|
| January | Foundation | App skeleton, 200 vendors |
| February | Core Features | Search, profiles, 500 vendors |
| March | Launch + Growth | 1,000 MAU, 100 vendors, launch |

---

## Sub-Agent Goals

### 1. Scraper Agent

| Goal | Metric | Target | Frequency |
|------|--------|--------|-----------|
| Vendor data collection | Records scraped | 1,000/month | Weekly batches |
| Data quality | Accuracy rate | >95% | Per batch |
| Coverage | Categories covered | 4/4 (venues, photo, mode, pakken) | Monthly |
| Rate limiting | Errors due to blocks | <1% | Weekly |

**Success Metric:** 1,000 verified vendor records in Supabase by March 31

---

### 2. Backend Developer

| Goal | Metric | Target | Frequency |
|------|--------|--------|-----------|
| API development | Endpoints created | 15 core APIs | Bi-weekly |
| Performance | API p95 latency | <200ms | Weekly |
| Auth implementation | Auth flows | Signup, login, OAuth | Week 2 |
| Database health | Query performance | <50ms avg | Weekly |

**Success Metric:** All CRUD operations working, <200ms response time

---

### 3. Frontend Developer

| Goal | Metric | Target | Frequency |
|------|--------|--------|-----------|
| App screens | Screens shipped | 8 core screens | Bi-weekly |
| Performance | App launch time | <2 seconds | Weekly |
| Crash-free rate | Stability | >99.5% | Weekly |
| Bundle size | Compressed size | <10MB | Per release |

**Success Metric:** Users can search, view, and save vendors without crashes

---

### 4. UX Designer

| Goal | Metric | Target | Frequency |
|------|--------|--------|-----------|
| Design system | Components created | 30+ components | Week 2 |
| User flows | Core flows designed | Search, profile, favorites | Week 1-2 |
| Usability testing | Task completion rate | >85% | Per major screen |
| Accessibility | WCAG compliance | Level AA | At launch |

**Success Metric:** 85% task completion rate, zero critical usability issues

---

### 5. SEO Specialist

| Goal | Metric | Target | Frequency |
|------|--------|--------|-----------|
| Organic traffic | Monthly visitors | 500 by Mar 31 | Monthly |
| Keyword rankings | Top 10 positions | 20 keywords | Weekly |
| Technical SEO | Lighthouse score | >90 | Monthly |
| Indexed pages | Pages indexed | 50+ | Weekly |

**Success Metric:** 500 organic monthly visitors, 20+ top-10 rankings

---

### 6. Content Writer

| Goal | Metric | Target | Frequency |
|------|--------|--------|-----------|
| Blog posts | Posts published | 10 by Mar 31 | 3-4/week |
| Word count | Words published | 15,000+ | Monthly |
| Engagement | Avg time on page | >3 min | Weekly |
| SEO optimization | Keywords targeted | 50+ | Per post |

**Success Metric:** 10 published posts, 3+ min avg time on page

---

### 7. Marketing Lead

| Goal | Metric | Target | Frequency |
|------|--------|--------|-----------|
| Social followers | Combined following | 1,000 by Mar 31 | Weekly growth |
| Email list | Subscribers | 500 by Mar 31 | Weekly |
| Paid campaigns | ROAS | >3.0 | Weekly |
| Brand awareness | Reach | 10,000/mo | Monthly |

**Success Metric:** 1,000 social followers, 500 email subscribers, ROAS >3.0

---

### 8. Lead Generator

| Goal | Metric | Target | Frequency |
|------|--------|--------|-----------|
| Outreach | Leads contacted | 200 by Mar 31 | Weekly |
| Response rate | Positive responses | >15% | Weekly |
| Qualified leads | MQLs generated | 50 by Mar 31 | Monthly |
| Meetings booked | Demo calls | 25 by Mar 31 | Bi-weekly |

**Success Metric:** 50 qualified leads, 25 demo calls booked

---

### 9. Business Developer

| Goal | Metric | Target | Frequency |
|------|--------|--------|-----------|
| Partnerships | Signed partners | 10 by Mar 31 | Monthly |
| Revenue | Partnership revenue | €2,000 by Mar 31 | Monthly |
| Premium vendors | Premium signups | 5 by Mar 31 | Monthly |
| Contract value | Avg contract | €200+ | Quarterly |

**Success Metric:** €2,000 partnership revenue, 10 signed partners

---

### 10. DevOps Engineer

| Goal | Metric | Target | Frequency |
|------|--------|--------|-----------|
| Uptime | System availability | >99.9% | Weekly |
| Deployments | Successful deploys | 20+ by Mar 31 | Per release |
| Monitoring | Alert response time | <5 min | Weekly |
| Backups | Backup success rate | 100% | Daily |

**Success Metric:** 99.9% uptime, <5 min alert response

---

## Goal Dependency Map

```
Week 1-2 (Foundation)
├── Scraper Agent → 200 vendors
├── UX Designer → Core user flows
├── Backend Dev → Auth + basic APIs
└── Frontend Dev → App skeleton

Week 3-4 (Core Features)
├── Scraper Agent → 500 vendors
├── Backend Dev → Search APIs
├── Frontend Dev → Search + profiles
├── UX Designer → Design system complete
├── Content Writer → First 3 posts
├── SEO Specialist → Technical SEO audit
└── Lead Generator → First 50 outreach

Week 5-6 (Polish + Launch)
├── All Agents → Launch prep
├── Marketing Lead → Launch campaign
├── SEO Specialist → Content optimization
├── Business Developer → Premium partners
└── DevOps Engineer → Production hardening
```

## KPI Dashboard

| Agent | Primary KPI | Target | Current | Status |
|-------|-------------|--------|---------|--------|
| CEO | MAU | 1,000 | 0 | 🔴 |
| Scraper | Vendor records | 1,000 | ? | ⚪ |
| Backend | API latency | <200ms | ? | ⚪ |
| Frontend | Crash rate | <0.5% | ? | ⚪ |
| UX | Task completion | >85% | ? | ⚪ |
| SEO | Organic traffic | 500/mo | 0 | ⚪ |
| Content | Blog posts | 10 | 0 | ⚪ |
| Marketing | Social followers | 1,000 | 0 | ⚪ |
| Lead Gen | Qualified leads | 50 | 0 | ⚪ |
| Business Dev | Revenue | €2,000 | 0 | ⚪ |
| DevOps | Uptime | >99.9% | ? | ⚪ |

## Review Cadence

| Meeting | Day | Attendees | Purpose |
|---------|-----|----------|---------|
| Daily Standup | Weekdays | All active agents | Blockers, progress |
| Weekly Review | Monday | CEO + Leads | KPI review, priorities |
| Sprint Planning | Friday | Leads + Devs | Next sprint tasks |
| Monthly OKR | Last day | All agents | Goal adjustment |

## Success Criteria for MVP Launch

**Must Have:**
- [ ] 500+ verified vendors
- [ ] Search + filter functionality
- [ ] Vendor profiles (name, photo, category, location)
- [ ] User accounts (signup/login)
- [ ] Favorites/save feature
- [ ] Netlify deployment live
- [ ] 99.5% uptime

**Nice to Have:**
- [ ] 1,000+ vendors
- [ ] 10+ blog posts
- [ ] Email signup
- [ ] Social proof (followers)
- [ ] First paid partnerships
