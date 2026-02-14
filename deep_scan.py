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

def deep_scrape():
    portal_id = "f0506820-802c-4638-b13c-0975775f0f35"
    cat_id = "fb38b25f-27f1-432d-965a-8b17351660f5" # Trouwlocaties
    
    base_url = "https://www.theperfectwedding.nl"
    # We gaan naar de specifieke gids pagina
    url = f"{base_url}/trouw-feestlocaties"
    
    print("Diepe scan starten...")
    res = httpx.get(url, headers={"User-Agent": "Mozilla/5.0"}, follow_redirects=True)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # Zoek naar ALLE links die naar /bedrijven/ gaan
    # We filteren op links die een naam bevatten
    links = soup.find_all('a', href=True)
    count = 0
    for link in links:
        href = link['href']
        if "/bedrijven/" in href and href.count('/') >= 3:
            full_url = base_url + href if href.startswith('/') else href
            name = link.get_text(strip=True)
            if not name or len(name) < 3: continue
            
            slug = full_url.split('/')[-1]
            
            vendor = {
                "name": name,
                "slug": slug,
                "portal_id": portal_id,
                "category_id": cat_id,
                "theperfectwedding_url": full_url
            }
            
            r = httpx.post(f"{SUPABASE_URL}/rest/v1/vendors", json=vendor, headers=headers)
            if r.status_code == 201:
                count += 1
                print(f"Nieuw: {name}")
    
    print(f"Scan klaar. {count} nieuwe bedrijven toegevoegd.")

if __name__ == "__main__":
    deep_scrape()
