import ctypes
import time
import sys

# Windows Constants
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

def keep_awake():
    print("RIMI ANTI-SLEEP ACTIEF: Je computer blijft nu wakker.")
    print("Druk op Ctrl+C in deze terminal om dit te stoppen.")
    
    # Voorkom slaapstand van systeem en scherm
    ctypes.windll.kernel32.SetThreadExecutionState(
        ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
    )
    
    try:
        while True:
            # Kleine heartbeats om te laten zien dat het draait
            time.sleep(60)
            print(f"Keep-Alive Heartbeat: {time.strftime('%H:%M:%S')}")
    except KeyboardInterrupt:
        # Reset naar normale staat
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        print("\nAnti-sleep gestopt.")

if __name__ == "__main__":
    keep_awake()
