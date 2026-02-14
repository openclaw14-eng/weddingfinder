import httpx
import time
import os

TELEGRAM_BOT_TOKEN = "8336455727:AAGpaqOA-yYwlHXlZvJkr6evtAaXvrPuGPU"
SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    try:
        httpx.post(url, json=data)
        print(f"Bericht verstuurd naar {chat_id}")
    except Exception as e:
        print(f"Error sending telegram: {e}")

def listen_for_leads(chat_id):
    headers = {"Authorization": f"Bearer {SUPABASE_KEY}", "apikey": SUPABASE_KEY}
    
    # Houd bij wat de hoogste lead_count is die we hebben gezien
    max_leads_seen = 0
    
    # Initieel bericht
    send_telegram_message(chat_id, "🤖 <b>Rimi Intelligence</b> is nu online.\n\nIk监控 je leads en stuur updates direct door. Zodra iemand op 'Contact' drukt in de app, krijg je hier een seintje! 🚀")

    while True:
        try:
            # Haal alle vendors op met hun lead_count
            r = httpx.get(f"{SUPABASE_URL}/rest/vendors?select=id,name,lead_count", headers=headers)
            vendors = r.json()
            
            current_max = 0
            for v in vendors:
                count = v.get('lead_count', 0) or 0
                if count > current_max:
                    current_max = count
                    
                # Check for new leads (increment > 0 and not yet notified logic simplified here to just max check for demo)
                # In a real robust system we'd check timestamp, but max_leads is a good proxy for "new activity"
            
            if current_max > max_leads_seen:
                new_leads_count = current_max - max_leads_seen
                msg = f"🔔 <b>Nieuwe Lead!</b>\n\nEr zijn {new_leads_count} nieuwe acties geteld in de app.\n\nCheck je dashboard voor details."
                send_telegram_message(chat_id, msg)
                max_leads_seen = current_max
                
        except Exception as e:
            print(f"Error checking leads: {e}")
        
        time.sleep(60) # Check elke minuut

if __name__ == "__main__":
    CHAT_ID = "868619775"
    listen_for_leads(CHAT_ID)