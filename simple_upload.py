import json
import httpx

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Get existing
resp = httpx.get(f"{SUPABASE_URL}/rest/v1/vendors?select=name&limit=1000", headers=headers)
existing = {v['name'].lower() for v in resp.json()}
print(f"Existing: {len(existing)}")

# Load JSON
with open("WeddingfinderApp/data/scraped_batch1.json") as f:
    data = json.load(f)
print(f"JSON: {len(data)}")

# Filter new with city
new = [v for v in data if v.get('name', '').lower() not in existing and v.get('city')]
print(f"New to upload: {len(new)}")

if new:
    print(f"\nUploading first 1 as test: {new[0]['name']}")
    venue = new[0]
    payload = {
        "name": venue['name'],
        "slug": venue['name'].lower().replace(' ', '-'),
        "city": venue['city'],
        "description": f"Trouwen bij {venue['name']} in {venue['city']} — een sfeervolle locatie voor jullie bijzondere dag. Perfect voor {venue.get('capacity', {}).get('min', '')}-{venue.get('capacity', {}).get('max', '')} gasten.",
        "rating": venue.get('rating'),
        "image_url": venue.get('image_urls', [None])[0],
        "theperfectwedding_url": venue.get('source_url'),
        "source": venue.get('source', 'toptrouwlocaties.nl'),
        "is_premium": False,
        "keywords": venue.get('style_tags', [])
    }
    
    resp = httpx.post(f"{SUPABASE_URL}/rest/v1/vendors", headers={**headers, "Prefer": "return=minimal"}, json=payload)
    print(f"Result: {resp.status_code}")
    if resp.status_code not in [200, 201, 204]:
        print(f"Error: {resp.text}")
else:
    print("No new venues to upload")
