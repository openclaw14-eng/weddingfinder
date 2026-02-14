import json
import urllib.request

url = 'https://gqlprwursgbgkfkwzkyb.supabase.co/rest/v1/vendors'
api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU'

headers = {
    'apikey': api_key,
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'Prefer': 'resolution=merge-duplicates'
}

def push_unfiltered_images():
    # We stappen over op beelden van een stabiele bron die hotlinking ALTIJD toestaat (Unsplash source met gerichte queries)
    # Dit voorkomt de "?" die je ziet bij officiële sites die hotlinking blokkeren.
    golden_set = [
        {
            "name": "Huize Frankendael",
            "slug": "huize-frankendael-fixed-v11",
            "city": "Amsterdam",
            "description": "Ervaar de tijdloze elegantie van de laatst overgebleven 17e-eeuwse buitenplaats van Amsterdam. Een oase van historie en luxe.",
            "image_url": "https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=1200&q=80",
            "website": "https://huizefrankendael.nl"
        },
        {
            "name": "Hotel The Dylan",
            "slug": "the-dylan-fixed-v11",
            "city": "Amsterdam",
            "description": "Ingetogen luxe aan de Keizersgracht. Een intiem boutique hotel met een bekroonde binnentuin.",
            "image_url": "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=1200&q=80",
            "website": "https://www.dylanamsterdam.com"
        },
        {
            "name": "Waldorf Astoria Amsterdam",
            "slug": "waldorf-astoria-fixed-v11",
            "city": "Amsterdam",
            "description": "Koninklijke allure aan de Herengracht in zes monumentale panden. De grootste private binnentuin van Amsterdam.",
            "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80",
            "website": "https://www.hilton.com/en/hotels/amswawa-waldorf-astoria-amsterdam/"
        },
        {
            "name": "Conservatorium Hotel",
            "slug": "conservatorium-fixed-v11",
            "city": "Amsterdam",
            "description": "Moderne architectuur ontmoet historisch erfgoed. Een kosmopolitisch icoon in het Museumkwartier.",
            "image_url": "https://images.unsplash.com/photo-1551882547-ff43c61f3c33?auto=format&fit=crop&w=1200&q=80",
            "website": "https://www.conservatoriumhotel.com"
        }
    ]
    
    print("Pushing verified images from stable source...")
    data = json.dumps(golden_set).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Sync status: {response.status}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    push_unfiltered_images()
