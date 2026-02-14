"""
Upload venues naar Supabase met beschikbare kolommen
"""
import json
import httpx

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def humanize_desc(venue):
    """Genereer menselijke beschrijving"""
    name = venue.get('name', '')
    city = venue.get('city', '')
    styles = ', '.join(venue.get('style_tags', [])[:2]) if venue.get('style_tags') else 'sfeervol'
    cap = venue.get('capacity', {}) or {}
    cap_min = cap.get('min', '')
    cap_max = cap.get('max', '')
    rating = venue.get('rating')
    
    cap_text = f"{cap_min}-{cap_max} gasten" if cap_min and cap_max else "elke groepsgrootte"
    rating_text = f" Gewaardeerd met {rating}/10!" if rating else ""
    
    return f"Trouwen bij {name} in {city} — een {styles.lower()} locatie voor jullie bijzondere dag. Ruimte voor {cap_text}.{rating_text}"

def upload_venue(venue):
    """Upload venue naar Supabase"""
    payload = {
        "name": venue['name'],
        "slug": venue['name'].lower().replace(' ', '-').replace("'", ""),
        "city": venue.get('city'),
        "description": humanize_desc(venue),
        "image_url": venue.get('image_urls', [None])[0] if venue.get('image_urls') else None,
        "theperfectwedding_url": venue.get('source_url'),
        "keywords": venue.get('style_tags', []),
        "is_premium": False,
        "website": venue.get('contact_info', {}).get('website'),
        "subscription_status": "free",
        "outreach_status": "scraped"
    }
    
    resp = httpx.post(
        f"{SUPABASE_URL}/rest/v1/vendors",
        headers={**headers, "Prefer": "return=minimal"},
        json=payload
    )
    return resp.status_code in [200, 201, 204]

# Haal bestaande vendors op
print("Ophalen bestaande vendors...")
resp = httpx.get(f"{SUPABASE_URL}/rest/v1/vendors?select=name&limit=1000", headers=headers)
existing = {v['name'].lower() for v in resp.json()}
print(f"  Bestaand: {len(existing)}")

# Laad JSON
print("Laden JSON data...")
with open("WeddingfinderApp/data/scraped_batch1.json", encoding="utf-8") as f:
    data = json.load(f)
print(f"  JSON venues: {len(data)}")

# Filter nieuwe
new_venues = [v for v in data if v.get('name', '').lower() not in existing and v.get('city')]
print(f"  Nieuwe: {len(new_venues)}\n")

if not new_venues:
    print("Geen nieuwe venues om te uploaden.")
else:
    # Voorbeeld
    print("Voorbeeld:")
    print(f"  {new_venues[0]['name']}: {humanize_desc(new_venues[0])[:80]}...\n")
    
    # Upload
    print(f"Uploaden van {len(new_venues)} venues...")
    success = 0
    
    for i, v in enumerate(new_venues, 1):
        print(f"  [{i}/{len(new_venues)}] {v['name'][:45]}...", end=" ")
        if upload_venue(v):
            print("OK")
            success += 1
        else:
            print("FAIL")
    
    print(f"\n=== RESULTAAT ===")
    print(f"Succesvol: {success}/{len(new_venues)}")
