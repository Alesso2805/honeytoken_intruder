import requests
import time

BASE_URL = "http://localhost:5000"

def simulate_attack():
    print("--- 🛡️ Honeytoken Intrusion Test ---")
    
    print("\n[+] Testing legitimate health check endpoint...")
    try:
        r = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"Status: {r.status_code} | Body: {r.json()}")
    except:
        print("❌ Error: Is the Flask server running? Try: python main.py")
        return

    print("\n[!] 🔥 ATTACKING: Accessing /.env trap...")
    r = requests.get(f"{BASE_URL}/.env")
    print(f"Status: {r.status_code} | System logic: Honeytoken Triggered")

    print("\n[!] 🔥 ATTACKING: Accessing /admin/config-backup trap...")
    r = requests.get(f"{BASE_URL}/admin/config-backup")
    print(f"Status: {r.status_code} | System logic: Honeytoken Triggered")

    print("\n[!] 🎭 DECEPTION: Accessing /admin/login (Fake Portal)...")
    r = requests.get(f"{BASE_URL}/admin/login")
    if "Infrastructure Portal" in r.text:
         print(f"Status: {r.status_code} | System logic: Attacker DECEIVED (Showing Fake Login)")
    else:
         print(f"Status: {r.status_code} | System logic: Error in Deception Layer")

    print("\n[✔] Check your DB ('honeytoken.db') and Discord Webhook if configured!")

if __name__ == "__main__":
    simulate_attack()
