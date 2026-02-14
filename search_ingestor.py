import httpx
import time

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "apikey": SUPABASE_KEY,
    "Content-Type": "application/json"
}

def save_vendors_from_search(results, category_slug):
    # Get IDs
    portal_id = "f0506820-802c-4638-b13c-0975775f0f35"
    cat_res = httpx.get(f"{SUPABASE_URL}/rest/v1/categories?slug=eq.{category_slug}&select=id", headers=headers)
    cat_id = cat_res.json()[0]['id'] if cat_res.json() else None
    
    count = 0
    for r in results:
        url = r.get('url')
        if not url or "/bedrijven/" not in url: continue
        
        name = r.get('title', '').split('|')[0].replace('Trouwlocatie', '').strip()
        slug = url.split('/')[-1]
        
        vendor = {
            "name": name,
            "slug": slug,
            "portal_id": portal_id,
            "category_id": cat_id,
            "theperfectwedding_url": url,
            "description": r.get('description', '')
        }
        
        res = httpx.post(f"{SUPABASE_URL}/rest/v1/vendors", json=vendor, headers=headers)
        if res.status_code == 201:
            count += 1
            print(f"  + {name}")
    return count

if __name__ == "__main__":
    # We simulate getting results from web_search (I'll do this in a loop in the next turn)
    pass
