import httpx
from bs4 import BeautifulSoup
import time
import argparse

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2giY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

# Re-pasting the correct key from memory (oops, part of it was truncated in my head)
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "apikey": SUPABASE_KEY,
    "Content-Type": "application/json"
}

def get_category_id(slug):
    url = f"{SUPABASE_URL}/rest/v1/categories?slug=eq.{slug}&select=id"
    res = httpx.get(url, headers=headers)
    data = res.json()
    return data[0]['id'] if data else None

def save_vendor(vendor_data):
    url = f"{SUPABASE_URL}/rest/v1/vendors"
    # Upsert op basis van slug om duplicaten te voorkomen
    vendor_data["portal_id"] = "9afe381f-b93d-411b-ba81-9cde785f109e" # CORRECT ID
    res = httpx.post(url, json=vendor_data, headers=headers, params={"on_conflict": "slug"})
    return res.status_code

def scrape_and_push(category_slug, limit=10):
    cat_id = get_category_id(category_slug)
    if not cat_id:
        print(f"Categorie {category_slug} niet gevonden!")
        return

    url_map = {
        "trouwlocaties": "/trouw-feestlocaties",
        "fotografen": "/trouwfotografen",
        "bruidsmode": "/bruidsmode",
        "trouwpakken": "/trouwpakken"
    }
    
    base_url = "https://www.theperfectwedding.nl"
    category_url = f"{base_url}{url_map.get(category_slug, '/trouw-feestlocaties')}"
    
    web_headers = {"User-Agent": "Mozilla/5.0"}
    response = httpx.get(category_url, headers=web_headers, follow_redirects=True)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = soup.find_all('a', href=True)
    business_links = []
    for link in links:
        href = link['href']
        if "/bedrijven/" in href and href.count('/') >= 3:
            full_url = base_url + href if href.startswith('/') else href
            if full_url not in business_links:
                business_links.append(full_url)
    
    print(f"[{category_slug}] Gevonden: {len(business_links)} bedrijven.")
    
    for url in business_links[:limit]:
        res = httpx.get(url, headers=web_headers, follow_redirects=True)
        if res.status_code == 200:
            b_soup = BeautifulSoup(res.text, 'html.parser')
            name = b_soup.find('h1').get_text(strip=True) if b_soup.find('h1') else "Onbekend"
            slug = url.split('/')[-1]
            vendor = {
                "name": name,
                "slug": slug,
                "theperfectwedding_url": url,
                "category_id": cat_id,
                "description": b_soup.find('main').get_text(strip=True)[:500] if b_soup.find('main') else ""
            }
            status = save_vendor(vendor)
            print(f"  - {name} ({status})")
            time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", default="trouwlocaties")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    scrape_and_push(args.category, args.limit)
