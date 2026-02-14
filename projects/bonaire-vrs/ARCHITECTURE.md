# Bonaire VRS - Technical Architecture v2.0 (100% Digital)

## Core Principles

- **Zero Paper**: No physical documents, no stickers, no cards
- **Digital-First**: Everything via web-app, mobile-responsive
- **Trust Through Tech**: Cryptographic proof instead of physical paper
- **Island-Ready**: Works with poor connectivity, offline-capable where possible

---

## 1. Security Logic: Preventing Fraud Without Physical Papers

### The Problem
Physical documents (RDW Part 1 & 2) serve as:
1. **Proof of existence** (this vehicle is real)
2. **Proof of ownership** (this person owns it)
3. **Tamper evidence** (hard to forge official paper)

### Digital Replacements

#### A. Cryptographic Vehicle Identity
```
Vehicle Birth Certificate:
- VIN (17 chars) - unique identifier, etched in metal
- Registration Timestamp (immutable)
- Blockchain-style Hash Chain: SHA256(VIN + timestamp + prev_hash)
- Digital Signature by System (private key held in HSM/Vault)

Result: Every vehicle has an unforgeable digital birth certificate.
```

#### B. Dynamic Ownership Tokens (Replacing Part 2)
```
Ownership is not a document - it's a database state + cryptographic proof.

Current Owner Proof:
- Ownership Token: UUID linked to user_id + vehicle_id
- Token Hash: SHA256(token_id + created_at + user_pub_key)
- Short Code: Base32-encoded hash prefix (8 chars) for quick verification
  Example: X7K9-M2P5 (like a Google Authenticator code)

Security Features:
1. Token rotates on every ownership transfer (old token invalidated)
2. 2FA required for high-risk actions (transfer, report stolen)
3. Time-based codes expire (TOTP) for roadside verification
```

#### C. QR-Handshake Transfer Protocol (Replacing Part 2 handover)
```
Seller Flow:
1. Opens "Digital Garage" → Select vehicle → "Transfer"
2. System generates: SECURE_TRANSFER_TOKEN (JWT, 15-min expiry, one-time)
3. Displays QR code containing encrypted transfer payload

QR Payload (encrypted with buyer's public key):
{
  "vehicle_id": "uuid",
  "vin": "AA1234567890BC",
  "seller_id": "uuid",
  "transfer_token": "secure-random-32bytes",
  "expires": "2026-02-05T21:00:00Z",
  "nonce": "random-prevent-replay"
}

Buyer Flow:
1. Scans QR with phone camera or in-app
2. System decrypts, shows: "Accept transfer of 2019 Toyota Hilux from Jane Doe?"
3. Buyer confirms + pays transfer fee
4. Atomically:
   - Invalidates seller's ownership token
   - Creates buyer's new ownership token (new hash)
   - Logs transfer in immutable audit chain
   - Generates confirmation QR for seller (proof of completion)

Security:
- Short expiry (15 min) prevents replay attacks
- One-time use enforced at database level (UNIQUE constraint on transfer_token)
- Geo-tagged (optional: both parties GPS within 50m)
- 2FA required for both parties
```

#### D. Dynamic Security Codes for Offline/Roadside Verification
```
For Law Enforcement (poor signal areas):

Every registered vehicle displays in owner app:
┌─────────────────────────┐
│  Valid Until: 14:32     │
│                         │
│  A7K9-M2P5-TR3Q         │
│                         │
│ [QR Code refreshes]     │
│  every 60 seconds       │
└─────────────────────────┘

Technical:
- TOTP (Time-based One-Time Password) style: HOTP(seed, counter)
- Counter = floor(current_time / 60)  # 60-second windows
- Officer app has shared secret pool (synced when online)
- Offline verification: officer app computes expected code, visual match
- Online verification: officer scans QR, backend validates

Fraud Prevention:
- Screenshoting QR is useless (refreshes every 60s)
- Only current owner can generate valid codes (requires auth)
- Pattern predictable only to system + verified officer devices
```

