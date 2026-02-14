import httpx
from bs4 import BeautifulSoup
import time

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "apikey": SUPABASE_KEY,
    "Content-Type": "application/json"
}

def scrape_category(category_slug, max_pages=5):
    cat_id = "fb38b25f-27f1-432d-965a-8b17351660f5" # ID voor trouwlocaties (eerder opgehaald)
    portal_id = "f0506820-802c-4638-b13c-0975775f0f35"
    
    base_url = "https://www.theperfectwedding.nl"
    path = "/trouw-feestlocaties" if category_slug == "trouwlocaties" else "/trouwfotografen"
    
    for page in range(1, max_pages + 1):
        url = f"{base_url}{path}?page={page}"
        print(f"Pagina {page} ophalen...")
        
        res = httpx.get(url, headers={"User-Agent": "Mozilla/5.0"}, follow_redirects=True)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Zoek naar alle bedrijfskaarten
        # PW gebruikt vaak specifieke classes voor hun listings
        listings = soup.select('a[href*="/bedrijven/"]')
        found_on_page = 0
        
        for link in listings:
            href = link['href']
            if href.count('/') >= 3:
                full_url = base_url + href if href.startswith('/') else href
                slug = full_url.split('/')[-1]
                name = link.get_text(strip=True) or slug
                
                # Sla op in Supabase
                vendor = {
                    "name": name,
                    "slug": slug,
                    "portal_id": portal_id,
                    "category_id": cat_id,
                    "theperfectwedding_url": full_url
                }
                
                # POST met on_conflict=slug (upsert)
                # Opmerking: PostgREST upsert via query param
                r = httpx.post(f"{SUPABASE_URL}/rest/v1/vendors", json=vendor, headers=headers, params={"on_conflict": "slug"})
                if r.status_code in [201, 409]:
                    found_on_page += 1
        
        print(f"Pagina {page} klaar. {found_on_page} nieuwe/geupdate vendors.")
        if found_on_page == 0: break # Geen resultaten meer
        time.sleep(1)

if __name__ == "__main__":
    scrape_category("trouwlocaties", max_pages=10)
