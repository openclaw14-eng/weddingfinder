import json
import urllib.request
import uuid

url = 'https://gqlprwursgbgkfkwzkyb.supabase.co/rest/v1/vendors'
api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU'

headers = {
    'apikey': api_key,
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

def add_services():
    # Dit zijn de 'niet-locaties' die we ook in de database hadden (fotografen, etc)
    services = [
        {"name": "Sjoerd Booij Fotografie", "city": "Amsterdam", "type": "Fotograaf", "desc": "Gespecialiseerd in verhalende trouwfotografie."},
        {"name": "Weddingplanner Amsterdam", "city": "Amsterdam", "type": "Planning", "desc": "Voor een zorgeloze organisatie van jullie grote dag."},
        {"name": "The Flower Family", "city": "Amsterdam", "type": "Bloemen", "desc": "Prachtige florale arrangementen en bruidsboeketten."}
    ]
    
    to_push = []
    for s in services:
        to_push.append({
            "name": s["name"],
            "slug": s["name"].lower().replace(" ", "-") + "-" + str(uuid.uuid4())[:4],
            "city": s["city"],
            "description": f"SERVICE - {s['type']}: {s['desc']}",
            "image_url": "https://images.unsplash.com/photo-1519741497674-611481863552?q=80&w=1200"
        })
        
    print(f"Adding {len(to_push)} complementary services...")
    data = json.dumps(to_push).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Status: {response.status}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    add_services()
