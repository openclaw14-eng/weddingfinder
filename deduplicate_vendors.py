import json
import urllib.request

url = 'https://gqlprwursgbgkfkwzkyb.supabase.co/rest/v1/vendors'
api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU'

headers = {
    'apikey': api_key,
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

def deduplicate():
    print("Deduplicating database based on name...")
    try:
        # 1. Fetch all records
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req) as response:
            all_vendors = json.load(response)
        
        # 2. Identify duplicates
        seen_names = {} # name -> id
        to_delete = []
        
        for v in all_vendors:
            name = v['name']
            vid = v['id']
            # If we see the name again, and the current one has a long description (meaning it is SEO enriched), 
            # keep the SEO one and delete the old one.
            if name in seen_names:
                old_id, old_desc_len = seen_names[name]
                new_desc_len = len(v.get('description', ''))
                
                if new_desc_len > old_desc_len:
                    to_delete.append(old_id)
                    seen_names[name] = (vid, new_desc_len)
                else:
                    to_delete.append(vid)
            else:
                seen_names[name] = (vid, len(v.get('description', '')))
        
        print(f"Found {len(to_delete)} duplicates to remove.")
        
        # 3. Exec deletes
        for vid in to_delete:
            del_req = urllib.request.Request(f"{url}?id=eq.{vid}", headers=headers, method='DELETE')
            with urllib.request.urlopen(del_req) as response:
                pass
        
        print("Deduplication complete.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    deduplicate()
