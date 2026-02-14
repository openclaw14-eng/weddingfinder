import httpx

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Ophalen ALLE vendors
print("Ophalen ALLE vendors uit Supabase...")
all_vendors = []
offset = 0
limit = 1000

while True:
    response = httpx.get(
        f"{SUPABASE_URL}/rest/v1/vendors?select=*&limit={limit}&offset={offset}",
        headers=headers
    )
    if response.status_code != 200:
        print(f"Fout bij offset {offset}: {response.text}")
        break
    
    batch = response.json()
    if not batch:
        break
    
    all_vendors.extend(batch)
    print(f"  Offset {offset}: {len(batch)} vendors (totaal: {len(all_vendors)})")
    
    if len(batch) < limit:
        break
    offset += limit

print(f"\n=== TOTAAL: {len(all_vendors)} vendors in Supabase ===\n")

# Check welke velden gevuld zijn
vendors_with_desc = [v for v in all_vendors if v.get('description')]
vendors_with_city = [v for v in all_vendors if v.get('city')]
vendors_with_address = [v for v in all_vendors if v.get('address')]
vendors_with_images = [v for v in all_vendors if v.get('images') and v.get('images') != []]

print(f"Met description: {len(vendors_with_desc)}")
print(f"Met city: {len(vendors_with_city)}")
print(f"Met address: {len(vendors_with_address)}")
print(f"Met images: {len(vendors_with_images)}\n")

# Toon de rijkste entries
rich_vendors = [v for v in all_vendors if v.get('description') or v.get('city') or v.get('address')]
if rich_vendors:
    print(f"=== {len(rich_vendors)} vendors MET data ===")
    for v in rich_vendors[:20]:
        print(f"\n> {v.get('name', 'Onbekend')}")
        if v.get('city'): print(f"  City: {v.get('city')}")
        if v.get('address'): print(f"  Address: {v.get('address')[:80]}..." if len(v.get('address', '')) > 80 else f"  Address: {v.get('address')}")
        if v.get('description'): print(f"  Description: {v.get('description')[:100]}..." if len(v.get('description', '')) > 100 else f"  Description: {v.get('description')}")
        if v.get('images'): print(f"  Images: {len(v.get('images'))} afbeeldingen")
else:
    print("Geen vendors met city/address/description gevonden in Supabase")
