import httpx

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Probeer alle mogelijke tabellen
tables_to_check = ["vendors", "venues", "locations", "wedding_venues", "companies", "businesses", "places"]

print("Check alle tabellen in Supabase:\n")

for table in tables_to_check:
    # Eerst count ophalen
    count_response = httpx.get(
        f"{SUPABASE_URL}/rest/v1/{table}?select=id",
        headers={**headers, "Prefer": "count=exact"}
    )
    
    total_count = "?"
    if count_response.status_code == 200:
        # Count zit in Content-Range header
        content_range = count_response.headers.get("content-range", "")
        if "/" in content_range:
            total_count = content_range.split("/")[-1]
    
    response = httpx.get(
        f"{SUPABASE_URL}/rest/v1/{table}?select=*&limit=5",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f" {table}: {total_count} totaal, {len(data)} getoond")
        if data:
            # Toon velden van eerste item
            fields = list(data[0].keys())
            print(f"   Kolommen: {', '.join(fields[:10])}{'...' if len(fields) > 10 else ''}")
            # Check of er data in zit
            sample = data[0]
            has_data = any(v for k, v in sample.items() if v and k != 'id' and k != 'created_at' and k != 'name')
            if has_data:
                print(f"   -> Bevat data! (naast alleen id/naam)")
                print(f"   Sample: {sample.get('name', 'N/A')[:50]}")
                if sample.get('city'):
                    print(f"           City: {sample.get('city')}")
                if sample.get('description'):
                    print(f"           Description: {str(sample.get('description'))[:60]}...")
        print()
    else:
        print(f" {table}: {response.status_code} (niet gevonden of geen toegang)")
