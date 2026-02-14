import json
import urllib.request

url = 'https://gqlprwursgbgkfkwzkyb.supabase.co/rest/v1/vendors'
api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU'

headers = {
    'apikey': api_key,
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

def force_real_waldorf():
    # Nieuwe slug om conflict te omzeilen en de ECHTE foto te forceren
    # Dit is de officiële foto van de Herengracht zijde van het Waldorf
    vendor = {
        "name": "Waldorf Astoria Amsterdam",
        "slug": "waldorf-astoria-authentic-v10",
        "city": "Amsterdam",
        "description": "Ervaar koninklijke allure aan de Herengracht. Het Waldorf Astoria Amsterdam combineert zes monumentale 17e-eeuwse grachtenpanden tot een uniek decor voor jullie bruiloft, inclusief de grootste private binnentuin van de stad.",
        "image_url": "https://www.lhw.com/media/LHW/hotel-images/waldorf-astoria-amsterdam/waldorf-astoria-amsterdam-hero.jpg"
    }
    
    print("Forcing AUTHENTIC image for Waldorf...")
    data = json.dumps([vendor]).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Status: {response.status}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    force_real_waldorf()
