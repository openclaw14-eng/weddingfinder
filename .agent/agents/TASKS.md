# Weddingfinder MVP - Task Roadmap

## Master TO DO List

```
PRIORITY 1: APP FOUNDATION
├── [ ] 1.1 Project setup (Expo + Supabase)
├── [ ] 1.2 User authentication (signup/login)
├── [ ] 1.3 Database schema for vendors
├── [ ] 1.4 Navigation structure
└── [ ] 1.5 Basic UI components

PRIORITY 2: VENDOR DATA (must be non-traceable)
├── [ ] 2.1 Scraper setup (theperfectwedding.nl)
├── [ ] 2.2 Data anonymization (no source links)
├── [ ] 2.3 Data storage in Supabase
├── [ ] 2.4 500 verified vendor records
└── [ ] 2.5 1,000 verified vendor records

PRIORITY 3: CORE FEATURES
├── [ ] 3.1 Search functionality (keywords + filters)
├── [ ] 3.2 Vendor profile pages
├── [ ] 3.3 Favorites/save feature
├── [ ] 3.4 User profile management
└── [ ] 3.5 Contact vendor functionality

PRIORITY 4: SEO OPTIMIZATION
├── [ ] 4.1 Technical SEO audit
├── [ ] 4.2 Meta tags for all pages
├── [ ] 4.3 Schema markup (LocalBusiness, FAQ)
├── [ ] 4.4 Sitemap.xml generation
├── [ ] 4.5 Robots.txt configuration
└── [ ] 4.6 Performance optimization (Lighthouse >90)

PRIORITY 5: POLISH & LAUNCH
├── [ ] 5.1 Accessibility audit (WCAG AA)
├── [ ] 5.2 Error handling & crash recovery
├── [ ] 5.3 Loading states & skeletons
├── [ ] 5.4 Dark mode support
├── [ ] 5.5 Production deployment
└── [ ] 5.6 Launch announcement
```

---

## Dependency Graph

```
1. PROJECT SETUP (1.1-1.5)
    ↓
2. VENDOR DATA (2.1-2.5)
    ↓
3. CORE FEATURES (3.1-3.5)
    ↓
4. SEO OPTIMIZATION (4.1-4.6)
    ↓
5. POLISH & LAUNCH (5.1-5.6)
```

**Parallel allowed:**
- 2.x (Scraper) runs independently while 1.x in progress
- 4.x (SEO) can start after 3.x partial completion
- 5.x (Polish) runs while 4.x in progress

---

## Completion Criteria

| Task | Definition of Done |
|------|-------------------|
| 1.1 | App builds locally, connects to Supabase |
| 1.2 | Signup, login, logout, password reset work |
| 1.3 | Tables: vendors, users, favorites, categories |
| 1.4 | Tab nav + stack nav working |
| 1.5 | 20+ reusable components |
| 2.1 | Scraper runs without errors |
| 2.2 | No URLs/links to source sites in DB |
| 2.3 | Data loads correctly in app |
| 2.4 | 500 records with: name, photo, category, location, description |
| 2.5 | 1,000 records (includes 2.4) |
| 3.1 | Search by name, filter by category/location |
| 3.2 | Profile shows vendor info |
| 3.3 | Save vendors to favorites |
| 3.4 | Edit user profile, avatar, preferences |
| 3.5 | Contact form or phone/email display |
| 4.1 | All issues fixed from audit |
| 4.2 | Dynamic meta tags for all routes |
| 4.3 | Valid JSON-LD markup |
| 4.4 | Sitemap includes all vendor pages |
| 4.5 | Robots.txt allows crawling |
| 4.6 | Lighthouse: Performance >90, SEO >95 |
| 5.1 | WCAG AA compliant |
| 5.2 | No unhandled errors |
| 5.3 | All loading states have skeletons |
| 5.4 | Light/dark theme toggle |
| 5.5 | Live on Netlify, custom domain |
| 5.6 | Social posts, email announcement |

---

## Agent Assignment

| Task | Primary Agent | Supporting Agents |
|------|--------------|-------------------|
| 1.1-1.5 | Frontend Dev | Backend Dev, UX Designer |
| 2.1-2.5 | Scraper Agent | Backend Dev |
| 3.1-3.5 | Frontend Dev | Backend Dev, UX Designer |
| 4.1-4.6 | SEO Specialist | Frontend Dev |
| 5.1-5.6 | DevOps | All dev agents |

---

## Progress Tracking

| Task | Status | Agent | Started | Completed |
|------|--------|-------|---------|-----------|
| 1.1 | ⏳ | - | - | - |
| 1.2 | ⏳ | - | - | - |
| 1.3 | ⏳ | - | - | - |
| 1.4 | ⏳ | - | - | - |
| 1.5 | ⏳ | - | - | - |
| 2.1 | ⏳ | - | - | - |
| 2.2 | ⏳ | - | - | - |
| 2.3 | ⏳ | - | - | - |
| 2.4 | ⏳ | - | - | - |
| 2.5 | ⏳ | - | - | - |
| 3.1 | ⏳ | - | - | - |
| ... | ⏳ | - | - | - |

---

## Parallel Work Policy

### Rule: NEVER STOP - Always Have Alternative

**IF A TASK IS BLOCKED → WORK ON SOMETHING ELSE**

```
TASK A BLOCKED
     │
     ├── Try alternative approach (3 attempts)
     ├── If still blocked → Mark L3 in ERROR_LOG.md
     └── Continue with any OTHER available task
```

### Explicit Parallel Workstreams

| Workstream | Tasks | Can Run When |
|------------|-------|--------------|
| **Workstream A** | 1.1, 1.2, 1.4, 1.5 | Foundation work (any order) |
| **Workstream B** | 2.1, 2.2, 2.3, 2.4, 2.5 | Scraping (INDEPENDENT of A!) |
| **Workstream C** | 3.1, 3.2, 3.3, 3.4, 3.5 | After 1.x OR 2.x partial |
| **Workstream D** | 4.1, 4.2, 4.3, 4.4, 4.5, 4.6 | After 3.1 or pages exist |
| **Workstream E** | 5.1, 5.2, 5.3, 5.4, 5.5, 5.6 | Can overlap with D |

### Dependency Exceptions (Only These Are Sequential)

| If This Is Blocked | Can Still Work On |
|--------------------|--------------------|
| 1.1 (Project setup) | 2.1-2.5 (Scraper - independent!) |
| 1.2 (Auth) | 1.3, 1.4, 1.5 (other foundation) |
| 1.3 (DB schema) | 1.1, 1.2, 1.4, 1.5 (other foundation) |
| 2.1 (Scraper setup) | 2.2-2.5 (other scraping tasks) |
| 3.1 (Search API) | 3.2, 3.3 (UI features) |
| 3.2 (Profile pages) | 3.1, 3.3, 3.4, 3.5 (other features) |
| 4.1 (SEO audit) | 4.2-4.6 (other SEO tasks) |

**KEY INSIGHT:** Workstream B (Scraper) is INDEPENDENT of Workstream A!  
If 1.1 is blocked → Scraping continues anyway!

---

## Velocity Tracking

| Agent | Tasks Completed | Avg Time/Task | Velocity Score |
|-------|----------------|---------------|----------------|
| Frontend Dev | 0 | - | - |
| Scraper Agent | 0 | - | - |
| Backend Dev | 0 | - | - |
| SEO Specialist | 0 | - | - |
| DevOps | 0 | - | - |

**Velocity = Tasks Completed / Agent Sprint**
