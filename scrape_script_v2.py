import httpx
from bs4 import BeautifulSoup
import json
import time

def scrape_vendors():
    # 1. Get region URLs from regions map directly
    region_urls = [
        "https://www.theperfectwedding.nl/trouw-feestlocaties/in/amsterdam",
        "https://www.theperfectwedding.nl/trouw-feestlocaties/in/rotterdam",
        "https://www.theperfectwedding.nl/trouw-feestlocaties/in/utrecht",
        "https://www.theperfectwedding.nl/trouw-feestlocaties/in/den-haag",
        "https://www.theperfectwedding.nl/trouw-feestlocaties/in/eindhoven",
        "https://www.theperfectwedding.nl/trouw-feestlocaties/in/groningen",
        "https://www.theperfectwedding.nl/trouw-feestlocaties/in/breda",
        "https://www.theperfectwedding.nl/trouw-feestlocaties/in/haarlem"
    ]
    
    vendors = []
    
    for region_url in region_urls:
        print(f"Scraping region: {region_url}")
        try:
            res = httpx.get(region_url)
            content = res.text
            
            # Extract JSON from the page
            start_str = ':profile-lists="'
            start_idx = content.find(start_str) + len(start_str)
            if start_idx < len(start_str): continue
            
            end_idx = content.find(']"', start_idx) + 1
            json_blob = content[start_idx:end_idx].replace('&quot;', '"')
            data = json.loads(json_blob)
            
            for list_item in data:
                for vendor_data in list_item:
                    v_id = str(vendor_data.get("id"))
                    # Filter unique
                    if any(v['id'] == v_id for v in vendors): continue
                    
                    vendor = {
                        "id": v_id,
                        "name": vendor_data.get("name"),
                        "city": vendor_data.get("city"),
                        "state": vendor_data.get("state"),
                        "url": vendor_data.get("url"),
                        "price": vendor_data.get("averageWeddingPrice"),
                        "rating": vendor_data.get("total_rating", {}).get("mean"),
                        "reviews": vendor_data.get("total_rating", {}).get("count"),
                    }
                    vendors.append(vendor)
            print(f"Total vendors so far: {len(vendors)}")
        except Exception as e:
            print(f"Error parsing region {region_url}: {e}")
        
        if len(vendors) >= 700:
            break
        time.sleep(0.5)

    print(f"Found {len(vendors)} unique vendors. Fetching deep details...")
    
    detailed_vendors = []
    for i, v in enumerate(vendors):
        if i >= 600: break
        if i % 20 == 0: print(f"Processing detail {i}/{len(vendors)}...")
        try:
            res = httpx.get(v["url"], timeout=10.0)
            soup = BeautifulSoup(res.text, "html.parser")
            
            # DESCRIPTION
            desc_div = soup.find("div", class_="description-text")
            v["description"] = desc_div.get_text(separator=" ").strip() if desc_div else ""
            
            # CAPACITY Section
            v["capacity_details"] = {}
            cap_section = soup.find("h2", string="Capaciteit")
            if cap_section:
                cap_container = cap_section.find_next("div")
                if cap_container:
                    # Look for labels like "Ceremonie:", "Receptie:", etc.
                    items = cap_container.find_all("div")
                    current_label = None
                    for item in items:
                        text = item.get_text().strip()
                        if text.endswith(":"):
                            current_label = text[:-1]
                        elif current_label:
                            v["capacity_details"][current_label] = text
                            current_label = None

            # FEATURES & CATERING
            features = []
            feat_section = soup.find("h2", string="Eigenschappen")
            if feat_section:
                feat_div = feat_section.find_next("div")
                if feat_div:
                    features = [t.strip() for t in feat_div.text.split(",")]
            v["features"] = features
            
            # Specific flags
            v["catering"] = "Eigen catering" if any("catering" in f.lower() for f in features) else "Externe catering mogelijk"
            v["parking"] = "Gratis parkeren" if any("parkeren" in f.lower() for f in features) else "Betaald/Openbaar"
            v["overnachting"] = "Ja" if any(x in str(v["features"]).lower() or x in v["description"].lower() for x in ["overnachting", "hotel", "slapen", "kamers"]) else "Nee"
            
            # Unified capacity string for UI
            v["capacity"] = v["capacity_details"].get("Feest", v["capacity_details"].get("Receptie", "Onbekend"))
            
            detailed_vendors.append(v)
        except Exception as e:
            print(f"Error detail {v['url']}: {e}")
        
    with open("vendors_detailed.json", "w") as f:
        json.dump(detailed_vendors, f)
    print("Done! vendors_detailed.json saved.")

if __name__ == "__main__":
    scrape_vendors()
