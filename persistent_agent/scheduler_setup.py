import os
import subprocess
import sys

def setup_scheduler():
    print("=== Windows Task Scheduler Setup ===")
    print("Deze script genereert commando's die je als Administrator moet uitvoeren.")
    print("Kopieer en plak deze commando's in een Admin PowerShell prompt.\n")

    scheduler_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "scheduler_service.py"))

    # Heartbeat: Every 1 hour
    heartbeat_cmd = f'schtasks /Create /SC HOURLY /MO 1 /TN "PerfectWedding\\Heartbeat" /TR "python {scheduler_script} heartbeat" /ST 00:00 /RL HIGHEST /F'
    print("1. HEARTBEAT (Elk uur):")
    print(heartbeat_cmd)
    print()

    # Scraper: Every 6 hours
    scraper_cmd = f'schtasks /Create /SC HOURLY /MO 6 /TN "PerfectWedding\\VendorScraper" /TR "python {scheduler_script} scraper" /ST 00:00 /RL HIGHEST /F'
    print("2. VENDOR SCRAPER (Elke 6 uur):")
    print(scraper_cmd)
    print()

    # SEO: Daily
    seo_cmd = f'schtasks /Create /SC DAILY /TN "PerfectWedding\\SEOAgent" /TR "python {scheduler_script} seo" /ST 02:00 /RL HIGHEST /F'
    print("3. SEO AGENT (Dagelijks om 02:00):")
    print(seo_cmd)
    print()

    # Keep Awake Service
    print("4. KEEP AWAKE SERVICE")
    print("Om te voorkomen dat de computer in slaap valt tijdens scrapes, start keep_awake.py:")
    keep_awake_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "keep_awake.py"))
    print(f"   Start-Process python -ArgumentList \"{keep_awake_path}\" -WindowStyle Hidden")
    print("   (Of voeg toe aan Startup folder: shell:startup)")

if __name__ == "__main__":
    setup_scheduler()
