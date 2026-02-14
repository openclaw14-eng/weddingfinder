import httpx

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM5fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Haal 1 vendor op
response = httpx.get(
    f"{SUPABASE_URL}/rest/v1/vendors?select=*&limit=1",
    headers=headers
)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Aantal: {len(data)}")
    if data:
        print(f"Keys: {list(data[0].keys())}")
        print(f"Data: {data[0]}")
else:
    print(f"Fout: {response.text}")
