import json
import httpx

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Haal ALLE Supabase vendors op (max 1000)
response = httpx.get(
    f"{SUPABASE_URL}/rest/v1/vendors?select=name,slug,city,source_url,created_at&limit=1000",
    headers=headers
)

supabase_vendors = response.json() if response.status_code == 200 else []
print(f"Supabase vendors: {len(supabase_vendors)}")

# Laad scraped data
with open("WeddingfinderApp/data/scraped_batch1.json", "r", encoding="utf-8") as f:
    scraped = json.load(f)

print(f"Scraped vendors in JSON: {len(scraped)}")

# Vergelijk namen
supabase_names = {v['name'].lower() for v in supabase_vendors}
scraped_names = {v['name'].lower() for v in scraped}

overlap = supabase_names & scraped_names
only_supabase = supabase_names - scraped_names
only_scraped = scraped_names - supabase_names

print(f"\nOverlap (in beide): {len(overlap)}")
print(f"Alleen in Supabase: {len(only_supabase)}")
print(f"Alleen in JSON: {len(only_scraped)}")

if overlap:
    print("\nVendors die in BEIDE zitten:")
    for name in list(overlap)[:10]:
        print(f"  - {name}")

# Laat zien wanneer Supabase vendors zijn aangemaakt
print("\nEerste 5 Supabase vendors (op created_at):")
sorted_vendors = sorted(supabase_vendors, key=lambda x: x.get('created_at', ''))
for v in sorted_vendors[:5]:
    print(f"  {v.get('created_at', 'N/A')[:19]} | {v.get('name')}")
