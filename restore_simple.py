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
        for v in data:
            if 'Elite' in v['name']: continue
            
            # Clean data
            name_slug = re.sub(r'[^a-z0-9-]', '', v['name'].lower().replace(' ', '-'))
            v['slug'] = v.get('slug') or name_slug
            v['portal_id'] = v.get('portal_id') or '9afe381f-b93d-411b-ba81-9cde785f109e'
            
            # Try to insert. If fails (likely duplicate), we skip since it's already there or a conflict.
            # We don't want to break the whole loop.
            try:
                # Use a single insert to be safe with existing data
                httpx.post(f'{SUPABASE_URL}/rest/v1/vendors', json=v, headers=headers)
            except:
                pass
        print("Restoration process finished.")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    restore()
