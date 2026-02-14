import json
import requests

url = "https://gqlprwursgbgkfkwzkyb.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

def push_to_supabase(table, data):
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }
    r = requests.post(f"{url}/rest/v1/{table}", headers=headers, json=data)
    if r.status_code >= 400:
        print(f"Error {r.status_code}: {r.text}")
    return r.status_code

def sync_all():
    try:
        with open('vendors_detailed.json', 'r') as f:
            detailed = json.load(f)
        
        to_sync = []
        for v in detailed:
            # Minimalist mapping: name, city, image_url, description, website
            sync_item = {
                "name": v.get('name', 'Onbekende Leverancier'),
                "city": v.get('city', 'Nederland'),
                "image_url": v.get('image_url') or "https://images.unsplash.com/photo-1519167758481-83f550bb49b3",
                "description": v.get('description', 'Hoogwaardige leverancier voor jullie bruiloft.'),
                "website": v.get('url', '#')
            }
            to_sync.append(sync_item)
            
        print(f"Syncing {len(to_sync)} items...")
        batch_size = 50
        for i in range(0, len(to_sync), batch_size):
            batch = to_sync[i:i+batch_size]
            status = push_to_supabase('vendors', batch)
            print(f"Batch {i//batch_size + 1} status: {status}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    sync_all()
