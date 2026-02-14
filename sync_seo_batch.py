import json
import urllib.request

url = 'https://gqlprwursgbgkfkwzkyb.supabase.co/rest/v1/vendors'
api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU'

headers = {
    'apikey': api_key,
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

def sync_seo_batch():
    try:
        with open('verified_vendors_final_SEO_148.json', 'r') as f:
            seo_data = json.load(f)
        
        for v in seo_data:
            # Match schema exactly: slug, name, city, description, image_url
            record = {
                "name": v["name"],
                "slug": v["slug"],
                "city": v["city"],
                "description": v["description"],
                "image_url": v["image_url"]
            }
            # Add uuid if missing or use existing slug to find/update is complex with REST, 
            # so we post as new or update via slug if Supabase allows
            print(f"Syncing {v['name']}...")
            data = json.dumps([record]).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers=headers, method='POST')
            with urllib.request.urlopen(req) as response:
                print(f"Done: {response.status}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    sync_seo_batch()
