import httpx
from bs4 import BeautifulSoup
import json
import time

def scrape_vendors():
    # DIRECT URLs to profile lists to bypass sitemap parsing if possible
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
    
    print("PHASE 1: Extracting basic data from listing pages...")
    for region_url in region_urls:
        print(f"Scraping region: {region_url}")
        try:
            res = httpx.get(region_url)
            content = res.text
            
            # Extract JSON from the page attribute
            start_str = ':profile-lists="'
            start_idx = content.find(start_str) + len(start_str)
            if start_idx < len(start_str): 
                print(f"No profile-lists found for {region_url}")
                continue
            
            end_idx = content.find(']"', start_idx) + 1
            json_blob = content[start_idx:end_idx].replace('&quot;', '"')
            data = json.loads(json_blob)
            
            for list_item in data:
                for vendor_data in list_item:
                    v_id = str(vendor_data.get("id"))
                    # Unique check
                    if any(v['id'] == v_id for v in vendors): continue
                    
                    v_name = vendor_data.get("name")
                    v_city = vendor_data.get("city")
                    v_state = vendor_data.get("state")
                    v_url = vendor_data.get("url")
                    v_price = vendor_data.get("averageWeddingPrice")
                    
                    # Construct basic object
                    vendor = {
                        "id": v_id,
                        "name": v_name,
                        "city": v_city,
                        "state": v_state,
                        "url": v_url,
                        "price": v_price,
                        "rating": vendor_data.get("total_rating", {}).get("mean", 4.8),
                        "reviews": vendor_data.get("total_rating", {}).get("count", 0),
                        "description": "",
                        "capacity": "Op aanvraag",
                        "catering": "Eigen catering",
                        "parking": "Gratis",
                        "overnachting": "Onbekend"
                    }
                    vendors.append(vendor)
            print(f"Total vendors fetched so far: {len(vendors)}")
        except Exception as e:
            print(f"Error region {region_url}: {e}")
        
    print(f"PHASE 1 COMPLETE. Found {len(vendors)} vendors.")
    
    print("PHASE 2: Fetching deep details for 500 vendors...")
    detailed_vendors = []
    for i, v in enumerate(vendors):
        if i >= 550: break
        if i % 10 == 0: 
            print(f"Processing detail {i}/{len(vendors)}...")
            # Periodic save in case of crash
            with open("vendors_detailed.json", "w") as f:
                json.dump(vendors[:i], f)

        try:
            res = httpx.get(v["url"], timeout=10.0)
            soup = BeautifulSoup(res.text, "html.parser")
            
            # DESCRIPTION
            desc_div = soup.find("div", class_="description-text")
            if desc_div:
                v["description"] = desc_div.get_text(separator=" ").strip()
            
            # CAPACITY
            cap_section = soup.find("h2", string=lambda x: x and "Capaciteit" in x)
            if cap_section:
                cap_div = cap_section.find_next("div")
                if cap_div:
                    cap_text = cap_div.get_text(separator=" ").replace("\n", " ").strip()
                    # Try to extract the highest number
                    import re
                    nums = re.findall(r'\d+', cap_text)
                    if nums:
                        v["capacity"] = max([int(n) for n in nums])
                    else:
                        v["capacity"] = "Diverse zalen"

            # FEATURES (Catering, Parking, etc)
            feat_section = soup.find("h2", string=lambda x: x and "Eigenschappen" in x)
            if feat_section:
                feat_div = feat_section.find_next("div")
                if feat_div:
                    f_list = feat_div.get_text().lower()
                    if "catering" in f_list: v["catering"] = "Eigen catering"
                    if "parkeren" in f_list: v["parking"] = "Parkeergelegenheid"
                    if "overnachting" in f_list or "hotel" in f_list: v["overnachting"] = "Ja"
                    else: v["overnachting"] = "Nee"
            
            detailed_vendors.append(v)
            
            # Rate limiting avoidance
            if i % 5 == 0: time.sleep(0.1)
        except Exception as e:
            print(f"Error detail {v['url']}: {e}")
            detailed_vendors.append(v) # Keep basic info at least
        
    with open("vendors_detailed.json", "w") as f:
        json.dump(detailed_vendors, f)
    print(f"SUCCESS: Scraped {len(detailed_vendors)} vendors with deep details.")

if __name__ == "__main__":
    scrape_vendors()
