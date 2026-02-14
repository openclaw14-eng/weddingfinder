import httpx
import json

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "apikey": SUPABASE_KEY,
    "Content-Type": "application/json"
}

def get_unoptimized_vendors():
    # Haal vendors op zonder SEO titel
    url = f"{SUPABASE_URL}/rest/v1/vendors?seo_title=is.null&limit=10"
    res = httpx.get(url, headers=headers)
    return res.json()

def update_vendor_seo(vendor_id, seo_data):
    url = f"{SUPABASE_URL}/rest/v1/vendors?id=eq.{vendor_id}"
    res = httpx.patch(url, json=seo_data, headers=headers)
    return res.status_code

def run_seo_optimization():
    vendors = get_unoptimized_vendors()
    print(f"Optimaliseren van {len(vendors)} vendors...")
    
    for v in vendors:
        name = v['name']
        # Simpele SEO generator (kan later via LLM sub-agent)
        seo_title = f"{name} - Beste Trouwlocatie in {v.get('city', 'Nederland')} | Jouw Bruiloft"
        seo_desc = f"Ontdek alles over {name}. Bekijk foto's, prijzen en ervaringen van dit prachtige bedrijf op ons platform."
        
        data = {
            "seo_title": seo_title,
            "seo_description": seo_desc,
            "keywords": [name, "trouwen", "bruiloft", v.get('city', 'Nederland')]
        }
        
        status = update_vendor_seo(v['id'], data)
        print(f"SEO geupdate voor {name} (Status: {status})")

if __name__ == "__main__":
    run_seo_optimization()
