import httpx
from bs4 import BeautifulSoup
import time
import json

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "apikey": SUPABASE_KEY,
    "Content-Type": "application/json"
}

def log_progress(msg, progress=0):
    with open("scraper_progress.json", "w") as f:
        json.dump({"message": msg, "progress": progress, "timestamp": time.time()}, f)

def heavy_scraper():
    portal_id = "f0506820-802c-4638-b13c-0975775f0f35"
    cat_id = "fb38b25f-27f1-432d-965a-8b17351660f5" # Trouwlocaties
    
    base_url = "https://www.theperfectwedding.nl"
    # Correct URL structure found via search
    regions = ["noord-holland", "zuid-holland", "utrecht", "noord-brabant", "gelderland"]
    
    total_added = 0
    
    for i, region in enumerate(regions):
        pct = int((i / len(regions)) * 100)
        log_progress(f"Regio {region} scannen...", pct)
        
        # CORRECT URL
        url = f"{base_url}/trouw-feestlocaties/in/provincie/{region}"
        print(f"Scannen regio: {region} ({url})")
        
        try:
            res = httpx.get(url, headers={"User-Agent": "Mozilla/5.0"}, follow_redirects=True, timeout=15)
            if res.status_code != 200:
                print(f"Fout bij {region}: Status {res.status_code}")
                continue
                
            soup = BeautifulSoup(res.text, 'html.parser')
            # De bedrijven staan vaak in a tags met /bedrijven/ in de href
            links = soup.find_all('a', href=True)
            
            region_added = 0
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
                        "theperfectwedding_url": full_url,
                        "city": region.replace('-', ' ').title() # Voorlopige stad
                    }
                    
                    r = httpx.post(f"{SUPABASE_URL}/rest/v1/vendors", json=vendor, headers=headers)
                    if r.status_code == 201:
                        region_added += 1
                        total_added += 1
                        print(f"  + {name}")
            
            print(f"Klaar met {region}: {region_added} nieuwe toegevoegd.")
            time.sleep(2)
        except Exception as e:
            print(f"Fout bij {region}: {e}")

    log_progress(f"Scan voltooid! {total_added} nieuwe vendors.", 100)

if __name__ == "__main__":
    heavy_scraper()
