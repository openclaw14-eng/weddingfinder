import httpx
from bs4 import BeautifulSoup

def diagnose():
    url = "https://www.theperfectwedding.nl/trouw-feestlocaties/bedrijven"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    print(f"Fetching {url}...")
    res = httpx.get(url, headers=headers, follow_redirects=True)
    print(f"Status: {res.status_code}")
    
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.find_all('a', href=True)
    
    bedrijven_links = [l['href'] for l in links if "/bedrijven/" in l['href']]
    print(f"Gevonden /bedrijven/ links: {len(bedrijven_links)}")
    for l in bedrijven_links[:10]:
        print(f"  - {l}")

if __name__ == "__main__":
    diagnose()
