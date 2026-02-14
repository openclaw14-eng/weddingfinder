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

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]', '-', text)
    return re.sub(r'-+', '-', text).strip('-')

def upload_clean():
    with open('final_clean_vendors.json', 'r') as f:
        raw_data = json.load(f)
    
    clean_data = []
    for v in raw_data:
        name = v.get("name")
        # Removing capacity/catering/is_active to match minimal schema
        record = {
            "name": name,
            "slug": slugify(name) + "-" + str(uuid.uuid4())[:12],
            "city": v.get("city", "Amsterdam"),
            "description": v.get("description", f"Prachtige trouwlocatie: {name}"),
            "image_url": v.get("image_url", "")
        }
        clean_data.append(record)

    print(f"Uploading {len(clean_data)} verified records with compatible schema...")
    for i in range(0, len(clean_data), 20):
        batch = clean_data[i:i+20]
        data = json.dumps(batch).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        try:
            with urllib.request.urlopen(req) as response:
                print(f"Batch {i//20 + 1} status: {response.status}")
        except urllib.error.HTTPError as e:
            print(f"Batch {i//20 + 1} failed: {e.read().decode()}")

if __name__ == "__main__":
    upload_clean()
