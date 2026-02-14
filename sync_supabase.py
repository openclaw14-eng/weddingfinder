import json
from supabase import create_client, Client

url = "https://gqlprwursgbgkfkwzkyb.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

supabase: Client = create_client(url, key)

def sync_venues():
    try:
        with open('scraped_venues.json', 'r') as f:
            data = json.load(f)
            venues = data.get('venues', [])
            
        print(f"Syncing {len(venues)} venues...")
        
        for venue in venues:
            # Prepare data for Supabase 'vendors' table
            # Adjusting keys to match expected DB schema if necessary
            vendor_data = {
                "name": venue.get('name'),
                "city": venue.get('city'),
                "province": venue.get('state'),
                "image_url": venue.get('image_url') or f"https://source.unsplash.com/featured/?wedding,{venue.get('name').replace(' ', '')}",
                "description": f"Prachtige trouwlocatie in {venue.get('city')}. Rating: {venue.get('rating')}.",
                "website": venue.get('url'),
                "capacity": "Op aanvraag",
                "catering": "Beschikbaar"
            }
            
            # Upsert based on name + city to avoid duplicates
            result = supabase.table('vendors').upsert(vendor_data, on_conflict='name,city').execute()
            print(f"Synced: {venue.get('name')}")
            
        print("Sync complete.")
    except Exception as e:
        print(f"Error during sync: {e}")

if __name__ == "__main__":
    sync_venues()
