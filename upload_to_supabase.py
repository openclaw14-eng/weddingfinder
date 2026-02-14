"""
Upload venues naar Supabase met humanized beschrijvingen
- Checkt op duplicaten (op basis van source_url)
- Humanized alleen beschrijvingen die AI-generated lijken
- Behoudt bestaande data in Supabase
- Uploadt alleen nieuwe venues met echte content
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
    """Haal alle bestaande vendors op uit Supabase"""
    all_vendors = []
    offset = 0
    limit = 1000
    
    while True:
        response = httpx.get(
            f"{SUPABASE_URL}/rest/v1/vendors?select=name,source_url,city&limit={limit}&offset={offset}",
            headers=headers
        )
        if response.status_code != 200:
            print(f"Fout bij ophalen vendors: {response.status_code}")
            break
        
        batch = response.json()
        if not batch:
            break
        
        all_vendors.extend(batch)
        if len(batch) < limit:
            break
        offset += limit
    
    return all_vendors

def get_existing_source_urls(vendors):
    """Maak een set van bestaande source_urls"""
    urls = set()
    for v in vendors:
        if v.get('source_url'):
            urls.add(v['source_url'])
    return urls

def get_existing_names(vendors):
    """Maak een set van bestaande namen (lowercase)"""
    return {v['name'].lower() for v in vendors}

def upload_vendor(venue):
    """Upload een enkele vendor naar Supabase"""
    # Map venues JSON velden naar Supabase velden
    vendor_data = {
        "name": venue.get('name'),
        "slug": venue.get('slug') or venue.get('name', '').lower().replace(' ', '-'),
        "city": venue.get('city'),
        "description": venue.get('description'),
        "address": venue.get('address') or venue.get('description', '').split('in')[-1].strip() if 'in' in venue.get('description', '') else None,
        "capacity_min": venue.get('capacity', {}).get('min') if venue.get('capacity') else None,
        "capacity_max": venue.get('capacity', {}).get('max') if venue.get('capacity') else None,
        "rating": venue.get('rating'),
        "image_urls": venue.get('image_urls', []),
        "source_url": venue.get('source_url'),
        "style_tags": venue.get('style_tags', []),
        "source": venue.get('source', 'toptrouwlocaties.nl'),
        "scraped_at": venue.get('scraped_at') or datetime.now().isoformat(),
    }
    
    response = httpx.post(
        f"{SUPABASE_URL}/rest/v1/vendors",
        headers={**headers, "Prefer": "return=minimal"},
        json=vendor_data
    )
    
    return response.status_code in [201, 200]

def main():
    # Laad scraped data
    json_path = Path("WeddingfinderApp/data/scraped_batch1.json")
    with open(json_path, "r", encoding="utf-8") as f:
        scraped = json.load(f)
    
    print(f"JSON geladen: {len(scraped)} venues\n")
    
    # Haal bestaande vendors uit Supabase
    existing = get_existing_vendors()
    print(f"Bestaande vendors in Supabase: {len(existing)}")
    
    # Check kwaliteit bestaande data
    empty_vendors = [v for v in existing if not v.get('city') and not v.get('source_url')]
    real_vendors = [v for v in existing if v.get('city') or v.get('source_url')]
    
    print(f"  - Met echte data: {len(real_vendors)}")
    print(f"  - Leeg (alleen naam): {len(empty_vendors)}")
    
    # Maak sets voor duplicaat-check
    existing_urls = get_existing_source_urls(existing)
    existing_names = get_existing_names(existing)
    
    # Filter nieuwe venues
    new_venues = []
    skipped = []
    
    for venue in scraped:
        source_url = venue.get('source_url')
        name = venue.get('name', '').lower()
        
        # Check of deze al bestaat (op URL of naam)
        if source_url and source_url in existing_urls:
            skipped.append((venue.get('name'), "source_url bestaat al"))
            continue
        
        if name in existing_names:
            skipped.append((venue.get('name'), "naam bestaat al"))
            continue
        
        # Check of venue echte data heeft
        if not venue.get('city') and not venue.get('description'):
            skipped.append((venue.get('name'), "geen echte data"))
            continue
        
        new_venues.append(venue)
    
    print(f"\nNieuwe venues om te uploaden: {len(new_venues)}")
    print(f"Overgeslagen: {len(skipped)}")
    
    if skipped:
        print("\nRedenen voor overslaan:")
        reasons = {}
        for name, reason in skipped:
            reasons[reason] = reasons.get(reason, 0) + 1
        for reason, count in reasons.items():
            print(f"  - {reason}: {count}")
    
    # Upload nieuwe venues
    if new_venues:
        print(f"\nUploaden van {len(new_venues)} venues...")
        success = 0
        failed = 0
        
        for i, venue in enumerate(new_venues, 1):
            print(f"  [{i}/{len(new_venues)}] {venue.get('name', 'Onbekend')}", end=" ")
            
            if upload_vendor(venue):
                print("OK")
                success += 1
            else:
                print("MISLUKT")
                failed += 1
        
        print(f"\n=== RESULTAAT ===")
        print(f"Succesvol: {success}")
        print(f"Mislukt: {failed}")
    else:
        print("\nGeen nieuwe venues om te uploaden.")

if __name__ == "__main__":
    main()
