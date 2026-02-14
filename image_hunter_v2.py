import json
import urllib.request
import urllib.parse
import re

def get_direct_images(query):
    # Search for the venue on DuckDuckGo images or similar accessible via search
    # We use Google Search API via web_search tool in the agent, 
    # but here we define the protocol for the scraper.
    print(f"Searching direct high-res images for: {query}")
    return []

# New instructions for the Scraper-Agent
new_instruction = """
PROTOCOL 'IMAGE-HUNTER V2':
1. Gebruik Google Search (via web_search) met de query: "[Vendor Name] [City] high resolution wedding photography".
2. Zoek specifiek naar directe image URLs van:
   - De officiële website van de locatie.
   - Grote trouwplatforms (ThePerfectWedding, TopTrouwlocaties) die de officiële foto's hosten.
3. Vermijd Pinterest/Instagram links (deze 'breken' vaak).
4. Sla de directe URL op die eindigt op .jpg of .png en minimaal 1000px breed is.
5. Als geen directe URL gevonden wordt op de eigen site, gebruik dan de Unsplash Wedding API als backup.
"""

print(new_instruction)
