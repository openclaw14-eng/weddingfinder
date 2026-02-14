import httpx
import json

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
}

def fetch_batch_vendors():
    # Since we don't have a 'seo_update_pending' column yet, 
    # let's fetch vendors that have a description but lack an 'official_website' if that column exists,
    # or just fetch the first 50 to process.
    # Actually, the user says "Fetch vendors where SEO update is pending".
    # Let's check if there are columns like 'seo_optimized' or similar.
    # From previous output, I see 'seo_description' and 'seo_title' are null.
    
    # Query for vendors where seo_description is null
    response = httpx.get(
        f"{SUPABASE_URL}/rest/v1/vendors?select=id,name,city,description,website,image_url,seo_title,seo_description&seo_description=is.null&limit=50",
        headers=headers
    )
    if response.status_code == 200:
        vendors = response.json()
        print(f"Found {len(vendors)} vendors needing SEO overhaul.")
        with open("vendors_batch_1.json", "w", encoding="utf-8") as f:
            json.dump(vendors, f, indent=2)
    else:
        print(f"Error fetching vendors: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    fetch_batch_vendors()