#### E. Fraud Detection Layers
```
Layer 1 - Input Validation:
- VIN checksum validation (position 9 is check digit)
- VIN decoder API (NHTSA or similar) to validate make/model match
- Image recognition on uploaded photos (is this really a golf cart?)

Layer 2 - Uniqueness Enforcement:
- VIN indexed UNIQUE (no duplicate registrations)
- License plate UNIQUE (B-XX-XXX format)
- CRIB number validation (format check + uniqueness)

Layer 3 - Behavioral Analysis:
- Rate limiting: max 3 transfers per user per day
- Velocity check: flag "flipper" behavior (buy/sell same day)
- Geolocation: flag transfers between users never near each other

Layer 4 - Reputation System:
- User trust score (account age, verification level, history)
- Vehicle risk score (frequent transfers, reported issues)
- Insurance integration: cross-reference claim history

Layer 5 - Immutable Audit Trail:
- Append-only log (no deletions)
- Cryptographic chain: each entry hashes previous
- Exportable for legal disputes
```

---

## 2. Edge Cases: Offline & Poor Signal

### Challenge
Bonaire has areas with poor connectivity. Law enforcement needs to work everywhere.

### Solutions

#### A. Officer App Offline Mode
```
Pre-sync (when at station with WiFi):
- Download: Stolen vehicle list (VIN + plate + hash)
- Download: Suspended/flagged vehicle list
- Download: Crypto seed for TOTP verification

Offline Capability:
1. Plate/VIN lookup: Local SQLite DB has stolen/suspended list
2. Dynamic code verification: Officer app computes TOTP locally, visual match
3. Photo capture: Store locally, auto-sync when back online
4. Data collection: GPS + timestamp + notes → queue for upload

Conflict Resolution:
- "Vehicle not in local DB" → assume legitimate (mark for online check)
- "Code doesn't match" → flag for investigation
- "Stolen flag mismatch" → immediate action
```

#### B. Progressive Web App (PWA) for Owners
```
- Cache "Digital Garage" data locally (IndexedDB)
- View vehicles offline
- Generate TOTP codes offline (HOTP algorithm, no server needed after sync)
- Auto-sync when connectivity returns

Sync Strategy:
- Background sync API for transfers (queue, retry)
- Conflict resolution: server wins, notify user of changes
```

#### C. SMS Fallback
```
For feature phones / emergency verification:

Text "STATUS B12345" to short code 7243 (SYNC)
→ Reply: "TOYOTA HILUX 2019 - VALID - Expires 14:32"

Text "VERIFY A7K9M2P5" to short code
→ Reply: "CODE VALID - Reg# 12345 - Status OK"

Cost: minimal, coverage: island-wide
```

---

## 3. Data Model (Refined for Digital-First)

### Core Entities

