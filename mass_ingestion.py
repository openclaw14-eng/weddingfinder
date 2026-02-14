import httpx

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "apikey": SUPABASE_KEY,
    "Content-Type": "application/json"
}

def get_cat_id(slug):
    res = httpx.get(f"{SUPABASE_URL}/rest/v1/categories?slug=eq.{slug}&select=id", headers=headers)
    return res.json()[0]['id'] if res.json() else None

def ingest_all():
    # ACTUAL PORTAL ID
    portal_id = "9afe381f-b93d-411b-ba81-9cde785f109e"
    
    # Locaties
    loc_id = get_cat_id("trouwlocaties")
    locaties = [
        {"name": "Hoeve Zzamen", "slug": "hoeve-zzamen", "url": "https://www.theperfectwedding.nl/bedrijven/26718/hoeve-zzamen"},
        {"name": "De Heische Hoeve", "slug": "de-heische-hoeve", "url": "https://www.theperfectwedding.nl/bedrijven/8859/de-heische-hoeve"},
        {"name": "Landgoed Te Werve", "slug": "landgoed-te-werve", "url": "https://www.theperfectwedding.nl/bedrijven/151/landgoed-te-werve"},
        {"name": "Landgoed Groenendaal", "slug": "landgoed-groenendaal", "url": "https://www.theperfectwedding.nl/bedrijven/7046/landgoed-groenendaal"},
        {"name": "Het Scheepvaartmuseum", "slug": "het-scheepvaartmuseum", "url": "https://www.theperfectwedding.nl/bedrijven/6402/het-scheepvaartmuseum"},
        {"name": "Kasteel de Haar", "slug": "kasteel-haar", "url": "https://www.theperfectwedding.nl/bedrijven/199/kasteel-haar"}
    ]
    
    # Fotografen
    fot_id = get_cat_id("fotografen")
    fotografen = [
        {"name": "Trouwfoto.nl", "slug": "trouwfotonl", "url": "https://www.theperfectwedding.nl/bedrijven/39648/trouwfotonl"},
        {"name": "Adindafoto.nl", "slug": "adindafotonl", "url": "https://www.theperfectwedding.nl/bedrijven/1299/adindafotonl"},
        {"name": "Trouwgeluk", "slug": "trouwgeluk-fotografie-film", "url": "https://www.theperfectwedding.nl/bedrijven/21285/trouwgeluk-fotografie-film"},
        {"name": "Shine Moments", "slug": "shine-moments", "url": "https://www.theperfectwedding.nl/bedrijven/18369/shine-moments"}
    ]
    
    # Bruidsmode
    mode_id = get_cat_id("bruidsmode")
    bruidsmode = [
        {"name": "Compagne Bruidsmode", "slug": "5721/compagne-bruidsmode", "url": "https://www.theperfectwedding.nl/bedrijven/5721/compagne-bruidsmode"},
        {"name": "Trouw Bruidsmode", "slug": "26266/trouw-bruidsmode", "url": "https://www.theperfectwedding.nl/bedrijven/26266/trouw-bruidsmode"},
        {"name": "Ann & John", "slug": "355/ann-john-bruidsmode-group", "url": "https://www.theperfectwedding.nl/bedrijven/355/ann-john-bruidsmode-group"}
    ]
    
    all_data = []
    for item in locaties: all_data.append({**item, "category_id": loc_id, "portal_id": portal_id})
    for item in fotografen: all_data.append({**item, "category_id": fot_id, "portal_id": portal_id})
    for item in bruidsmode: all_data.append({**item, "category_id": mode_id, "portal_id": portal_id})
    
    for v in all_data:
        vendor = {
            "name": v['name'],
            "slug": v['slug'],
            "portal_id": v['portal_id'],
            "category_id": v['category_id'],
            "theperfectwedding_url": v['url']
        }
        res = httpx.post(f"{SUPABASE_URL}/rest/v1/vendors", json=vendor, headers=headers)
        print(f"Ingested {v['name']}: {res.status_code}")

if __name__ == "__main__":
    ingest_all()
