import json
import urllib.request
import ssl

# Create SSL context that doesn't verify certificates (for simplicity)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Fetch the API data
url = "https://www.theperfectwedding.nl/api/profiles/trouw-feestlocaties"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ssl_context) as response:
    data = json.loads(response.read().decode('utf-8'))

# Extract first 20 venues
venues = []
for profile in data.get("profiles", [])[:20]:
    venue = {
        "id": profile.get("id"),
        "name": profile.get("name"),
        "city": profile.get("city"),
        "state": profile.get("state"),
        "zipcode": profile.get("zipcode"),
        "country": profile.get("country"),
        "averageWeddingPrice": profile.get("averageWeddingPrice"),
        "rating": profile.get("total_rating", {}).get("mean"),
        "ratingCount": profile.get("total_rating", {}).get("count"),
        "url": profile.get("url"),
        "slug": profile.get("slug"),
        "location": profile.get("location")
    }
    venues.append(venue)

# Save to JSON file
output_file = r"C:\Users\eami\.openclaw\workspace\scraped_venues.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump({
        "total_scraped": len(venues),
        "venues": venues
    }, f, indent=2, ensure_ascii=False)

print(f"Scraped {len(venues)} venues successfully!")
for i, v in enumerate(venues, 1):
    print(f"{i}. {v['name']} - {v['city']}, {v['state']}")
