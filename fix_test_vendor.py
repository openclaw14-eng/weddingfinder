import json
import urllib.request

url = 'https://gqlprwursgbgkfkwzkyb.supabase.co/rest/v1/vendors'
api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU'

headers = {
    'apikey': api_key,
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

def fix_with_new_slug():
    # Using a totally fresh slug to bypass the conflict and test the image
    vendor = {
        "name": "Waldorf Astoria Amsterdam",
        "slug": "waldorf-astoria-final-verified-786",
        "city": "Amsterdam",
        "description": "Exclusieve luxe aan de Amsterdamse grachten. Waldorf Astoria Amsterdam biedt een koninklijk decor voor een onvergetelijke bruiloft met de grootste private binnentuin van de stad.",
        "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?q=80&w=1200&auto=format&fit=crop"
    }
    
    print("Pushing new clean Waldorf record...")
    data = json.dumps([vendor]).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Push Status: {response.status}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    fix_with_new_slug()