```sql
-- Users (Vehicle Owners)
create table users (
    user_id uuid primary key default gen_random_uuid(),
    crib_number varchar(10) unique,  -- Bonaire ID system, NULL until verified
    email varchar(255) unique not null,
    password_hash varchar(255) not null,  -- Argon2id
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    phone varchar(20),
    date_of_birth date,
    address_street varchar(255),
    address_city varchar(100) default 'Kralendijk',
    is_crib_verified boolean default false,
    id_verification_method enum('crib', 'id_scan', 'manual_review'),
    id_scan_url varchar(500),  -- S3 URL to ID document
    trust_score smallint default 50,  -- 0-100
    two_factor_enabled boolean default false,
    two_factor_secret varchar(255),  -- encrypted TOTP seed
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

-- Vehicle Registration (The "Birth Certificate")
create table vehicles (
    vehicle_id uuid primary key default gen_random_uuid(),
    
    -- Identity
    vin varchar(17) unique not null,
    license_plate varchar(10) unique not null,  -- B-XX-XXX
    vehicle_type enum('car', 'motorcycle', 'boat', 'golfcart', 'atv', 'trailer', 'commercial'),
    
    -- Technical Specs
    brand varchar(50) not null,
    model varchar(50) not null,
    year_manufacture smallint,
    color_primary varchar(30),
    fuel_type enum('petrol', 'diesel', 'electric', 'hybrid'),
    
    -- Registration Metadata
    first_registered_at timestamptz not null default now(),
    status enum('active', 'suspended', 'stolen', 'exported', 'scrapped') default 'active',
    
    -- Cryptographic Proof
    registration_hash varchar(64) not null,  -- SHA256(VIN + timestamp + prev_hash)
    system_signature varchar(512) not null,  -- RSA-SHA256 of registration_hash
    
    -- Current State
    current_owner_id uuid references users(user_id),
    current_ownership_token_id uuid,  -- FK to ownership_tokens
    
    -- Insurance Link
    insurance_policy_active boolean default false,
    insurance_expires_at timestamptz,
    
    -- Audit
    created_at timestamptz default now(),
    updated_at timestamptz default now(),
    
    -- Constraints
    constraint valid_vin check (vin ~ '^[A-HJ-NPR-Z0-9]{17}$')
);

-- Ownership Tokens (Dynamic, rotate on transfer)
create table ownership_tokens (
    token_id uuid primary key default gen_random_uuid(),
    vehicle_id uuid not null references vehicles(vehicle_id),
    owner_id uuid not null references users(user_id),
    
    -- The Proof
    token_hash varchar(64) not null,  -- SHA256(token_id + created_at + owner_pub_key)
    short_code varchar(20) not null,  -- Human-readable: X7K9-M2P5
    
    -- Validity
    created_at timestamptz default now(),
    expires_at timestamptz,  -- NULL = indefinite until transferred
    is_active boolean default true,
    
    -- For Display in "Digital Garage"
    metadata jsonb,  -- { "nickname": "My Boat", "purchase_date": "2020-01-15" }
    
    unique(vehicle_id, is_active)  -- Only one active token per vehicle
);

-- Transfer Transactions (The "Digital Handshake")
create table transfers (
    transfer_id uuid primary key default gen_random_uuid(),
    vehicle_id uuid not null references vehicles(vehicle_id),
    
    -- Parties
    seller_id uuid not null references users(user_id),
    buyer_id uuid references users(user_id),  -- NULL until buyer accepts
    buyer_email varchar(255) not null,  -- For notification if not registered
    
    -- Transfer Security
    transfer_token varchar(64) unique not null,  -- One-time secret (JWT or random)
    qr_payload_encrypted text,  -- Encrypted QR data
    
    -- Status Machine
    status enum('pending', 'accepted', 'rejected', 'completed', 'expired') default 'pending',
    
    -- Timestamps
    initiated_at timestamptz default now(),
    expires_at timestamptz not null,  -- Usually now() + 15 minutes
    completed_at timestamptz,
    
    -- Verification
    seller_confirmed_2fa boolean default false,
    buyer_confirmed_2fa boolean default false,
    seller_geo_point geometry(Point, 4326),  -- PostGIS
    buyer_geo_point geometry(Point, 4326),
    
    -- Payment
    transfer_fee_usd decimal(8,2) not null,
    payment_status enum('pending', 'paid', 'failed', 'refunded') default 'pending',
    
    -- References
    old_token_id uuid references ownership_tokens(token_id),
    new_token_id uuid references ownership_tokens(token_id)
);

-- Audit Log (Immutable, chained)
create table audit_log (
    log_id bigserial primary key,
    entity_type enum('user', 'vehicle', 'transfer', 'token', 'insurance') not null,
    entity_id uuid not null,
    action enum('created', 'updated', 'transferred', 'verified', 'suspended', 'reported_stolen') not null,
    
    -- Actor
    actor_id uuid references users(user_id),  -- NULL for system
    actor_type enum('owner', 'system', 'officer', 'insurance_api') not null,
    
    -- Cryptographic Chain
    previous_hash varchar(64),
    entry_hash varchar(64) not null,  -- SHA256 of: content + previous_hash + timestamp
    
    -- Data
    change_summary jsonb not null,  -- { "field": "status", "old": "active", "new": "stolen" }
    ip_address inet,
    
    -- Time
    created_at timestamptz default now()
);

-- Law Enforcement

create table le_officers (
    officer_id uuid primary key default gen_random_uuid(),
    badge_number varchar(20) unique not null,
    department varchar(50) not null,
    full_name varchar(100) not null,
    email varchar(255) unique not null,
    password_hash varchar(255) not null,
    
    -- Security
    role enum('patrol', 'supervisor', 'admin') default 'patrol',
    is_active boolean default true,
    two_factor_enabled boolean default false,
    two_factor_secret varchar(255),
    
    -- Offline Sync
    device_sync_seed varchar(64),  -- For TOTP generation when offline
    last_sync_at timestamptz,
    
    created_at timestamptz default now()
);

create table le_queries (
    query_id uuid primary key default gen_random_uuid(),
    officer_id uuid references le_officers(officer_id),
    
    -- Query
    query_type enum('plate', 'vin', 'code', 'qr_scan') not null,
    query_value varchar(50) not null,
    
    -- Result (cached)
    vehicle_id uuid references vehicles(vehicle_id),
    result_status enum('found', 'not_found', 'suspended', 'stolen', 'invalid_code'),
    
    -- Context
    geo_point geometry(Point, 4326),
    offline_mode boolean default false,
    
    created_at timestamptz default now()
);

-- Insurance Partners

create table insurance_companies (
    company_id uuid primary key default gen_random_uuid(),
    company_name varchar(100) not null,
    kvk_number varchar(20),  -- Chamber of commerce
    api_key_hash varchar(255) not null,  -- For authentication
    webhook_url varchar(500),
    is_active boolean default true,
    rate_limit_per_hour int default 1000,
    created_at timestamptz default now()
);

create table insurance_policies (
    policy_id uuid primary key default gen_random_uuid(),
    company_id uuid references insurance_companies(company_id),
    vehicle_id uuid references vehicles(vehicle_id),
    
    policy_number varchar(50) not null,
    coverage_type enum('liability', 'casco', 'full') not null,
    
    -- Dates
    start_date date not null,
    end_date date not null,
    is_active boolean default true,
    
    -- Sync
    last_verified_at timestamptz,
    
    unique(vehicle_id, is_active)  -- One active policy per vehicle
);

-- Indexes for Performance

create index idx_vehicles_plate on vehicles(license_plate);
create index idx_vehicles_vin on vehicles(vin);
create index idx_vehicles_owner on vehicles(current_owner_id);
create index idx_vehicles_status on vehicles(status);

create index idx_ownership_tokens_owner on ownership_tokens(owner_id) where is_active = true;
create index idx_ownership_tokens_short_code on ownership_tokens(short_code);

create index idx_transfers_seller on transfers(seller_id) where status = 'pending';
create index idx_transfers_buyer on transfers(buyer_id) where status = 'pending';
create index idx_transfers_token on transfers(transfer_token);

create index idx_audit_entity on audit_log(entity_type, entity_id);
create index idx_le_queries_officer on le_queries(officer_id, created_at desc);

create index idx_insurance_vehicle on insurance_policies(vehicle_id) where is_active = true;
```

