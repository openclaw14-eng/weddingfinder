import httpx

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Haal alle 80 vendors op
print("Ophalen alle 80 vendors...\n")
response = httpx.get(
    f"{SUPABASE_URL}/rest/v1/vendors?select=*&limit=100",
    headers=headers
)

if response.status_code == 200:
    vendors = response.json()
    print(f"Totaal opgehaald: {len(vendors)}\n")
    
    # Check welke vendors data hebben
    print("=== DETAIL CHECK ===\n")
    
    for i, v in enumerate(vendors):
        name = v.get('name', 'Geen naam')
        
        # Check alle velden
        has_city = bool(v.get('city'))
        has_address = bool(v.get('address'))
        has_description = bool(v.get('description'))
        has_phone = bool(v.get('phone'))
        has_website = bool(v.get('website'))
        has_image = bool(v.get('image_url'))
        has_slug = bool(v.get('slug'))
        
        # Alleen tonen als er iets anders is dan alleen naam
        if has_city or has_address or has_description or has_phone or has_website or has_image or has_slug:
            print(f"#{i+1}: {name}")
            if has_city: print(f"   City: {v.get('city')}")
            if has_address: print(f"   Address: {v.get('address')[:60]}..." if len(v.get('address','')) > 60 else f"   Address: {v.get('address')}")
            if has_description: 
                desc = str(v.get('description'))
                print(f"   Description: {desc[:80]}..." if len(desc) > 80 else f"   Description: {desc}")
            if has_phone: print(f"   Phone: {v.get('phone')}")
            if has_website: print(f"   Website: {v.get('website')}")
            if has_image: print(f"   Image: {v.get('image_url')[:60]}..." if len(v.get('image_url','')) > 60 else f"   Image: {v.get('image_url')}")
            if has_slug: print(f"   Slug: {v.get('slug')}")
            print()
    
    # Samenvatting
    cities = sum(1 for v in vendors if v.get('city'))
    addresses = sum(1 for v in vendors if v.get('address'))
    descriptions = sum(1 for v in vendors if v.get('description'))
    phones = sum(1 for v in vendors if v.get('phone'))
    websites = sum(1 for v in vendors if v.get('website'))
    images = sum(1 for v in vendors if v.get('image_url'))
    slugs = sum(1 for v in vendors if v.get('slug'))
    
    print("\n=== SAMENVATTING ===")
    print(f"Totaal vendors: {len(vendors)}")
    print(f"Met city: {cities}")
    print(f"Met address: {addresses}")
    print(f"Met description: {descriptions}")
    print(f"Met phone: {phones}")
    print(f"Met website: {websites}")
    print(f"Met image_url: {images}")
    print(f"Met slug: {slugs}")
    
    # Check of "Landgoed Huis de Voorst" erin zit
    target = "Landgoed Huis de Voorst"
    found = [v for v in vendors if target.lower() in v.get('name', '').lower()]
    if found:
        print(f"\n=== '{target}' GEVONDEN ===")
        for v in found:
            print(f"Naam: {v.get('name')}")
            print(f"Alle velden: {v}")
    else:
        print(f"\n=== '{target}' NIET in Supabase ===")
        print("Dit staat alleen in scraped_batch1.json, niet in de database")
        
else:
    print(f"Fout: {response.status_code}")
    print(response.text)
