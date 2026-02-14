import httpx
import json
import uuid

def upload_to_supabase_v2():
    url = "https://gqlprwursgbgkfkwzkyb.supabase.co/rest/v1/vendors"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"
    
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    with open("vendors_detailed.json", "r") as f:
        vendors = json.load(f)

    import random
    processed = []
    for v in vendors:
        # Standardize for existing schema
        processed.append({
            "name": v['name'],
            "city": v['city'],
            "description": f"{v['description']} | Capaciteit: {v['capacity']} | Catering: {v['catering']} | Parkeren: {v['parking']} | Slaapplekken: {v['overnachting']}",
            "is_premium": random.choice([True, False, False, False]),
            "slug": f"{v['name'].lower().replace(' ', '-')}-{v['id']}",
            "theperfectwedding_url": v['url']
        })

    # Upsert in batches of 50 for safety
    for i in range(0, len(processed), 50):
        batch = processed[i:i+50]
        print(f"Uploading batch {i//50 + 1}...")
        try:
            res = httpx.post(url, json=batch, headers=headers)
            res.raise_for_status()
            print(f"Batch {i//50 + 1} uploaded.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    upload_to_supabase_v2()
