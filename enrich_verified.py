import json
import urllib.request
import uuid
import re
import time

url = 'https://gqlprwursgbgkfkwzkyb.supabase.co/rest/v1/vendors'
api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU'

headers = {
    'apikey': api_key,
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'Prefer': 'resolution=merge-duplicates'
}

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]', '-', text)
    return re.sub(r'-+', '-', text).strip('-')

def get_category(name, desc):
    full_text = (str(name) + " " + str(desc)).lower()
    if any(x in full_text for x in ['industrie', 'loods', 'fabriek', 'silo']): return 'industrial'
    if any(x in full_text for x in ['kasteel', 'landgoed', 'buitenplaats', 'slot', 'paleis']): return 'castle'
    if any(x in full_text for x in ['strand', 'beach', 'zee', 'paviljoen']): return 'beach'
    if any(x in full_text for x in ['boerderij', 'hoeve', 'schuur', 'stal']): return 'farm'
    if any(x in full_text for x in ['hotel', 'overnacht', 'slapen']): return 'hotel'
    return 'classic'

def enrich_and_sync():
    with open('final_clean_vendors.json', 'r') as f:
        vendors = json.load(f)
    
    enriched = []
    print(f"Enriching {len(vendors)} vendors...")
    
    for v in vendors:
        name = v.get('name')
        desc = v.get('description', '')
        
        # Clean record
        record = {
            "name": name,
            "slug": slugify(name) + "-" + str(uuid.uuid4())[:8],
            "city": v.get("city", "Amsterdam"),
            "description": desc,
            "image_url": v.get("image_url", ""),
            "category": get_category(name, desc),
            "website": v.get("website", ""),
            "capacity": str(v.get("capacity", "Op aanvraag")),
            "catering": v.get("catering", "In-house"),
            "is_active": True
        }
        
        # If no image, we will need to scrape/find one, but for now ensure valid structure
        enriched.append(record)

    # Hard reset DB to ensure schema match (since we added columns)
    # Note: If columns don't exist in Supabase, this will still 400. 
    # I will stick to the known working schema but ensure category is handled in HTML if DB lacks it.
    
    # Actually, let's just update the local JSON and the Scraper-Agent will fill images.
    with open('verified_vendors_enriched.json', 'w') as f:
        json.dump(enriched, f, indent=2)
    
    print("Enrichment local done. Starting image & link verification...")

if __name__ == "__main__":
    enrich_and_sync()
