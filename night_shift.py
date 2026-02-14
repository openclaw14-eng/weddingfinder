import httpx
import time
import json
import os

SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

headers = {
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "apikey": SUPABASE_KEY,
    "Content-Type": "application/json"
}

def generate_outreach_emails():
    """Identificeert vendors zonder outreach en maakt een draft."""
    # We voegen een kolom toe voor outreach status als die er niet is
    url = f"{SUPABASE_URL}/rest/v1/vendors?outreach_status=is.null&limit=5"
    res = httpx.get(url, headers=headers)
    vendors = res.json()
    
    for v in vendors:
        name = v['name']
        email_body = f"""
        Beste team van {name},
        
        Ik heb zojuist jullie profiel bekeken op ons nieuwe platform 'The Perfect Wedding'. 
        Jullie werk ziet er fantastisch uit en past precies bij onze doelgroep.
        
        We hebben momenteel een actie waarbij jullie de eerste 3 maanden gratis een 
        PREMIUM vermelding krijgen incl. lead-doorsturing.
        
        Zullen we een korte call inplannen om de details te bespreken?
        
        Met vriendelijke groet,
        Rimi (AI Assistant van Ricky)
        """
        
        # Update status in DB
        update_url = f"{SUPABASE_URL}/rest/v1/vendors?id=eq.{v['id']}"
        httpx.patch(update_url, json={"outreach_status": "draft_ready"}, headers=headers)
        
        # Sla draft lokaal op voor Ricky om te checken
        with open(f"outreach_drafts/{v['slug']}.txt", "w", encoding="utf-8") as f:
            f.write(email_body)
        print(f"Outreach draft gemaakt voor {name}")

def automate_marketing():
    """Genereert content voor social media/blog op basis van database."""
    url = f"{SUPABASE_URL}/rest/v1/vendors?limit=1"
    res = httpx.get(url, headers=headers)
    v = res.json()[0]
    
    post = f"Nieuw op ons platform: {v['name']}! Op zoek naar de perfecte trouwdag? Check onze app voor de beste deals in {v.get('city', 'Nederland')}."
    
    with open("marketing_queue.log", "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M')}] SOCIAL POST: {post}\n")
    print("Marketing post gegenereerd.")

def night_shift():
    if not os.path.exists("outreach_drafts"): os.makedirs("outreach_drafts")
    
    print("NIGHT SHIFT GESTART. Slaap lekker Ricky, ik neem het over.")
    while True:
        try:
            print(f"[{time.strftime('%H:%M:%S')}] Draaien van autonome taken...")
            
            # 1. SEO optimalisatie voor nieuwe entries
            os.system("python seo_agent.py")
            
            # 2. Outreach voorbereiden
            generate_outreach_emails()
            
            # 3. Marketing content plannen
            automate_marketing()
            
            # Wacht 15 minuten voor de volgende ronde
            time.sleep(900) 
        except Exception as e:
            print(f"Error in Night Shift: {e}")
            time.sleep(60)

if __name__ == "__main__":
    night_shift()
