import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# endpoint untuk cek & klaim free spin
availability_url = "https://app.ludo.gift/api/cases/43/free-availability"
open_free_url = "https://app.ludo.gift/api/cases/43/open-free"

def load_tokens(filename="accounts.txt"):
    """Baca Bearer tokens dari file"""
    with open(filename) as f:
        return [line.strip() for line in f if line.strip()]

def check_availability(bearer):
    """Cek apakah free spin tersedia"""
    headers = {
        "Authorization": f"Bearer {bearer}"
    }
    try:
        resp = requests.get(availability_url, headers=headers, timeout=10)
        print(f"🔍 [{bearer[:10]}...] Check: {resp.status_code}")
        print(f"Response: {resp.text[:200]}")
        if resp.ok and ('true' in resp.text.lower() or 'available' in resp.text.lower()):
            return True
    except Exception as e:
        print(f"❌ [{bearer[:10]}...] Error check: {e}")
    return False

def claim_free_spin(bearer):
    """Klaim free spin"""
    headers = {
        "Authorization": f"Bearer {bearer}"
    }
    try:
        resp = requests.post(open_free_url, headers=headers, timeout=10)
        print(f"🎁 [{bearer[:10]}...] Claim: {resp.status_code}")
        print(f"Response: {resp.text[:200]}")
    except Exception as e:
        print(f"❌ [{bearer[:10]}...] Error claim: {e}")

def run_for_one_account(bearer):
    """Jalankan untuk satu akun"""
    print(f"\n🚀 Mulai untuk Bearer: {bearer[:20]}...")
    if check_availability(bearer):
        print(f"✅ [{bearer[:10]}...] Free spin tersedia, klaim sekarang!")
        claim_free_spin(bearer)
    else:
        print(f"⏳ [{bearer[:10]}...] Free spin belum tersedia.")
    print("=" * 60)

def run_all_accounts():
    """Jalankan untuk semua akun"""
    tokens = load_tokens()
    with ThreadPoolExecutor(max_workers=min(10, len(tokens))) as executor:
        futures = [executor.submit(run_for_one_account, token) for token in tokens]
        for future in as_completed(futures):
            pass

if __name__ == "__main__":
    while True:
        print("\n🔄 Menjalankan semua akun dari file untuk free spin…")
        run_all_accounts()
        print("✅ Semua akun selesai. Tunggu 24 jam lagi…")
        print("=" * 60)
        time.sleep(24 * 60 * 60)  # tunggu 24 jam
