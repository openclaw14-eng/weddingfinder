import httpx

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Haal recente vendors op
resp = httpx.get(
    f"{SUPABASE_URL}/rest/v1/vendors?select=name,city,description,created_at&order=created_at.desc&limit=20",
    headers=headers
)

if resp.status_code == 200:
    vendors = resp.json()
    print(f"Recente {len(vendors)} vendors (nieuwste eerst):\n")
    
    for v in vendors[:10]:
        desc = v.get('description', '') or 'GEEN BESCHRIJVING'
        print(f"{v.get('created_at', 'N/A')[:19]} | {v.get('name')}")
        print(f"  City: {v.get('city', 'None')}")
        print(f"  Desc: {desc[:100]}...\n")
    
    # Check met echte data
    with_city = sum(1 for v in vendors if v.get('city'))
    with_desc = sum(1 for v in vendors if v.get('description'))
    print(f"Van deze 20:")
    print(f"  - Met city: {with_city}")
    print(f"  - Met description: {with_desc}")
