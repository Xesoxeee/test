import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# endpoint untuk cek & klaim free spin
availability_url = "https://app.ludo.gift/api/cases/43/free-availability"
open_free_url = "https://app.ludo.gift/api/cases/43/open-free"

def load_accounts(filename="accounts.txt"):
    """Load daftar user_id dari file"""
    accounts = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # validasi: harus ada isinya & tidak ada spasi
                if line and not line.startswith("#"):  # bisa pakai # untuk komentar
                    user_id = line.split()[0]  # kalau ada lebih dari 1 kolom, ambil kolom pertama
                    accounts.append(user_id)
        if not accounts:
            print("⚠️ Tidak ada akun valid di file.")
        return accounts
    except Exception as e:
        print(f"❌ Gagal membaca file akun: {e}")
        return []

def check_availability(user_id):
    """Cek apakah free spin tersedia"""
    query = f"user_id={user_id}"
    full_url = f"{availability_url}?{query}"
    try:
        resp = requests.get(full_url, timeout=10)
        print(f"🔍 [{user_id}] Check: {resp.status_code}")
        print(f"Response: {resp.text[:200]}")
        if resp.ok and ('true' in resp.text.lower() or 'available' in resp.text.lower()):
            return True
    except Exception as e:
        print(f"❌ [{user_id}] Error check: {e}")
    return False

def claim_free_spin(user_id):
    """Klaim free spin"""
    query = f"user_id={user_id}"
    full_url = f"{open_free_url}?{query}"
    try:
        resp = requests.post(full_url, timeout=10)
        print(f"🎁 [{user_id}] Claim: {resp.status_code}")
        print(f"Response: {resp.text[:200]}")
    except Exception as e:
        print(f"❌ [{user_id}] Error claim: {e}")

def run_for_one_account(user_id):
    """Proses untuk satu akun"""
    print(f"\n🚀 Mulai untuk user: {user_id}")
    if check_availability(user_id):
        print(f"✅ [{user_id}] Free spin tersedia, klaim sekarang!")
        claim_free_spin(user_id)
    else:
        print(f"⏳ [{user_id}] Free spin belum tersedia.")
    print("=" * 60)

def run_all_accounts():
    """Jalankan semua akun dari file"""
    accounts = load_accounts()
    if not accounts:
        print("🚫 Tidak ada akun untuk dijalankan.")
        return
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