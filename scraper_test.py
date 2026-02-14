import httpx
from bs4 import BeautifulSoup
import json
import time

def scrape_listings(limit=5):
    base_url = "https://www.theperfectwedding.nl"
    category_url = f"{base_url}/trouw-feestlocaties"
    
    print(f"Ophalen van categorie: {category_url}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = httpx.get(category_url, headers=headers, follow_redirects=True)
    if response.status_code != 200:
        print(f"Fout bij ophalen pagina: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Zoek naar links die naar bedrijvengids pagina's wijzen
    # Op basis van de eerdere web_search: /bedrijven/[id]/[slug]
    listings = []
    links = soup.find_all('a', href=True)
    business_links = []
    
    for link in links:
        href = link['href']
        if "/bedrijven/" in href and href.count('/') >= 3:
            full_url = base_url + href if href.startswith('/') else href
            if full_url not in business_links:
                business_links.append(full_url)
    
    print(f"{len(business_links)} bedrijven gevonden. We scrapen de eerste {limit}...")
    
    results = []
    for url in business_links[:limit]:
        print(f"Scrapen van: {url}")
        res = httpx.get(url, headers=headers, follow_redirects=True)
        if res.status_code == 200:
            b_soup = BeautifulSoup(res.text, 'html.parser')
            
            # Basis extractie (kan later uitgebreid worden)
            title = b_soup.find('h1').get_text(strip=True) if b_soup.find('h1') else "Geen titel"
            
            # Zoek naar de tekst in de main content
            content_div = b_soup.find('div', class_='content') or b_soup.find('main')
            description = content_div.get_text(strip=True)[:500] + "..." if content_div else "Geen beschrijving"
            
            results.append({
                "name": title,
                "url": url,
                "description": description
            })
            time.sleep(1) # Netjes blijven
            
    with open('wedding_listings.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\nKlaar! {len(results)} resultaten opgeslagen in wedding_listings.json")

if __name__ == "__main__":
    scrape_listings()
