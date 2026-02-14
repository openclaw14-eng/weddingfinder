import httpx
from bs4 import BeautifulSoup
import json
import time

def scrape_vendors():
    # 1. Get region URLs
    sitemap_url = "https://www.theperfectwedding.nl/trouw-feestlocaties/regions.xml"
    response = httpx.get(sitemap_url)
    soup = BeautifulSoup(response.content, "html.parser")
    region_urls = [loc.text for loc in soup.find_all("loc")]
    
    vendors = []
    
    # Process first few regions to get enough vendors quickly
    for region_url in region_urls[:10]:
        print(f"Scraping region: {region_url}")
        res = httpx.get(region_url)
        content = res.text
        
        # Look for the JSON blob in the :profile-lists attribute
        # It's inside a Vue component often
        try:
            start_str = ':profile-lists="'
            start_idx = content.find(start_str) + len(start_str)
            end_idx = content.find(']"', start_idx) + 1
            json_blob = content[start_idx:end_idx].replace('&quot;', '"')
            data = json.loads(json_blob)
            
            for list_item in data:
                for vendor_data in list_item:
                    vendor = {
                        "id": vendor_data.get("id"),
                        "name": vendor_data.get("name"),
                        "city": vendor_data.get("city"),
                        "state": vendor_data.get("state"),
                        "url": vendor_data.get("url"),
                        "price": vendor_data.get("averageWeddingPrice"),
                        "rating": vendor_data.get("total_rating", {}).get("mean"),
                        "reviews": vendor_data.get("total_rating", {}).get("count"),
                    }
                    vendors.append(vendor)
                    if len(vendors) >= 600:
                        break
                if len(vendors) >= 600: break
        except Exception as e:
            print(f"Error parsing region {region_url}: {e}")
            
        if len(vendors) >= 600:
            break
        time.sleep(1)

    with open("vendors_basic.json", "w") as f:
        json.dump(vendors, f)
    
    print(f"Found {len(vendors)} vendors. Now fetching details for first 500...")
    
    detailed_vendors = []
    for i, v in enumerate(vendors[:500]):
        if i % 10 == 0: print(f"Processing detail {i}...")
        try:
            res = httpx.get(v["url"])
            soup = BeautifulSoup(res.text, "html.parser")
            
            description = soup.find("div", class_="description-text")
            v["description"] = description.text.strip() if description else ""
            
            # Extract capacity from the page
            # Look for capacity section
            cap_section = soup.find("h2", string="Capaciteit")
            if cap_section:
                cap_div = cap_section.find_next("div")
                if cap_div:
                    v["capacity"] = cap_div.text.strip().replace("\n", " ")
            
            # Extract features/catering/etc
            features = []
            features_section = soup.find("h2", string="Eigenschappen")
            if features_section:
                feat_div = features_section.find_next("div")
                if feat_div:
                    features = [t.strip() for t in feat_div.text.split(",")]
            v["features"] = features
            
            detailed_vendors.append(v)
        except Exception as e:
            print(f"Error detail {v['url']}: {e}")
        
    with open("vendors_detailed.json", "w") as f:
        json.dump(detailed_vendors, f)

if __name__ == "__main__":
    scrape_vendors()
