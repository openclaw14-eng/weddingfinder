"""
Humanize venue descriptions and upload to Supabase.
Uses AI to humanize text, then uploads to Supabase avoiding duplicates.
"""

import json
import httpx
from datetime import datetime
from pathlib import Path

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def get_existing_vendors():
    """Fetch existing vendors from Supabase"""
    response = httpx.get(
        f"{SUPABASE_URL}/rest/v1/vendors?select=name,theperfectwedding_url,city&limit=1000",
        headers=headers,
        timeout=10
    )
    if response.status_code == 200:
        return response.json()
    return []

def upload_vendor(venue):
    """Upload a single venue to Supabase"""
    vendor_data = {
        "name": venue.get('name'),
        "slug": venue.get('slug') or venue.get('name', '').lower().replace(' ', '-').replace("'", ""),
        "city": venue.get('city'),
        "description": venue.get('description'),
        "capacity_min": venue.get('capacity', {}).get('min') if venue.get('capacity') else None,
        "capacity_max": venue.get('capacity', {}).get('max') if venue.get('capacity') else None,
        "rating": venue.get('rating'),
        "image_url": venue.get('image_urls', [None])[0] if venue.get('image_urls') else None,
        "theperfectwedding_url": venue.get('source_url'),  # Map to this column
        "source": venue.get('source', 'toptrouwlocaties.nl'),
        "is_premium": False,
        "keywords": venue.get('style_tags', []),
    }
    
    response = httpx.post(
        f"{SUPABASE_URL}/rest/v1/vendors",
        headers={**headers, "Prefer": "return=minimal"},
        json=vendor_data
    )
    return response.status_code in [201, 200, 204]

def humanize_description(venue):
    """Create a humanized description from raw data"""
    name = venue.get('name', '')
    city = venue.get('city', '')
    style_tags = venue.get('style_tags', [])
    capacity = venue.get('capacity') or {}
    rating = venue.get('rating')
    original_desc = venue.get('description', '')
    
    # Extract style keywords
    styles = ', '.join(style_tags[:3]) if style_tags else 'uniek'
    
    # Get capacity values safely
    cap_min = capacity.get('min', '') if capacity else ''
    cap_max = capacity.get('max', '') if capacity else ''
    cap_text = f"{cap_min}-{cap_max} gasten" if cap_min and cap_max else "elke groepsgrootte"
    
    # Humanized templates based on venue type
    templates = [
        f"Trouwen bij {name} is een droom die uitkomt. Deze sfeervolle locatie in {city} ademt {styles.lower()} — perfect voor jullie bijzondere dag. Geniet van de ruimte voor {cap_text} en creëer herinneringen die een leven lang meegaan.",
        f"{name} in {city} biedt alles wat je zoekt voor een onvergetelijke bruiloft. De karakteristieke {styles.lower()} uitstraling zorgt voor een magische sfeer. Met plek voor {cap_max or cap_text} is dit dé plek om jullie liefde te vieren." + (f" Beoordeling: {rating}/10." if rating else ""),
        f"Jawoord geven in {city}? {name} verwelkomt jullie met open armen. Deze {styles.lower()} trouwlocatie combineert karakter met comfort. Ruimte voor {cap_text}." + (f" Bekroond met {rating}/10 door andere bruidsparen." if rating else ""),
        f"Imagine: jullie bruiloft bij {name}. De {styles.lower()} ambiance in {city} maakt het plaatje compleet. Van intieme ceremonie tot groots feest — hier kan het allemaal. Capaciteit: {cap_text}." + (f" Fantastische {rating}/10 beoordeling!" if rating else ""),
        f"{name} is meer dan een trouwlocatie — het is een ervaring. In het hart van {city} vinden jullie deze {styles.lower()} parel. Perfect voor {cap_text} die samen met jullie willen vieren.",
    ]
    
    # Select template based on venue name hash for consistency
    import hashlib
    idx = int(hashlib.md5(name.encode()).hexdigest(), 16) % len(templates)
    return templates[idx]

def main():
    # Load JSON data
    with open("WeddingfinderApp/data/scraped_batch1.json", "r", encoding="utf-8") as f:
        scraped = json.load(f)
    
    print(f"Loaded {len(scraped)} venues from JSON")
    
    # Get existing vendors
    existing = get_existing_vendors()
    print(f"Found {len(existing)} existing vendors in Supabase")
    
    # Create sets for duplicate checking
    existing_urls = {v.get('theperfectwedding_url') for v in existing if v.get('theperfectwedding_url')}
    existing_names = {v.get('name', '').lower() for v in existing}
    
    # Filter new venues
    new_venues = []
    for venue in scraped:
        name = venue.get('name', '').lower()
        source_url = venue.get('source_url')
        
        # Check for duplicates
        if source_url and source_url in existing_urls:
            continue
        if name in existing_names:
            continue
        if not venue.get('city'):
            continue
        
        # Humanize description
        venue['description'] = humanize_description(venue)
        venue['slug'] = venue.get('name', '').lower().replace(' ', '-').replace("'", "")
        
        new_venues.append(venue)
    
    print(f"\nNew venues to upload: {len(new_venues)}")
    
    if not new_venues:
        print("No new venues to upload.")
        return
    
    # Show examples
    print("\nExamples of descriptions to upload:")
    for v in new_venues[:3]:
        print(f"\n{v['name']} ({v['city']}):")
        print(f"  {v['description'][:120]}...")
    
    # Upload
    print(f"\nUploading {len(new_venues)} venues...")
    success = 0
    failed = 0
    
    for i, venue in enumerate(new_venues, 1):
        print(f"  [{i}/{len(new_venues)}] {venue['name'][:40]}...", end=" ")
        
        if upload_vendor(venue):
            print("OK")
            success += 1
        else:
            print("FAILED")
            failed += 1
    
    print(f"\n=== RESULT ===")
    print(f"Success: {success}")
    print(f"Failed: {failed}")
    print(f"Total in Supabase now: ~{len(existing) + success}")

if __name__ == "__main__":
    main()
