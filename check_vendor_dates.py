import httpx

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

response = httpx.get(
    f"{SUPABASE_URL}/rest/v1/vendors?select=name,created_at,slug&order=created_at.asc&limit=100",
    headers=headers
)

if response.status_code == 200:
    vendors = response.json()
    print("Vendors gesorteerd op created_at (oudste eerst):\n")
    for v in vendors[:20]:
        print(f"{v.get('created_at', 'N/A')[:19]} | {v.get('name', 'Onbekend')}")
    print(f"\n... en {len(vendors) - 20} meer")
else:
    print(f"Fout: {response.status_code}")
