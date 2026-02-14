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
with open("WeddingfinderApp/data/scraped_batch1.json") as f:
    json_data = json.load(f)

city_map = {v['name'].lower(): v.get('city') for v in json_data if v.get('city')}

# Haal vendors zonder city op
resp = httpx.get(
    f"{SUPABASE_URL}/rest/v1/vendors?select=id,name,city&is.city.null=true&limit=1000",
    headers=headers
)

vendors_without_city = resp.json()
print(f"Vendors zonder city: {len(vendors_without_city)}")

# Update met city
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
            print(f"Fixed: {v['name']} -> {city_map[name]}")
        else:
            print(f"Failed: {v['name']} - {update_resp.status_code}")

print(f"\nTotaal gefixt: {fixed}/{len(vendors_without_city)}")
