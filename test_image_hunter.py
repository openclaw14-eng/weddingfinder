import json
import urllib.request

url = 'https://gqlprwursgbgkfkwzkyb.supabase.co/rest/v1/vendors'
api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU'

headers = {
    'apikey': api_key,
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

def push_test_minimal():
    # Only fields we know for SURE work (from previous Batch 1-8 successes)
    vendor = {
        "name": "Waldorf Astoria Amsterdam (TEST DE LUXE)",
        "slug": "waldorf-astoria-test-final-v9",
        "city": "Amsterdam",
        "description": "Beleef de ultieme definitie van luxe en tijdloze klasse bij het Waldorf Astoria Amsterdam. Deze SEO tekst is uniek geschreven.",
        "image_url": "https://www.historichotels.org/images/hotels/Waldorf_Astoria_Amsterdam/Waldorf_Astoria_Amsterdam_Exterior_Boat.jpg"
    }
    
    data = json.dumps([vendor]).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Test Push Status: {response.status}")
    except urllib.error.HTTPError as e:
        print(f"Failed Body: {e.read().decode()}")

if __name__ == "__main__":
    push_test_minimal()