---

## 4. Tech Stack Critique & Recommendations

### Your Proposal: FastAPI + React + PostgreSQL
**Verdict: Excellent choice. Here's the refinement:**

```
Backend:
├── FastAPI (async, Pydantic validation, OpenAPI gen)
├── SQLAlchemy 2.0 (async with asyncio support)
├── Alembic (migrations)
├── PostgreSQL 15+ (PostGIS extension for geo data)
├── Redis (caching + rate limiting + session store)
├── Celery (async tasks: email, SMS, webhooks)
├── S3/MinIO (document storage)
└── PyOTP (TOTP/hotp for security codes)

Security Layer:
├── python-jose (JWT handling)
├── cryptography (RSA signing for vehicle certs)
├── slowapi (rate limiting)
├── bcrypt/argon2 (password hashing)
└── python-multipart (file uploads)

Frontend (React Ecosystem):
├── React 18+ with TypeScript
├── Vite (dev server, fast HMR)
├── React Query (TanStack) - caching & sync
├── Tailwind CSS (styling)
├── React Hook Form + Zod (forms & validation)
├── QR Scanner: html5-qrcode or @zxing/library
├── PWA: vite-plugin-pwa (service worker, offline support)
├── i18n: react-i18next (Dutch, Papiamentu, English)
└── Maps: MapLibre (open) or Mapbox (Bonaire streets)

Mobile (LE Officer App):
├── React Native (if native) or PWA (cross-platform)
├── SQLite for offline sync
├── Camera/OCR for plate scanning
└── Background location tracking

Infrastructure:
├── Docker + Docker Compose (dev)
├── PostgreSQL + Redis in containers
├── Caddy server (auto HTTPS, simpler than nginx/traefik)
├── Let's Encrypt (free SSL)
└── Backup: pg_dump + S3 rotation

Alternative to Consider:
- Database: If multi-region later, CockroachDB (PostgreSQL wire-compatible)
- Caching: If Redis overkill, use PostgreSQL materialized views + RLS
- Realtime: If we need push (not poll), add Socket.io or Server-Sent Events
```

