import httpx
import json

def upload_to_supabase():
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

    # Upsert in batches of 100
    for i in range(0, len(vendors), 100):
        batch = vendors[i:i+100]
        print(f"Uploading batch {i//100 + 1}...")
        try:
            res = httpx.post(url, json=batch, headers=headers)
            res.raise_for_status()
            print(f"Batch {i//100 + 1} uploaded successfully.")
        except Exception as e:
            print(f"Error batch {i//100 + 1}: {e}")
            if hasattr(e, 'response'): print(e.response.text)

if __name__ == "__main__":
    upload_to_supabase()
