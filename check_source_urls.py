import httpx

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Check de source_url van Supabase vendors
response = httpx.get(
    f"{SUPABASE_URL}/rest/v1/vendors?select=name,source_url,created_at&limit=1000",
    headers=headers
)

if response.status_code == 200:
    vendors = response.json()
    print(f"Totaal: {len(vendors)} vendors\n")
    
    # Groepeer per bron
    sources = {}
    for v in vendors:
        url = v.get('source_url', '') or 'GEEN URL'
        if 'theperfectwedding' in url:
            src = 'theperfectwedding.nl'
        elif 'toptrouwlocaties' in url:
            src = 'toptrouwlocaties.nl'
        elif 'ceremoniemeester' in url:
            src = 'ceremoniemeester.nl'
        elif url == 'GEEN URL':
            src = 'GEEN BRON'
        else:
            src = url[:40]
        sources[src] = sources.get(src, 0) + 1
    
    print("Bronnen:")
    for src, count in sorted(sources.items(), key=lambda x: -x[1]):
        print(f"  {src}: {count}")
    
    # Toon een paar voorbeelden zonder URL
    no_url = [v for v in vendors if not v.get('source_url')]
    if no_url:
        print(f"\nVoorbeelden zonder source_url:")
        for v in no_url[:10]:
            print(f"  - {v.get('name')}")
