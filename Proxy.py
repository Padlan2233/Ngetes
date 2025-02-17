import requests
from concurrent.futures import ThreadPoolExecutor

# URL API Proxyscrape untuk mengambil daftar proxy HTTP
PROXY_SCRAPE_API = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=1000&country=all"

def fetch_proxies():
    """Mengambil daftar proxy dari Proxyscrape."""
    response = requests.get(PROXY_SCRAPE_API)
    if response.status_code == 200:
        proxies = response.text.split('\n')
        return [proxy.strip() for proxy in proxies if proxy.strip()]
    else:
        print("Gagal mengambil proxy.")
        return []

def check_proxy(proxy):
    """Memeriksa apakah proxy valid."""
    try:
        response = requests.get("http://httpbin.org/ip", proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=5)
        if response.status_code == 200:
            print(f"Proxy valid: {proxy}")
            return proxy
    except:
        pass
    return None

def main():
    proxies = fetch_proxies()
    print(f"Total proxy yang diambil: {len(proxies)}")

    valid_proxies = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(check_proxy, proxies)
        for result in results:
            if result:
                valid_proxies.append(result)

    print(f"Total proxy valid: {len(valid_proxies)}")
    with open("valid_proxies.txt", "w") as file:
        for proxy in valid_proxies:
            file.write(f"{proxy}\n")

if __name__ == "__main__":
    main()
