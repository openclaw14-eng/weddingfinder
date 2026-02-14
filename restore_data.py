import json, httpx, re

SUPABASE_URL = 'https://gqlprwursgbgkfkwzkyb.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU'
headers = {
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'apikey': SUPABASE_KEY,
    'Content-Type': 'application/json'
}

def restore():
    try:
        data = json.load(open('vendors_batch_1.json'))
        clean_data = []
        for v in data:
            if 'Elite' not in v['name']:
                # Ensure slug exists
                name_slug = re.sub(r'[^a-z0-9-]', '', v['name'].lower().replace(' ', '-'))
                v['slug'] = v.get('slug') or name_slug
                # Fix portal_id if missing
                v['portal_id'] = v.get('portal_id') or '9afe381f-b93d-411b-ba81-9cde785f109e'
                # Ensure city is a string
                v['city'] = v.get('city') or 'Nederland'
                clean_data.append(v)
        
        # Prepare upsert headers
        upsert_headers = headers.copy()
        upsert_headers['Prefer'] = 'resolution=merge-duplicates'
        
        # Post in batches
        for i in range(0, len(clean_data), 50):
            batch = clean_data[i:i+50]
            # Use on_conflict parameter if needed, but Prefer: resolution=merge-duplicates is better for Postgres/PostgREST
            # Try UPSERT via POST with on_conflict
            res = httpx.post(f'{SUPABASE_URL}/rest/v1/vendors', json=batch, headers=upsert_headers, params={"on_conflict": "slug"})
            print(f"Batch {i//50 + 1}: {res.status_code}")
            if res.status_code >= 400:
                print(res.text)
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    restore()
