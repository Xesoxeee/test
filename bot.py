import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# URL endpoint
availability_url = "https://app.ludo.gift/api/cases/43/free-availability"
open_free_url = "https://app.ludo.gift/api/cases/43/open-free"

def load_accounts(filename="accounts.txt"):
    """Baca semua akun (query string) dari file"""
    with open(filename) as f:
        return [line.strip() for line in f if line.strip()]

def check_availability(query_string):
    """Cek apakah free spin tersedia"""
    full_url = f"{availability_url}?{query_string}"
    try:
        resp = requests.get(full_url, timeout=10)
        print(f"🔍 [{query_string[:30]}...] Check: {resp.status_code}")
        print(f"Response: {resp.text[:200]}")
        if resp.ok and ('true' in resp.text.lower() or 'available' in resp.text.lower()):
            return True
    except Exception as e:
        print(f"❌ [{query_string[:30]}...] Error check: {e}")
    return False

def claim_free_spin(query_string):
    """Klaim free spin"""
    full_url = f"{open_free_url}?{query_string}"
    try:
        resp = requests.post(full_url, timeout=10)
        print(f"🎁 [{query_string[:30]}...] Claim: {resp.status_code}")
        print(f"Response: {resp.text[:200]}")
    except Exception as e:
        print(f"❌ [{query_string[:30]}...] Error claim: {e}")

def run_for_one_account(query_string):
    """Jalankan untuk satu akun"""
    print(f"\n🚀 Mulai untuk user: {query_string[:50]}...")
    if check_availability(query_string):
        print(f"✅ [{query_string[:30]}...] Free spin tersedia, klaim sekarang!")
        claim_free_spin(query_string)
    else:
        print(f"⏳ [{query_string[:30]}...] Free spin belum tersedia.")
    print("=" * 60)

def run_all_accounts():
    """Jalankan untuk semua akun dalam file"""
    accounts = load_accounts()
    with ThreadPoolExecutor(max_workers=min(10, len(accounts))) as executor:
        futures = [executor.submit(run_for_one_account, acc) for acc in accounts]
        for future in as_completed(futures):
            pass

if __name__ == "__main__":
    while True:
        print("\n🔄 Menjalankan semua akun dari file untuk free spin…")
        run_all_accounts()
        print("✅ Semua akun selesai. Tunggu 24 jam lagi…")
        print("=" * 60)
        time.sleep(24 * 60 * 60)  # tunggu 24 jam
