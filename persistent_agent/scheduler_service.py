import sys
import os
import time
import subprocess

# Add root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from persistent_agent.checkpoint_system import save_checkpoint, get_last_run

# Import agent functions (assuming they can be imported or run via subprocess)
# For simplicity in this environment, we might run them as subprocess or refactor them to be importable.
# Since the prompt implies "Build a persistent agent system", wrapping them is good practice.

def run_heartbeat():
    print("Running Heartbeat...")
    try:
        # Ideally import and run heartbeat_monitor.py logic
        # For now, just updating the log
        with open("HEARTBEAT.log", "a") as f:
            f.write(f"Heartbeat: {time.ctime()}\n")
        save_checkpoint("heartbeat", "COMPLETED")
        return True
    except Exception as e:
        save_checkpoint("heartbeat", "FAILED", {"error": str(e)})
        return False

def run_scraper():
    print("Running Scraper...")
    try:
        # We need to handle the offset/resume logic here if scraper_supabase.py supports it.
        # If not, we should wrap it.
        # Checking checkpoint for resume
        checkpoint = get_last_run("scraper")
        # logic to resume...
        
        # Run the script
        subprocess.run([sys.executable, "scraper_supabase.py"], check=True)
        save_checkpoint("scraper", "COMPLETED")
        return True
    except Exception as e:
        save_checkpoint("scraper", "FAILED", {"error": str(e)})
        return False

def run_seo():
    print("Running SEO Agent...")
    try:
        subprocess.run([sys.executable, "seo_agent.py"], check=True)
        save_checkpoint("seo_agent", "COMPLETED")
        return True
    except Exception as e:
        save_checkpoint("seo_agent", "FAILED", {"error": str(e)})
        return False

if __name__ == "__main__":
    # Simple command dispatcher
    if len(sys.argv) < 2:
        print("Usage: python scheduler_service.py [heartbeat|scraper|seo]")
        sys.exit(1)
    
    mode = sys.argv[1]
    
    if mode == "heartbeat":
        run_heartbeat()
    elif mode == "scraper":
        run_scraper()
    elif mode == "seo":
        run_seo()
    else:
        print("Unknown mode")
