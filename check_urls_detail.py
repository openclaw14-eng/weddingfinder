import httpx

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Check 5 vendors uit Supabase
response = httpx.get(
    f"{SUPABASE_URL}/rest/v1/vendors?select=name,theperfectwedding_url,city,slug&limit=5",
    headers=headers
)

if response.status_code == 200:
    vendors = response.json()
    print("Voorbeelden uit Supabase:")
    for v in vendors:
        print(f"\n  {v['name']}")
        print(f"    URL: {v.get('theperfectwedding_url', 'LEEG')}")
        print(f"    City: {v.get('city', 'LEEG')}")
        print(f"    Slug: {v['slug']}")