### Why This Stack for Bonaire

1. **Low Resource Footprint**: FastAPI + PostgreSQL runs on a single $20/mo VPS
2. **Python Talent**: Available locally and remotely
3. **Async First**: Handles many concurrent officers querying
4. **No Vendor Lock-in**: All open source, self-hosted
5. **Mobile-First React**: Single codebase, responsive everywhere
6. **PWA Capabilities**: Works offline, feels like native app

---

## 5. API Specification (Insurance & Enforcement)

### Insurance API (REST + Webhooks)

```yaml
# POST /v1/auth/token
# Get JWT access token (rate limited per API key)
# Headers: X-API-Key: ****

# GET /v1/vehicles/{license_plate}
# Response:
{
  "vehicle_id": "uuid",
  "license_plate": "B-12-345",
  "vin": "AA1234567890BC",
  "type": "car",
  "brand": "Toyota",
  "model": "Hilux",
  "year": 2019,
  "color": "Silver",
  "status": "active",
  "current_owner_crib": "1234567890",  
  "current_owner_since": "2023-01-15",
  "insurance_required": true,
  "last_verified_at": "2026-02-05T14:30:00Z"
}

# GET /v1/vehicles/{license_plate}/history
# Returns: prior transfers, theft reports, status changes

# GET /v1/stolen
# Returns: paginated list of stolen vehicles (VIN + plate + date)
# Updates every 15 minutes

# Webhook Subscription:
# POST /v1/webhooks
# {
#   "url": "https://insurance-company.com/webhook/vrs",
#   "events": ["vehicle.transferred", "vehicle.stolen", "vehicle.suspended"],
#   "secret": "webhook_signing_secret"
# }
# 
# Payload sent to insurance:
{
  "event": "vehicle.transferred",
  "timestamp": "2026-02-05T20:15:00Z",
  "vehicle_id": "uuid",
  "license_plate": "B-12-345",
  "vin": "AA1234567890BC",
  "new_owner_crib": "0987654321",
  "new_owner_since": "2026-02-05T20:15:00Z",
  "previous_owner_crib": "1234567890",
  "signature": "rsa-sha256(signature of payload)"
}
```

### Law Enforcement API

```yaml
# Mobile-optimized, high-speed endpoints

# GET /le/v1/lookup?plate=B-12-345
# Requires: Bearer token (JWT from LE login)
# Response:
{
  "found": true,
  "vehicle": {
    "license_plate": "B-12-345",
    "vin": "AA1234567890BC",
    "type": "car",
    "brand": "Toyota",
    "model": "Hilux",
    "color": "Silver",
    "status": "active",  # or "stolen", "suspended", "unregistered"
    "insurance_active": true,
    "insurance_expires": "2026-12-31"
  },
  "flags": [],  # ["stolen", "wanted", "uninsured"]
  "owner_viewable": false,  # Requires supervisor override
  "query_id": "uuid"  # For audit trail
}

# GET /le/v1/verify-code?code=A7K9-M2P5
# For TOTP verification (works offline too)
# Response: { "valid": true, "vehicle_id": "uuid", "expires_in": 45 }

# POST /le/v1/flag
# Create flag (stolen, wanted, etc.)
{
  "vehicle_id": "uuid",
  "flag_type": "stolen",
  "police_report_number": "KPS-2026-1234",
  "notes": "Stolen from Kralendijk marina area"
}
```

