# Bonaire Vehicle Registration System (VRS) - Brainstorm Document

## Context & Problem Statement

**Location:** Bonaire, Caribbean Netherlands (Dutch municipality)  
**Gap:** No local vehicle registration authority like RDW (Netherlands)  
**Opportunity:** Create a comprehensive registration system for all vehicle types

## Dutch RDW System Reference (What We're Mirroring)

### Core Documents (Kentekenbewijs)

**Part 1 (Kentekencard / Registration Card):**
- Vehicle identification: License plate (kenteken), chassis number (VIN)
- Technical specs: Make, model, type, fuel, color, mass, seats
- Registration: First admission date, current registration date
- Document number, barcode/QR code

**Part 2 (Ownership Document / Ten aanvang van de eigendom):**
- Owner details: Name, address, birth date (partial for privacy)
- Vehicle reference: Links to Part 1 via kenteken + document number
- Acquisition data: How obtained (purchase, inheritance, gift)
- **CRITICAL:** Required for selling/transferring vehicle

### RDW Data Fields

```
Vehicle Identity:
- Kenteken (license plate format: XX-XXX-X for cars, XX-XX-XX older)
- VIN/Chassis number (17 chars)
- Brand (merk)
- Type/model
- Variant
- Color (primary, secondary)

Technical:
- Vehicle category (personenauto, motor, aanhanger, etc.)
- Mass empty (ledig gewicht)
- Mass max (toegestane massa)
- Cylinder capacity
- Power (kW/HP)
- Fuel type
- CO2 emissions
- Seats
- Doors

Legal:
- First admission date ( datum eerste toelating)
- APK/MOT expiry (periodic inspection)
- Stolen status (gestolen/gezocht)
- Suspended (gestort/geschorst)
- Export status
- Insurance status (WAM-linked)
```

## Bonaire-Specific Requirements

### Vehicle Types (Bonaire Context)

