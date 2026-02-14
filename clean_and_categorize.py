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

# The Real Deal: Genuine venues only. 
# Schema adjustment: Name, Slug, City, Description, Image_Url must be strings
verified_gallery = [
    {
        "name": "Huize Frankendael",
        "slug": "huize-frankendael-castle-v8",
        "city": "Amsterdam",
        "description": "INDUSTRIEEL - De laatst overgebleven 17e-eeuwse buitenplaats van Amsterdam. Een oase van historische elegantie met weelderige stijltuinen.",
        "image_url": "https://images.unsplash.com/photo-1560249213-9a4ee1102946?q=80&w=1200"
    },
    {
        "name": "Kasteel de Hooge Vuursche",
        "slug": "hooge-vuursche-baarn-v8",
        "city": "Baarn",
        "description": "KASTEEL - Een sprookjesachtig kasteel omgeven door uitgestrekte bossen in Baarn. Dé locatie voor een klassieke bruiloft.",
        "image_url": "https://images.unsplash.com/photo-1506501139174-099022df5260?q=80&w=1200"
    },
    {
        "name": "Pompstation",
        "slug": "pompstation-amsterdam-v8",
        "city": "Amsterdam",
        "description": "INDUSTRIEEL - Gevestigd in een monumentaal pompstation uit 1912. Een karakteristieke mix van industriële flair.",
        "image_url": "https://images.unsplash.com/photo-1510526024011-755f62c1c24e?q=80&w=1200"
    }
]

def final_push():
    print("Pushing verified real architecture locations...")
    data = json.dumps(verified_gallery).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Verified Push Status: {response.status}")
    except Exception as e:
        if hasattr(e, "read"):
            print(f"Failed Body: {e.read().decode()}")
        print(f"Error: {e}")

if __name__ == "__main__":
    final_push()
