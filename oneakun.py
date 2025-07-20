import requests
import time

availability_url = "https://app.ludo.gift/api/cases/43/free-availability"
open_free_url = "https://app.ludo.gift/api/cases/43/open-free"

def load_bearers(filename="accounts.txt"):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip()]

def check_availability(bearer):
    headers = {
        "Authorization": f"Bearer {bearer}",
        "Accept": "application/json"
    }
    try:
        resp = requests.get(availability_url, headers=headers, timeout=10)
        print(f"🔍 [{bearer[:10]}...] Check: {resp.status_code}")
        print(f"Response: {resp.text[:200]}")
        if resp.ok and '"available":true' in resp.text.lower():
            return True
    except Exception as e:
        print(f"❌ [{bearer[:10]}...] Error check: {e}")
    return False

def claim_free_spin(bearer):
    headers = {
        "Authorization": f"Bearer {bearer}",
        "Content-Type": "application/json"
    }
    data = {
        "case_id": 43
    }
    try:
        resp = requests.post(open_free_url, headers=headers, json=data, timeout=10)
        print(f"🎁 [{bearer[:10]}...] Claim: {resp.status_code}")
        print(f"Response: {resp.text[:200]}")
    except Exception as e:
        print(f"❌ [{bearer[:10]}...] Error claim: {e}")

def run_for_one_account(bearer):
    print(f"\n🚀 Mulai untuk Bearer: {bearer[:10]}...")
    if check_availability(bearer):
        print(f"✅ [{bearer[:10]}...] Free spin tersedia, klaim sekarang!")
        claim_free_spin(bearer)
    else:
        print(f"⏳ [{bearer[:10]}...] Free spin belum tersedia.")
    print("=" * 60)

def run_all_accounts():
    accounts = load_bearers()
    for acc in accounts:
        run_for_one_account(acc)

if __name__ == "__main__":
    while True:
        print("\n🔄 Menjalankan semua akun dari file untuk free spin…")
        run_all_accounts()
        print("✅ Semua akun selesai. Tunggu 24 jam lagi…")
        print("=" * 60)
        time.sleep(24 * 60 * 60)  # tunggu 24 jam
