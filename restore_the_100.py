import json
import urllib.request
import uuid
import re

url = 'https://gqlprwursgbgkfkwzkyb.supabase.co/rest/v1/vendors'
api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU'

headers = {
    'apikey': api_key,
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

def restore_originals():
    try:
        with open('vendors.json', 'r') as f:
            original_data = json.load(f)
        
        to_push = []
        for v in original_data:
            name = v.get('name', 'Onbekende Locatie')
            # Categorisatie op basis van de originele data
            desc = (v.get('description', '') + " " + name).lower()
            category = 'classic'
            if any(x in desc for x in ['industrie', 'loods', 'fabriek', 'pomp']): category = 'industrial'
            elif any(x in desc for x in ['kasteel', 'landgoed', 'slot']): category = 'castle'
            elif any(x in desc for x in ['strand', 'beach', 'zee']): category = 'beach'
            elif any(x in desc for x in ['boerderij', 'hoeve', 'schuur']): category = 'farm'
            elif any(x in desc for x in ['hotel', 'overnacht']): category = 'hotel'

            # Bouw het record exact volgens de werkende schema
            record = {
                "name": name,
                "slug": re.sub(r'[^a-z0-9]', '-', name.lower()) + "-" + str(uuid.uuid4())[:6],
                "city": v.get("city", "Amsterdam"),
                "description": f"{category.upper()} - {v.get('description', 'Prachtige trouwlocatie in ' + v.get('city', 'Amsterdam'))}",
                "image_url": v.get("image_url", "https://images.unsplash.com/photo-1519167758481-83f550bb49b3?q=80&w=1200") # Fallback
            }
            to_push.append(record)

        print(f"Restoring {len(to_push)} original locations...")
        # In batches van 50
        for i in range(0, len(to_push), 50):
            batch = to_push[i:i+50]
            data = json.dumps(batch).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers=headers, method='POST')
            with urllib.request.urlopen(req) as response:
                print(f"Batch {i//50 + 1} status: {response.status}")
                
    except Exception as e:
        print(f"Restore failed: {e}")

if __name__ == "__main__":
    restore_originals()