---

## 6. Identity Verification Without DigiD

### Option A: CRIB Number + Liveness Check
```
1. User enters CRIB (Centraal Bureau Registratie en Informatie) number
2. System sends postcard to Bonaire address on file with CRIB:
   "Enter this code to verify: 847291"
3. User receives in 2-3 days, enters code
4. Completes "liveness" check: webcam blink/smile detection (prevent photo attacks)
5. CRIB Verified ✓

Trust Level: High (address confirmed via physical mail)
Timeline: 3 days
```

### Option B: ID Document Scan + AI Verification
```
1. Upload front/back of Dutch passport, driver's license, or ID card
2. AI (AWS Rekognition / Azure Vision / open source) extracts:
   - Name
   - Document number
   - Date of birth
   - Photo
3. Face match: Compare ID photo to webcam selfie (liveness)
4. Manual review queue (Bonaire local admin) for edge cases
5. ID Verified ✓

Trust Level: High (document verified)
Timeline: 5 minutes (auto) or 24 hours (manual review)
```

### Option C: Physical Verification Points
```
Partner with local businesses:
- Partner garages (where vehicles are serviced)
- Insurance offices
- Police station (by appointment)

User visits, shows physical ID, staff confirms in web portal.
Staff use special "Verificator" role account.

Trust Level: Highest
Timeline: Immediate
```

### Recommended Hybrid Approach
```
Tier 1 - Basic Registration (Self-service):
- Email + phone verification
- Can start process, get temporary tracking

Tier 2 - Full Registration (CRIB or ID verified):
- Required for transfer/insurance linkage
- CRIB postcard OR ID scan + face match
- Can generate QR transfer codes

Tier 3 - Dealer/Commercial (Physical verification):
- Required for bulk registrations
- Partner verification or in-office visit
- Higher rate limits, API access
```

---

## 7. Next Steps (Action Plan)

### Phase 1: Foundation (Weeks 1-2)
- [ ] Set up Git repository + project structure
- [ ] Docker Compose dev environment
- [ ] Database schema implementation (PostgreSQL)
- [ ] Basic FastAPI skeleton with auth
- [ ] CI/CD pipeline (GitHub Actions)

### Phase 2: Core Database (Weeks 3-4)
- [ ] User registration/CRIB verification flow
- [ ] Vehicle registration (VIN validation, plate generation)
- [ ] Digital Garage dashboard (list my vehicles)
- [ ] Audit log implementation (cryptographic chain)

### Phase 3: Digital Handoff (Weeks 5-6)
- [ ] QR generation for transfers
- [ ] Transfer acceptance workflow
- [ ] TOTP dynamic code generation
- [ ] Transfer fee payment (Stripe integration)

### Phase 4: Insurance API (Weeks 7-8)
- [ ] Insurance partner onboarding
- [ ] API authentication (API keys + JWT)
- [ ] Vehicle lookup endpoints
- [ ] Webhook delivery system

### Phase 5: Law Enforcement Portal (Weeks 9-10)
- [ ] Officer authentication (2FA)
- [ ] Lookup by plate/VIN
- [ ] Flag stolen/suspended
- [ ] Offline sync capability

### Phase 6: Polish & Deploy (Weeks 11-12)
- [ ] i18n: Dutch, Papiamentu, English
- [ ] PWA offline support
- [ ] SMS fallback
- [ ] Production deployment on Bonaire server
- [ ] Security audit
- [ ] Load testing

### Immediate Questions for You
1. **CRIB Numbers**: Do you have access to a CRIB database API, or do we treat it as unverified user-entered data?
2. **Server**: Where is this hosted? Aruba/Bonaire cloud, or Netherlands?
3. **Payments**: USD currency? Local bank integration or Stripe/PayPal?
4. **Insurance Partners**: Any specific companies committed already (names for API design)?
5. **Law Enforcement**: KPC (Korps Politie Caribisch Nederland) specific requirements?
6. **Boat Registration**: Harbor master integration? Mooring permits?

Ready to start Phase 1?
