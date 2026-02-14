import http.server
import socketserver
import json
import threading
import time
import httpx
import os
from datetime import datetime

# CONFIG
SUPABASE_URL = "https://gqlprwursgbgkfkwzkyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU"
PORT = 3005

state = {
    "vendors": 0,
    "leads": 0,
    "seo_coverage": "0%",
    "active_agents": ["Scraper", "SEO Optimizer"],
    "last_update": "",
    "revenue_est": "€0.00",
    "status": "Thinking...",
    "scraper_status": "Active",
    "scraper_progress": 0
}

def update_state():
    headers = {"Authorization": f"Bearer {SUPABASE_KEY}", "apikey": SUPABASE_KEY}
    while True:
        try:
            # Check scraper progress
            if os.path.exists("scraper_progress.json"):
                with open("scraper_progress.json", "r") as f:
                    progress_data = json.load(f)
                    state["scraper_status"] = progress_data.get("message", "Standby")
                    state["scraper_progress"] = progress_data.get("progress", 0)

            # Get vendor count
            r = httpx.get(f"{SUPABASE_URL}/rest/v1/vendors?select=count", headers=headers)
            state["vendors"] = r.headers.get("Content-Range", "0-0/0").split("/")[-1]
            
            # Get lead count
            r = httpx.get(f"{SUPABASE_URL}/rest/v1/vendors?select=lead_count.sum()", headers=headers)
            try:
                val = r.json()[0].get('sum', 0)
                state["leads"] = val if val is not None else 0
            except: state["leads"] = 0
            
            state["revenue_est"] = f"€{int(state['leads']) * 2}.00"
            
            # SEO Coverage
            r = httpx.get(f"{SUPABASE_URL}/rest/v1/vendors?seo_title=not.is.null&select=count", headers=headers)
            optimized = int(r.headers.get("Content-Range", "0-0/0").split("/")[-1])
            if int(state["vendors"]) > 0:
                state["seo_coverage"] = f"{int((optimized / int(state['vendors'])) * 100)}%"
            
            state["last_update"] = datetime.now().strftime("%H:%M:%S")
            state["status"] = "Active"
        except Exception as e:
            state["status"] = f"Error: {str(e)}"
        
        time.sleep(5)

class DashboardHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(state).encode())
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            try:
                with open('KANBAN.html', 'r') as f:
                    html = f.read()
                    polling_script = """
                    <script>
                        async function update() {
                            try {
                                const res = await fetch('/api/status');
                                const data = await res.json();
                                document.getElementById('dashboard-title').innerText = 'Rimi OS - Live';
                                document.getElementById('update-time').innerText = 'Laatste update: ' + data.last_update;
                                document.getElementById('stat-vendors').innerText = data.vendors;
                                document.getElementById('stat-leads').innerText = data.revenue_est;
                                document.getElementById('stat-seo').innerText = data.seo_coverage;
                                document.getElementById('scraper-msg').innerText = data.scraper_status;
                                document.getElementById('scraper-bar').style.width = data.scraper_progress + '%';
                            } catch (e) { console.error('Dashboard error:', e); }
                        }
                        setInterval(update, 3000);
                        update();
                    </script>
                    """
                    self.wfile.write(html.replace('</body>', polling_script + '</body>').encode())
            except Exception as e:
                self.wfile.write(f"Error loading KANBAN.html: {str(e)}".encode())

def run_server():
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f"Rimi Dashboard live op port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=update_state, daemon=True).start()
    run_server()
