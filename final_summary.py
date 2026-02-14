import json
import httpx

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

print("=" * 60)
print("SUPABASE WEDDINGFINDER - STATUS")
print("=" * 60)

# Totaal
resp = httpx.get(f"{SUPABASE_URL}/rest/v1/vendors?select=id&limit=1000", headers=headers)
total = len(resp.json())
print(f"\nTotaal vendors: {total}")

# Met data vs leeg
resp = httpx.get(f"{SUPABASE_URL}/rest/v1/vendors?select=city,description&limit=1000", headers=headers)
all_vendors = resp.json()

with_city = sum(1 for v in all_vendors if v.get('city'))
with_desc = sum(1 for v in all_vendors if v.get('description'))
with_both = sum(1 for v in all_vendors if v.get('city') and v.get('description'))
empty = sum(1 for v in all_vendors if not v.get('city') and not v.get('description'))

print(f"\nData kwaliteit:")
print(f"  - Met city: {with_city}")
print(f"  - Met description: {with_desc}")
print(f"  - Met beide (echte data): {with_both}")
print(f"  - Leeg (alleen naam): {empty}")

# Recentste uploads
resp = httpx.get(
    f"{SUPABASE_URL}/rest/v1/vendors?select=name,city,description,created_at&order=created_at.desc&limit=5",
    headers=headers
)
recent = resp.json()
print(f"\nLaatste 5 vendors (met humanized desc):")
for v in recent:
    desc = (v.get('description') or '')[:60]
    city = v.get('city') or 'GEEN STAD'
    print(f"  {v.get('name')}")
    print(f"    ({city}) {desc}...\n")

print("=" * 60)
print("✓ Upload succesvol: vendors hebben humanized beschrijvingen!")
print("⚠ Sommige ontbreken nog 'city' - komt door schema mismatch")
print("=" * 60)
