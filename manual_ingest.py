import httpx
import time

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"
PORTAL_ID = "9afe381f-b93d-411b-ba81-9cde785f109e"
CAT_ID = "fb38b25f-27f1-432d-965a-8b17351660f5" # Trouwlocaties

headers = {
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "apikey": SUPABASE_KEY,
    "Content-Type": "application/json"
}

links = [
    "https://www.theperfectwedding.nl/bedrijven/2812/kasteel-woerden",
    "https://www.theperfectwedding.nl/bedrijven/18550/grand-cafe-borg-nienoord",
    "https://www.theperfectwedding.nl/bedrijven/13855/slot-moermond",
    "https://www.theperfectwedding.nl/bedrijven/11863/grand-cafe-el-molino",
    "https://www.theperfectwedding.nl/bedrijven/11956/de-schildhoeve",
    "https://www.theperfectwedding.nl/bedrijven/14242/plok",
    "https://www.theperfectwedding.nl/bedrijven/224/kasteel-wijenburg",
    "https://www.theperfectwedding.nl/bedrijven/12482/het-brabantse-land",
    "https://www.theperfectwedding.nl/bedrijven/41398/hotel-marktstad",
    "https://www.theperfectwedding.nl/bedrijven/2868/haarlemmermeerstation",
    "https://www.theperfectwedding.nl/bedrijven/281166/brasserie-laegt",
    "https://www.theperfectwedding.nl/bedrijven/239098/delbrock",
    "https://www.theperfectwedding.nl/bedrijven/15122/landgoed-klarenbeek",
    "https://www.theperfectwedding.nl/bedrijven/5532/lambertuskerk-raamsdonk",
    "https://www.theperfectwedding.nl/bedrijven/238855/helling7",
    "https://www.theperfectwedding.nl/bedrijven/17906/harteluk-natuurpark",
    "https://www.theperfectwedding.nl/bedrijven/2661/slot-doddendael",
    "https://www.theperfectwedding.nl/bedrijven/26718/hoeve-zzamen",
    "https://www.theperfectwedding.nl/bedrijven/8770/innesto",
    "https://www.theperfectwedding.nl/bedrijven/222144/koks-gemert",
    "https://www.theperfectwedding.nl/bedrijven/5229/abel-grand-cafe-restaurant",
    "https://www.theperfectwedding.nl/bedrijven/8426/strandpaviljoen-thalassa",
    "https://www.theperfectwedding.nl/bedrijven/3352/restaurant-boswachter-liesbosch",
    "https://www.theperfectwedding.nl/bedrijven/2430/het-kasteel-rhoon",
    "https://www.theperfectwedding.nl/bedrijven/6747/beachclub-zuiderduin",
    "https://www.theperfectwedding.nl/bedrijven/286138/casa-do-alto",
    "https://www.theperfectwedding.nl/bedrijven/17456/de-theeschenkerij-velserbeek",
    "https://www.theperfectwedding.nl/bedrijven/6729/hotel-restaurant-de-zeegser-duinen",
    "https://www.theperfectwedding.nl/bedrijven/280797/de-schaapjes-haaren",
    "https://www.theperfectwedding.nl/bedrijven/287315/restaurant-hemels",
    "https://www.theperfectwedding.nl/bedrijven/5579/het-wapen-zoetermeer",
    "https://www.theperfectwedding.nl/bedrijven/2394/gasterij-vergeer",
    "https://www.theperfectwedding.nl/bedrijven/18137/villa-clementine",
    "https://www.theperfectwedding.nl/bedrijven/6863/de-brabantse-hoeve",
    "https://www.theperfectwedding.nl/bedrijven/13909/de-bronckhorst-hoeve",
    "https://www.theperfectwedding.nl/bedrijven/2873/landgoed-rhederoord",
    "https://www.theperfectwedding.nl/bedrijven/2876/de-havixhorst",
    "https://www.theperfectwedding.nl/bedrijven/2590/orangerie-elswout",
    "https://www.theperfectwedding.nl/bedrijven/22540/buitenplaats-land-es",
    "https://www.theperfectwedding.nl/bedrijven/325/buitenplaats-sparrendaal",
    "https://www.theperfectwedding.nl/bedrijven/341/landgoed-groot-warnsborn"
]

def ingest():
    count = 0
    for url in links:
        slug = url.strip('/').split('/')[-1]
        name = slug.replace('-', ' ').title()
        
        vendor = {
            "name": name,
            "slug": slug,
            "portal_id": PORTAL_ID,
            "category_id": CAT_ID,
            "theperfectwedding_url": url
        }
        
        r = httpx.post(f"{SUPABASE_URL}/rest/v1/vendors", json=vendor, headers=headers)
        if r.status_code in [201, 204, 200]:
            count += 1
            print(f"  + {name}")
        elif r.status_code == 409:
            print(f"  - Skip {name} (exists)")
        else:
            print(f"  ! Error {name}: {r.status_code}")
    
    print(f"Done. Ingested {count} vendors.")

if __name__ == "__main__":
    ingest()
