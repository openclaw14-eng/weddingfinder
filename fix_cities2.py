"""
Fix missing cities for recently uploaded vendors
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

# Laad JSON data om city mapping te maken
with open("WeddingfinderApp/data/scraped_batch1.json", encoding="utf-8") as f:
    json_data = json.load(f)

city_map = {v['name'].lower(): v.get('city') for v in json_data if v.get('city')}
print(f"City mappings uit JSON: {len(city_map)}")

# Haal recente vendors (laatste 50)
resp = httpx.get(
    f"{SUPABASE_URL}/rest/v1/vendors?select=id,name,city,created_at&order=created_at.desc&limit=100",
    headers=headers
)

vendors = resp.json()
print(f"Recente vendors opgehaald: {len(vendors)}")

# Filter zonder city
vendors_without_city = [v for v in vendors if not v.get('city')]
print(f"Vendors zonder city: {len(vendors_without_city)}")

if vendors_without_city:
    print("\nEerste 10 zonder city:")
    for v in vendors_without_city[:10]:
        print(f"  - {v.get('name')}")

# Update met city uit JSON
fixed = 0
for v in vendors_without_city:
    name = v['name'].lower()
    if name in city_map:
        update_resp = httpx.patch(
            f"{SUPABASE_URL}/rest/v1/vendors?id=eq.{v['id']}",
            headers={**headers, "Prefer": "return=minimal"},
            json={"city": city_map[name]}
        )
        if update_resp.status_code in [200, 204]:
            fixed += 1
            print(f"✓ {v['name']} -> {city_map[name]}")
        else:
            print(f"✗ {v['name']} - {update_resp.status_code}")

print(f"\nGefixt: {fixed}/{len(vendors_without_city)}")
