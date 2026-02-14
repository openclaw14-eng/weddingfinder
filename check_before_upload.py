import json
import httpx
from pathlib import Path

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

print("1. Ophalen vendors uit Supabase...")
response = httpx.get(
    f"{SUPABASE_URL}/rest/v1/vendors?select=name,theperfectwedding_url,city&limit=1000",
    headers=headers,
    timeout=10
)

if response.status_code != 200:
    print(f"Fout: {response.status_code}")
    print(response.text)
    exit(1)

existing = response.json()
print(f"   Gevonden: {len(existing)} vendors")

print("\n2. Laden JSON data...")
with open("WeddingfinderApp/data/scraped_batch1.json", "r", encoding="utf-8") as f:
    scraped = json.load(f)
print(f"   Gevonden: {len(scraped)} venues")

print("\n3. Analyseren...")
existing_urls = {v.get('theperfectwedding_url') for v in existing if v.get('theperfectwedding_url')}
existing_names = {v.get('name', '').lower() for v in existing}

print(f"   Bestaande URLs in Supabase: {len(existing_urls)}")
print(f"   Bestaande namen in Supabase: {len(existing_names)}")

new_venues = []
for venue in scraped:
    source_url = venue.get('source_url')
    name = venue.get('name', '').lower()
    
    # Check op URL (als die in theperfectwedding_url zit)
    if source_url and source_url in existing_urls:
        continue
    # Check op naam
    if name in existing_names:
        continue
    # Check of venue echte data heeft
    if not venue.get('city') and not venue.get('description'):
        continue
    
    new_venues.append(venue)

print(f"\n   Nieuwe venues: {len(new_venues)}")

# Check overlap
scraped_urls = {v.get('source_url') for v in scraped if v.get('source_url')}
overlap = existing_urls & scraped_urls
print(f"\n4. Overlap analyse:")
print(f"   Bestaande URLs: {len(existing_urls)}")
print(f"   URLs in JSON: {len(scraped_urls)}")
print(f"   Overlap: {len(overlap)}")

if overlap:
    print("\n   Voorbeelden overlap:")
    for url in list(overlap)[:3]:
        print(f"     {url[:60]}...")

if new_venues:
    print("\n5. Voorbeelden nieuwe venues:")
    for v in new_venues[:5]:
        print(f"   - {v.get('name')} ({v.get('city')})")
