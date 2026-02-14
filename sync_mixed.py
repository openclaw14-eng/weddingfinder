import json
from supabase import create_client, Client

url = "https://gqlprwursgbgkfkwzkyb.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

# Use simple requests if supabase lib is missing or broken
import requests

def push_to_supabase(table, data):
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }
    r = requests.post(f"{url}/rest/v1/{table}", headers=headers, json=data)
    return r.status_code

def sync_all():
    # Load detailed data which contains more types
    try:
        with open('vendors_detailed.json', 'r') as f:
            detailed = json.load(f)
        
        to_sync = []
        for v in detailed:
            # Basic mapping for varied types
            v_name = v.get('name', 'Onbekende Leverancier')
            v_city = v.get('city', 'Nederland')
            
            # Identify type for description mapping
            v_type = v.get('type', '').lower()
            v_desc = v.get('description', f"Hoogwaardige {v_type or 'leverancier'} voor jullie bruiloft.")
            
            if 'photo' in v_name.lower() or 'photo' in v_type:
                v_desc += " Professionele bruidsfotografie."
            if 'video' in v_name.lower() or 'video' in v_type:
                v_desc += " Prachtige trouwvideo's."

            sync_item = {
                "name": v_name,
                "city": v_city,
                "province": v.get('state', 'NL'),
                "image_url": v.get('image_url') or f"https://source.unsplash.com/featured/?wedding,{v_type or 'vendor'}",
                "description": v_desc,
                "website": v.get('url', '#'),
                "capacity": v.get('capacity', 'N/A'),
                "catering": v.get('catering', 'N/A')
            }
            to_sync.append(sync_item)
            
        print(f"Syncing {len(to_sync)} mixed vendors to Supabase...")
        # Batch upload to avoid timeouts
        batch_size = 50
        for i in range(0, len(to_sync), batch_size):
            batch = to_sync[i:i+batch_size]
            status = push_to_supabase('vendors', batch)
            print(f"Batch {i//batch_size + 1} status: {status}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    sync_all()
