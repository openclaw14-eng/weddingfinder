import json
import httpx

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Eerst simpele check
print("1. Ophalen vendors uit Supabase...")
response = httpx.get(
    f"{SUPABASE_URL}/rest/v1/vendors?select=name",
    headers=headers
)
print(f"   Status: {response.status_code}")
print(f"   Content-Range: {response.headers.get('content-range', 'N/A')}")

if response.status_code == 200:
    supabase_vendors = response.json()
    print(f"   Aantal vendors: {len(supabase_vendors)}")
    
    # Laad JSON data
    print("\n2. Laden scraped_batch1.json...")
    with open("WeddingfinderApp/data/scraped_batch1.json", "r", encoding="utf-8") as f:
        scraped = json.load(f)
    print(f"   Aantal in JSON: {len(scraped)}")
    
    # Vergelijk
    supabase_names = {v['name'].lower() for v in supabase_vendors}
    scraped_names = {v['name'].lower() for v in scraped}
    
    overlap = supabase_names & scraped_names
    only_supabase = supabase_names - scraped_names
    only_scraped = scraped_names - supabase_names
    
    print(f"\n3. Vergelijking:")
    print(f"   In beide: {len(overlap)}")
    print(f"   Alleen Supabase: {len(only_supabase)}")
    print(f"   Alleen JSON: {len(only_scraped)}")
    
    if only_supabase:
        print(f"\n4. Voorbeelden ALLEEN in Supabase:")
        for name in list(only_supabase)[:5]:
            print(f"   - {name}")
    
    if overlap:
        print(f"\n5. Voorbeelden in BEIDE:")
        for name in list(overlap)[:5]:
            print(f"   - {name}")
    else:
        print("\n5. GEEN overlap!")
        print("   Dit betekent: de 80 vendors in Supabase zijn NOOIT gescraped naar JSON")
        print("   Ze zijn via een andere weg in Supabase gekomen.")
