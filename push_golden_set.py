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

def push_golden_set():
    golden_set = [
        {
            "name": "Huize Frankendael",
            "slug": "huize-frankendael-premium",
            "city": "Amsterdam",
            "description": "De laatst overgebleven 17e-eeuwse buitenplaats van Amsterdam. Een oase van historische elegantie met weelderige stijltuinen, perfect voor een romantische huwelijksceremonie en een diner op topniveau door Restaurant Merkelbach.",
            "image_url": "https://huizefrankendael.nl/wp-content/uploads/2021/05/huize-frankendael-trouwen.jpg",
            "website": "https://huizefrankendael.nl"
        },
        {
            "name": "Hotel The Dylan",
            "slug": "the-dylan-amsterdam-premium",
            "city": "Amsterdam",
            "description": "Verscholen aan de Keizersgracht biedt The Dylan een intieme setting voor een exclusieve bruiloft. De prachtige binnentuin en de culinaire perfectie van Michelin-restaurant Vinkeles maken elke huwelijksdag hier onvergetelijk.",
            "image_url": "https://www.dylanamsterdam.com/wp-content/uploads/2019/02/The-Dylan-Amsterdam-Garden.jpg",
            "website": "https://www.dylanamsterdam.com"
        },
        {
            "name": "Waldorf Astoria Amsterdam",
            "slug": "waldorf-astoria-premium",
            "city": "Amsterdam",
            "description": "Zes monumentale grachtenpanden vormen het decor van Waldorf Astoria Amsterdam. Met de grootste private binnentuin van de stad en een koninklijke uitstraling aan de Herengracht is dit de ultieme locatie voor een luxe droombruiloft.",
            "image_url": "https://www.hilton.com/im/en/AMSWAAA/14299946/exterior-boat.jpg",
            "website": "https://www.hilton.com/en/hotels/amswawa-waldorf-astoria-amsterdam/"
        },
        {
            "name": "The Grand (Sofitel Legend)",
            "slug": "the-grand-amsterdam-premium",
            "city": "Amsterdam",
            "description": "Historische pracht en legendarische service in het hart van Amsterdam. De monumentale Raadzaal, waar Prinses Beatrix trouwde, biedt een ongeëvenaard statig decor voor jullie ja-woord.",
            "image_url": "https://www.sofitel-legend-thegrand.com/media/hotel-images/the-grand-exterior.jpg",
            "website": "https://www.sofitel-legend-thegrand.com"
        },
        {
            "name": "Conservatorium Hotel",
            "slug": "conservatorium-hotel-premium",
            "city": "Amsterdam",
            "description": "Moderne architectuur ontmoet historisch erfgoed in het Museumkwartier. Een iconische locatie met een kosmopolitische sfeer, perfect voor wie houdt van eigentijdse luxe en verfijnd design.",
            "image_url": "https://www.conservatoriumhotel.com/media/images/conservatorium-hotel-exterior.jpg",
            "website": "https://www.conservatoriumhotel.com"
        }
    ]
    
    print("Pushing verified Golden Set to database...")
    data = json.dumps(golden_set).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Sync Status: {response.status}")
    except Exception as e:
        if hasattr(e, 'read'):
            print(f"Failed: {e.read().decode()}")
        else:
            print(f"Failed: {e}")

if __name__ == "__main__":
    push_golden_set()
