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

category_links = {
    "trouwlocaties": [
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
    ],
    "fotografen": [
        "https://www.theperfectwedding.nl/bedrijven/41283/lux-visual-storytellers",
        "https://www.theperfectwedding.nl/bedrijven/14305/underneath-the-apple-tree",
        "https://www.theperfectwedding.nl/bedrijven/3387/dario-endara-photography",
        "https://www.theperfectwedding.nl/bedrijven/5036/nienke-denderen-fotografie",
        "https://www.theperfectwedding.nl/bedrijven/9616/fotografie-film-weddingstudios",
        "https://www.theperfectwedding.nl/bedrijven/17713/first-days-summer",
        "https://www.theperfectwedding.nl/bedrijven/25791/dajana-amelie",
        "https://www.theperfectwedding.nl/bedrijven/40915/marry-me",
        "https://www.theperfectwedding.nl/bedrijven/26655/romy-oomen-photography",
        "https://www.theperfectwedding.nl/bedrijven/238857/woesthuis-fotografie",
        "https://www.theperfectwedding.nl/bedrijven/42098/thijs-and-cher-yourwedding",
        "https://www.theperfectwedding.nl/bedrijven/9272/grace-wedding-stories",
        "https://www.theperfectwedding.nl/bedrijven/42564/ilse-dungen-fotografie",
        "https://www.theperfectwedding.nl/bedrijven/45757/mario-ruiz-photography",
        "https://www.theperfectwedding.nl/bedrijven/226959/q-fotografie",
        "https://www.theperfectwedding.nl/bedrijven/17996/marieke-tromp-trouwfotograaf",
        "https://www.theperfectwedding.nl/bedrijven/19537/roy-wens-bruidsfoto-film",
        "https://www.theperfectwedding.nl/bedrijven/173/pictures-plans",
        "https://www.theperfectwedding.nl/bedrijven/25284/bart-rondeel-photography",
        "https://www.theperfectwedding.nl/bedrijven/13612/marlies-dekker-fotografie",
        "https://www.theperfectwedding.nl/bedrijven/19035/the-wedding-story",
        "https://www.theperfectwedding.nl/bedrijven/22797/marnix-stigter-bruidsfotograaf",
        "https://www.theperfectwedding.nl/bedrijven/25446/precious-people-fotografie",
        "https://www.theperfectwedding.nl/bedrijven/211413/patrick-beek-fotografie",
        "https://www.theperfectwedding.nl/bedrijven/13906/michael-brown-photovideo",
        "https://www.theperfectwedding.nl/bedrijven/39648/trouwfotonl",
        "https://www.theperfectwedding.nl/bedrijven/13837/robin-looy-fotografie",
        "https://www.theperfectwedding.nl/bedrijven/23994/charlene-fotografie",
        "https://www.theperfectwedding.nl/bedrijven/21332/voorbeeld-fotografie",
        "https://www.theperfectwedding.nl/bedrijven/227221/get-framed-photography",
        "https://www.theperfectwedding.nl/bedrijven/23079/balu-bruidsfotografie",
        "https://www.theperfectwedding.nl/bedrijven/9284/kempff-fotografie",
        "https://www.theperfectwedding.nl/bedrijven/15520/wat-plaatje-by-angie-peralta",
        "https://www.theperfectwedding.nl/bedrijven/21387/xenia-kalogiros"
    ],
    "bruidsmode": [
        "https://www.theperfectwedding.nl/bedrijven/742/i-do-i-do",
        "https://www.theperfectwedding.nl/bedrijven/355/ann-john-bruidsmode-group",
        "https://www.theperfectwedding.nl/bedrijven/3435/het-witte-huys-bruidsmode",
        "https://www.theperfectwedding.nl/bedrijven/15178/something-blue-bruidsmode",
        "https://www.theperfectwedding.nl/bedrijven/808/tres-chic-bridal-wear-brandstore",
        "https://www.theperfectwedding.nl/bedrijven/2738/damore-bruidssalon",
        "https://www.theperfectwedding.nl/bedrijven/6900/bruidsboetiek-blauwe-hoeve",
        "https://www.theperfectwedding.nl/bedrijven/362/damore-bruidssalon",
        "https://www.theperfectwedding.nl/bedrijven/25773/de-bruidszaak",
        "https://www.theperfectwedding.nl/bedrijven/361/covers-couture",
        "https://www.theperfectwedding.nl/bedrijven/704/bruidsgalerie-wetering",
        "https://www.theperfectwedding.nl/bedrijven/26054/atelier-edwin-oudshoorn",
        "https://www.theperfectwedding.nl/bedrijven/2938/bruidshuis-diana",
        "https://www.theperfectwedding.nl/bedrijven/2747/valkengoed-wedding-fashion",
        "https://www.theperfectwedding.nl/bedrijven/810/unique-bridal",
        "https://www.theperfectwedding.nl/bedrijven/5721/compagne-bruidsmode",
        "https://www.theperfectwedding.nl/bedrijven/23154/ankii-the-lady-fitzgerald-boutique",
        "https://www.theperfectwedding.nl/bedrijven/285740/het-betuws-bruidshuys",
        "https://www.theperfectwedding.nl/bedrijven/5224/weddingstyles",
        "https://www.theperfectwedding.nl/bedrijven/229344/char-bridal-couture",
        "https://www.theperfectwedding.nl/bedrijven/770/mariage-bruidsmode",
        "https://www.theperfectwedding.nl/bedrijven/17729/bruidskleding-hannelore",
        "https://www.theperfectwedding.nl/bedrijven/686/beijer-besselink-bridal",
        "https://www.theperfectwedding.nl/bedrijven/25803/de-bruidsmode-outlet",
        "https://www.theperfectwedding.nl/bedrijven/7071/bruidsmode-outlet-rotterdam",
        "https://www.theperfectwedding.nl/bedrijven/275078/mwl-bride",
        "https://www.theperfectwedding.nl/bedrijven/5144/your-style-wedding-fashion-ann-john-bruidsmode-group",
        "https://www.theperfectwedding.nl/bedrijven/5145/bruidsmode-outlet-store-ann-john-bruidsmode-group",
        "https://www.theperfectwedding.nl/bedrijven/229202/bergisch-bridal",
        "https://www.theperfectwedding.nl/bedrijven/5118/wedding-company-almere",
        "https://www.theperfectwedding.nl/bedrijven/1927/santerello-bruidsmode",
        "https://www.theperfectwedding.nl/bedrijven/21148/boetiek-bruid",
        "https://www.theperfectwedding.nl/bedrijven/190/ministry-dresses",
        "https://www.theperfectwedding.nl/bedrijven/26266/trouw-bruidsmode",
        "https://www.theperfectwedding.nl/bedrijven/24579/queens-for-him-and-her",
        "https://www.theperfectwedding.nl/bedrijven/803/taft-tule",
        "https://www.theperfectwedding.nl/bedrijven/2775/thandora-bruidsmode",
        "https://www.theperfectwedding.nl/bedrijven/5081/weddings"
    ]
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

def main():
    total_added = 0
    target = 50
    web_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

    category_ids = {slug: get_category_id(slug) for slug in category_links.keys()}
    
    for category_slug, links in category_links.items():
        if total_added >= target:
            break
            
        cat_id = category_ids[category_slug]
        print(f"\n--- Categorie: {category_slug} (ID: {cat_id}) ---", flush=True)
        
        for url in links:
            if total_added >= target:
                break
                
            slug = url.strip('/').split('/')[-1]
            if vendor_exists(slug):
                print(f"  - Skip {slug} (bestaat al)", flush=True)
                continue
                
            print(f"  - Scraping {url}...", flush=True)
            try:
                res = httpx.get(url, headers=web_headers, follow_redirects=True, timeout=30)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, 'html.parser')
                    name_tag = soup.find('h1')
                    name = name_tag.get_text(strip=True) if name_tag else slug
                    
                    description = ""
                    main_tag = soup.find('main')
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
                        total_added += 1
                        print(f"    => TOEGEVOEGD ({total_added}/{target}): {name}", flush=True)
                    else:
                        print(f"    => FOUT bij opslaan: {status}", flush=True)
                else:
                    print(f"    => FOUT bij ophalen: {res.status_code}", flush=True)
            except Exception as e:
                print(f"    => ERROR: {e}", flush=True)
            
            time.sleep(0.5)
            
    print(f"\nKLAAR! Totaal toegevoegd: {total_added}", flush=True)

if __name__ == "__main__":
    main()
