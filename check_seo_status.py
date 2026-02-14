import httpx
import json

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
}

def check_vendors_for_seo():
    # Attempt to fetch vendors where seo_update_pending is true (if column exists)
    # If it doesn't exist, we might need to check which columns are available
    # For now, let's just get the first 50 vendors to see the schema
    response = httpx.get(
        f"{SUPABASE_URL}/rest/v1/vendors?select=*&limit=5",
        headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        print("Schema/Samples:")
        if data:
            print(json.dumps(data[0], indent=2))
        else:
            print("No data found in vendors table.")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    check_vendors_for_seo()