**Standard Vehicles:**
- Cars (personenauto's) - personal & commercial
- Motorcycles/scooters (motoren, brommers)
- Trucks (vrachtwagens) - light & heavy
- Trailers (aanhangwagens)

**Bonaire-Specific:**
- Golf carts (very common for local transport)
- Boats/yachts (marina registration)
- ATVs/UTVs (off-road vehicles, popular on island)
- Construction equipment (rental fleet vehicles)
- Rental fleet vehicles (tourism-focused)
- Electric bikes/golf carts (growing segment)
- Classic/vintage cars (collector scene)

### Stakeholders

#### 1. Vehicle Owners (Primary Users)
**Needs:**
- Register new vehicles (import, local purchase)
- View vehicle status
- Transfer/sell vehicles
- Report theft/loss
- Update owner data (address, contact)
- Access historical records
- Print duplicate documents (lost Part 1/2)

**Registration Flow:**
1. Owner creates account (verified identity)
2. Submits vehicle data (manually or via import docs)
3. System validates uniqueness (VIN check)
4. Generates kenteken (license plate number)
5. Issues Part 1 (digital + optional physical card)
6. Issues Part 2 (ownership document)
7. Payment processing (registration fees)

#### 2. Insurance Companies (API Access)
**Needs:**
- Verify vehicle existence and specs
- Check ownership (validate Part 2 holder)
- Access accident/theft history
- Real-time status changes (theft alert, suspension)
- Bulk data for actuarial analysis
- Policy linkage (vehicle ↔ insurance contract)

**Integration Points:**
- REST API with authentication (mTLS + API keys)
- Webhook notifications on status changes
- Batch export capabilities
- Query by kenteken, VIN, or owner

#### 3. Law Enforcement (Secure Portal)
**Needs:**
- Lookup by license plate (mobile-friendly)
- Lookup by VIN
- Owner lookup (authorized only)
- Stolen vehicle alerts
- Wanted/suspended status flags
- Violation/ticket linkage (future)
- Cross-border data sharing (Dutch Antilles coordination)

**Security Requirements:**
- Role-based access control (RBAC)
- Audit logging (every query logged)
- Two-factor authentication
- IP whitelisting
- Session timeouts

#### 4. Dealers/Importers (Bulk Operations)
**Needs:**
- Bulk registration (imported vehicles)
- Pre-registration (before sale)
- Temporary plates (test drives, transport)
- Mass transfers (fleet sales)

#### 5. Maintenance/Inspection (Future)
**Needs:**
- APK/MOT-like periodic inspection tracking
- Inspection station access
- Expiry alerts to owners

## Comprehensive Feature List

### Core Features (MVP)

#### Registration Module
```
Owner Section:
- Digital identity verification (CBS nummer integration?)
- Account management
- Dashboard (my vehicles)

Vehicle Registration:
- Online form (step-by-step)
- Document upload (import papers, invoice, customs docs)
- VIN validation (checksum + uniqueness)
- License plate generation (format: B-XX-XXX for Bonaire)
- Fee calculation & payment (Stripe/Mollie/CC)
- Digital document delivery (PDF + email)

Vehicle Types Support:
- Car (personenauto) - standard plate format
- Boat (motor boot) - watercraft ID
- Golf cart (golfkar) - separate category with restricted road access
- Motorcycle/ATV - 2/3/4 wheel distinction
- Trailer - linked to towing vehicle
- Commercial vehicle
```

#### Transfer/Sale Module
```
Digital Transfer Process (like RDW):
1. Seller initiates transfer in portal
2. Enters buyer details (name, BSN/CBS, email)
3. System sends notification to buyer
4. Buyer accepts and pays transfer fee
5. Buyer receives new Part 2 (new document number)
6. Seller's Part 2 invalidated
7. New kentekenbewijs issued to buyer

Key Points:
- Part 2 document number changes (security feature)
- Previous owner history retained (audit trail)
- Temporary transfer proof issued
- Physical card (Part 1) stays with vehicle

Edge Cases:
- Seller has lien/loan (need bank approval)
- Export (to Netherlands or abroad)
- Inheritance (death certificate upload)
- Gift (tax implications)
- Theft (police report required)
- Total loss (insurance declaration)
```

#### Insurance Integration
```
API Capabilities:
- GET /vehicles/{kenteken} → full specs
- GET /vehicles/{kenteken}/owner → ownership details (with consent)
- GET /vehicles/{kenteken}/history → thefts, accidents, transfers
- POST /webhooks/subscribe → status notifications
- GET /reports/stolen → list of stolen vehicles

Security:
- Oauth2 / API key authentication
- Rate limiting
- Request signing
- Access logs (compliance)
```

#### Law Enforcement Portal
```
Features:
- Quick lookup (plate scanning via camera API)
- Full vehicle dossier view
- Owner contact info (restricted access)
- Flag stolen/recovered
- Flag wanted (investigation)
- Suspension/removal status
- Query audit trail

Mobile App:
- Officer login
- License plate photo → OCR → lookup
- GPS tagged queries
- Offline mode with sync
```

### Advanced Features (Post-MVP)

#### Notifications & Alerts
```
Owner Alerts:
- MOT/APK expiry (90, 30, 7 days)
- Insurance lapsing
- Stolen vehicle alert in area
- Registration fee due
- Transfer confirmation

Insurance Alerts:
- Vehicle status change (theft, suspension)
- Ownership change (policy review trigger)
- New damage/theft report

Law Enforcement Alerts:
- Stolen vehicle spotted (insurance-linked tracker)
- Suspended vehicle in operation
- Unregistered vehicle detected
```

#### Reporting & Analytics
```
Public Dashboard:
- Vehicles registered by type
- Electric vehicle adoption
- Import statistics

Insurance Portal:
- Risk statistics by vehicle type/age
- Theft heatmaps
- Claim correlation data

Admin/Government:
- Revenue reports
- Compliance statistics
- Fleet composition
- Environmental impact (EV adoption)
```

#### Compliance & Fraud Prevention
```
Security Measures:
- VIN check against stolen databases (Interpol)
- Duplicate registration detection
- Identity verification (CBS number cross-check)
- Document forgery detection (watermarks in PDF)
- Rate limiting on queries

Audit Trail:
- Every data change logged (who, when, what)
- Immutable log storage
- Compliance reporting
```

## Data Model (Preliminary)

### Entities

```
Owner:
- owner_id (UUID)
- cbs_number (Dutch Caribbean ID, unique)
- first_name, last_name
- birth_date
- address (street, city, postal, country)
- email, phone
- identity_verified (bool, timestamp)
- created_at, updated_at

Vehicle:
- vehicle_id (UUID)
- kenteken (B-XX-XXX format, unique)
- vin (VIN, unique, indexed)
- vehicle_type (enum: car, motorcycle, boat, golfcart, trailer, atv, etc.)
- category_detail (sub-type)
- brand, model, variant
- year_manufacture
- color_primary, color_secondary
- mass_empty_kg
- mass_max_kg
- cylinder_capacity_cc
- power_kw
- fuel_type (petrol, diesel, electric, hybrid)
- co2_g_km
- seats
- doors
- first_admission_date
- current_owner_id (FK)
- status (registered, suspended, stolen, exported, scrapped)
- part_1_doc_number (secure generated)
- part_1_issued_at
- part_1_pdf_url
- last_apk_date (optional MOT)
- created_at, updated_at

OwnershipRecord:
- record_id (UUID)
- vehicle_id (FK)
- owner_id (FK)
- part_2_doc_number (secure generated, unique)
- acquisition_type (purchase, inheritance, gift, company, import)
- acquisition_date
- purchase_price (optional, for tax)
- previous_owner_id (nullable)
- is_current (bool)
- terminated_at (nullable)
- created_at

Transfer:
- transfer_id (UUID)
- vehicle_id (FK)
- seller_owner_id (FK)
- buyer_cbs_number
- buyer_email
- status (pending, accepted, rejected, completed, expired)
- initiated_at
- expires_at (14 days default)
- completed_at
- fee_paid (bool)
- transfer_notes

InsurancePolicy:
- policy_id (UUID)
- vehicle_id (FK)
- insurance_company_id (FK)
- policy_number
- coverage_type (liability, casco, full)
- start_date, end_date
- is_active
- claim_count

EventLog:
- event_id (UUID)
- entity_type (vehicle, owner, transfer)
- entity_id
- event_type (created, updated, transferred, stolen_reported, etc.)
- actor_id (who did it)
- actor_type (owner, system, admin, le_officer)
- ip_address
- user_agent
- data_changes (JSON diff)
- created_at

LawEnforcementOfficer:
- officer_id (UUID)
- badge_number (unique)
- department
- email (verified)
- role (basic, supervisor, admin)
- is_active
- last_login
- two_factor_enabled

StolenReport:
- report_id (UUID)
- vehicle_id (FK)
- owner_id (FK)
- police_report_number
- stolen_date
- stolen_location
- recovered_date (nullable)
- status (stolen, recovered, closed)
- reported_at
```

## Technical Architecture

### Tech Stack

```
Backend:
- Python 3.11+ with FastAPI (async, OpenAPI)
- PostgreSQL 15+ (main data)
- Redis (caching, sessions, rate limiting)
- Celery (background jobs, notifications)
- Alembic (migrations)

Frontend:
- React/Vue/Svelte (TBD)
- Tailwind CSS
- Mobile-responsive (critical for officers)

File Storage:
- MinIO/S3-compatible (document storage)
- PDF generation (WeasyPrint or ReportLab)

Security:
- JWT access tokens + refresh tokens
- Argon2 for password hashing
- rate-limiting (Redis-based)
- Audit logging (append-only)

Infrastructure:
- Docker containers
- Traefik or nginx reverse proxy
- Let's Encrypt SSL
- Backup: daily encrypted to offsite

APIs:
- REST for main operations
- GraphQL (consider for complex queries)
- Webhooks for insurance integration
```

### License Plate Format

Bonaire-specific format:
```
Cars: B-XX-XXX (B-01-234, B-AA-123)
Boats: BN-XXX (BN-001, BN-999)
Golf carts: G-XX-XXX (G-01-234)
Trailers: T-XX-XXX (T-01-234)
Temporary: X-XX-XXX (test/transport plates)
```

Sequencing: Not strictly sequential (privacy/security)

## User Flows

### Owner Registration Flow
```
1. Visit website → "Register Vehicle"
2. Create account (email, password, CBS number)
3. Verify email
4. Complete profile (address, phone, ID upload if unverified CBS)
5. Start vehicle registration:
   - Select type (car/boat/golf cart/...)
   - Enter VIN (system validates uniqueness)
   - Enter specs (manually or import from VIN decoder)
   - Upload supporting docs (invoice, customs clearance)
   - Select/confirm license plate (auto-generated, can change once)
6. Pay registration fee (€XX varies by type)
7. Receive digital Part 1 + Part 2 via email
8. Order physical card (optional, shipping fee)
```

### Vehicle Sale/Transfer Flow
```
Seller:
1. Login → My Vehicles → Select vehicle
2. Click "Transfer/Sell"
3. Enter buyer's CBS number or email
4. Confirm own details (address for record)
5. Pay transfer fee (€XX)
6. System generates transfer request
7. Email sent to buyer

Buyer:
1. Receives email with secure link
2. Clicks link → creates account (if new) or logs in
3. Reviews vehicle details
4. Confirms transfer
5. New Part 2 generated (new doc number)
6. Old Part 2 invalidated
7. Both parties receive confirmation

System:
- Updates vehicle.current_owner_id
- Archives old ownership record
- Creates new ownership record
- Logs transfer event
- Notifies insurance company (if API connected)
```

### Law Enforcement Lookup Flow
```
Officer:
1. Mobile app → Login (2FA)
2. Scan license plate or type manually
3. System returns:
   - Vehicle specs (make/model/color)
   - Registration status
   - Insurance status (if linked)
   - Stolen/wanted flags
4. If needed: "View owner details" (requires supervisor approval/badging)
5. Can flag vehicle as "inspected" or "stopped"
6. GPS coordinates logged
```

## Business Model & Fees

```
Registration Fees:
- New car: €100
- Golf cart: €50
- Boat: €75 (size-based tiers)
- Motorcycle: €40
- Trailer: €25
- Transfer fee: €25 per transaction
- Duplicate Part 1: €15
- Duplicate Part 2: €25
- Physical card shipping: €10

Insurance API Access:
- Basic tier: €500/month (1000 queries)
- Professional tier: €2000/month (unlimited)
- Webhook add-on: €200/month

Law Enforcement:
- Government contract (free, subsidized by fees)
```

## Legal & Compliance Considerations

```
GDPR/Dutch Caribbean Privacy:
- Explicit consent for data storage
- Right to data export
- Right to deletion (with legal retain periods)
- Data retention policy (10 years for vehicle history)
- Secure data handling certifications

Vehicle Law:
- Inspection requirements (APK equivalent)
- Insurance mandate (WAM equivalent on Bonaire)
- Roadworthiness standards
- Import regulations (customs integration)

Cross-Border:
- Data sharing with RDW Netherlands (optional/future)
- Interpol stolen vehicle database integration
- Curaçao/Saba/Sint Eustatius coordination
```

## Questions for Ricky

1. **Government Mandate:** Is this a government-backed official register, or a private service filling a gap? (Affects legal weight of registrations)

2. **CBS Number Integration:** Should we integrate with CBS (Centraal Bureau Statistiek) for identity verification? Or standalone verification?

3. **Physical Cards:** Does Bonaire have printing capabilities for physical Part 1 cards, or is digital-only acceptable initially?

4. **Insurance Mandate:** Is insurance mandatory for all vehicles? Which types?

5. **Boat Registration:** Boats need IMO/registration numbers - is this for local anchorage/fishing permits too?

6. **Golf Cart Rules:** Where can golf carts legally drive? Who enforces?

7. **Import Process:** Most vehicles are imported - need customs docs integration?

8. **Language:** Dutch, Papiamentu, English, or multilingual?

9. **Currency:** USD (common in Bonaire) or Euro?

10. **Existing Data:** Any existing (even informal) vehicle database to migrate?

## Next Steps

1. Validate concept with local stakeholders
2. Define MVP feature set (prioritize owner self-registration)
3. Technical architecture review
4. Legal framework consultation
5. UI/UX wireframing
6. Database schema detailed design
7. API specification for insurance partners
8. Prototype development
