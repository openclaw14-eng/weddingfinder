import json
import urllib.request
import uuid
import re

url = 'https://gqlprwursgbgkfkwzkyb.supabase.co/rest/v1/vendors'
api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU'

headers = {
    'apikey': api_key,
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

def push_national_set():
    # Deze set bevat de belangrijkste landelijke locaties die we in de batches hadden
    national_venues = [
        {"name": "Kasteel de Hooge Vuursche", "city": "Baarn", "cat": "castle", "desc": "Sprookjesachtig kasteel in de bossen van Baarn."},
        {"name": "Slot Doddendael", "city": "Ewijk", "cat": "castle", "desc": "Middeleeuws slot omringd door boomgaarden."},
        {"name": "Landgoed Te Werve", "city": "Rijswijk", "cat": "castle", "desc": "Monumentaal landgoed op een beschermd natuurpark."},
        {"name": "Buitenplaats Amerongen", "city": "Amerongen", "cat": "castle", "desc": "Historische buitenplaats met prachtige tuinen."},
        {"name": "De Vreemde Vogel", "city": "Vlaardingen", "cat": "farm", "desc": "Unieke buitenlocatie met een eigenzinnige sfeer."},
        {"name": "Orangerie Elswout", "city": "Overveen", "cat": "classic", "desc": "Statige orangerie op een van de mooiste landgoederen."},
        {"name": "SugarCity Events", "city": "Halfweg", "cat": "industrial", "desc": "Rauwe industriële kracht in een oude suikerfabriek."},
        {"name": "Landgoed de Olmenhorst", "city": "Lisserbroek", "cat": "farm", "desc": "Trouwen tussen de appel- en perenbomen."},
        {"name": "Paviljoen Puur", "city": "Diemen", "cat": "classic", "desc": "Design locatie verscholen in een historisch fort op de grens van Amsterdam."}
    ]
    
    to_push = []
    for v in national_venues:
        to_push.append({
            "name": v["name"],
            "slug": re.sub(r'[^a-z0-9]', '-', v["name"].lower()) + "-" + str(uuid.uuid4())[:6],
            "city": v["city"],
            "description": f"{v['cat'].upper()} - {v['desc']}",
            "image_url": "https://images.unsplash.com/photo-1519225495045-1b8823b214e9?q=80&w=1200"
        })
        
    print(f"Expanding coverage with {len(to_push)} national venues...")
    data = json.dumps(to_push).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Status: {response.status}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    push_national_set()
