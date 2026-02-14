import httpx
from bs4 import BeautifulSoup
import time
import sys

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"
PORTAL_ID = "9afe381f-b93d-411b-ba81-9cde785f109e"

headers = {
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "apikey": SUPABASE_KEY,
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def get_category_id(slug):
    url = f"{SUPABASE_URL}/rest/v1/categories?slug=eq.{slug}&select=id"
    res = httpx.get(url, headers=headers)
    data = res.json()
    return data[0]['id'] if data else None

def vendor_exists(slug):
    url = f"{SUPABASE_URL}/rest/v1/vendors?slug=eq.{slug}&select=id"
    res = httpx.get(url, headers=headers)
    return len(res.json()) > 0

def save_vendor(vendor_data):
    url = f"{SUPABASE_URL}/rest/v1/vendors"
    vendor_data["portal_id"] = PORTAL_ID
    res = httpx.post(url, json=vendor_data, headers=headers)
    return res.status_code

def scrape_category(category_slug, current_count, target=50):
    cat_id = get_category_id(category_slug)
    if not cat_id:
        print(f"Categorie {category_slug} niet gevonden!", flush=True)
        return current_count

    url_map = {
        "trouwlocaties": "/trouw-feestlocaties/bedrijven",
        "fotografen": "/trouwfotografen/bedrijven",
        "bruidsmode": "/bruidsmode/bedrijven"
    }
    
    base_url = "https://www.theperfectwedding.nl"
    web_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    page = 1
    while current_count < target:
        list_url = f"{base_url}{url_map[category_slug]}"
        if page > 1:
            list_url += f"?p={page}"
        
        print(f"Fetching {list_url}...", flush=True)
        try:
            response = httpx.get(list_url, headers=web_headers, follow_redirects=True, timeout=30)
            if response.status_code != 200:
                print(f"Fout bij ophalen lijst: {response.status_code}", flush=True)
                break
        except Exception as e:
            print(f"Error: {e}", flush=True)
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        business_links = []
        for link in links:
            href = link['href']
            if "/bedrijven/" in href and href.count('/') >= 3:
                full_url = base_url + href if href.startswith('/') else href
                if full_url not in business_links:
                    business_links.append(full_url)
        
        if not business_links:
            print("Geen bedrijven meer gevonden op deze pagina.", flush=True)
            break
            
        print(f"Gevonden op pagina {page}: {len(business_links)} bedrijven.", flush=True)
        
        for url in business_links:
            if current_count >= target:
                break
                
            slug = url.strip('/').split('/')[-1]
            if vendor_exists(slug):
                print(f"  - Skip {slug} (bestaat al)", flush=True)
                continue
            
            print(f"  - Scraping {url}...", flush=True)
            try:
                res = httpx.get(url, headers=web_headers, follow_redirects=True, timeout=30)
                if res.status_code == 200:
                    b_soup = BeautifulSoup(res.text, 'html.parser')
                    name_tag = b_soup.find('h1')
                    name = name_tag.get_text(strip=True) if name_tag else slug
                    
                    description = ""
                    main_tag = b_soup.find('main')
                    if main_tag:
                        description = main_tag.get_text(strip=True)[:1000]
                    
                    vendor = {
                        "name": name,
                        "slug": slug,
                        "theperfectwedding_url": url,
                        "category_id": cat_id,
                        "description": description
                    }
                    
                    status = save_vendor(vendor)
                    if status in [201, 204, 200]:
                        current_count += 1
                        print(f"    => TOEGEVOEGD ({current_count}/{target}): {name}", flush=True)
                    else:
                        print(f"    => FOUT bij opslaan: {status}", flush=True)
                else:
                    print(f"    => FOUT bij ophalen bedrijfspagina: {res.status_code}", flush=True)
            except Exception as e:
                print(f"    => ERROR: {e}", flush=True)
            
            time.sleep(1) # Be nice
            
        page += 1
        
    return current_count

if __name__ == "__main__":
    total_added = 0
    categories = ["trouwlocaties", "fotografen", "bruidsmode"]
    
    for cat in categories:
        if total_added >= 50:
            break
        print(f"\n--- Starten met categorie: {cat} ---", flush=True)
        total_added = scrape_category(cat, total_added, 50)
        
    print(f"\nKLAAR! Totaal nieuwe leveranciers toegevoegd: {total_added}", flush=True)
