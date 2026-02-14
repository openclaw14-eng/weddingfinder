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

def get_portal_id():
    url = f"{SUPABASE_URL}/rest/v1/portals?domain=eq.theperfectwedding.nl&select=id"
    res = httpx.get(url, headers=headers)
    return res.json()[0]['id']

def scrape_all_categories():
    base_url = "https://www.theperfectwedding.nl"
    web_headers = {"User-Agent": "Mozilla/5.0"}
    portal_id = get_portal_id()
    
    # We scrapen de homepage om categorie-links te vinden
    response = httpx.get(base_url, headers=web_headers, follow_redirects=True)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Dit is een versimpelde selectie van categorieën die vaak in de footer of menu staan
    # In een echte run zouden we hier dieper gaan
    categories = [
        {"name": "Trouwlocaties", "url": "/trouw-feestlocaties", "slug": "trouwlocaties"},
        {"name": "Fotografen", "url": "/trouwfotografen", "slug": "fotografen"},
        {"name": "Bruidsmode", "url": "/bruidsmode", "slug": "bruidsmode"},
        {"name": "Trouwpakken", "url": "/trouwpakken", "slug": "trouwpakken"}
    ]
    
    for cat in categories:
        # Check of categorie bestaat, anders aanmaken
        check_url = f"{SUPABASE_URL}/rest/v1/categories?slug=eq.{cat['slug']}&select=id"
        res = httpx.get(check_url, headers=headers)
        if not res.json():
            httpx.post(f"{SUPABASE_URL}/rest/v1/categories", json={
                "name": cat['name'], "slug": cat['slug'], "portal_id": portal_id
            }, headers=headers)
            print(f"Categorie aangemaakt: {cat['name']}")

if __name__ == "__main__":
    scrape_all_categories()
    print("Master setup klaar. Database is nu portal-aware.")
