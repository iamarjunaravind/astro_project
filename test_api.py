import requests

base_url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope"
sign = "aries"

endpoints = [
    f"{base_url}/daily?sign={sign}&day=today",
    f"{base_url}/daily?sign={sign}&day=tomorrow",
    f"{base_url}/daily?sign={sign}&day=yesterday",
    f"{base_url}/weekly?sign={sign}",
    f"{base_url}/monthly?sign={sign}",
    f"{base_url}/yearly?sign={sign}",
]

for url in endpoints:
    try:
        response = requests.get(url)
        print(f"URL: {url}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            success = data.get('success', False)
            print(f"Success Field: {success}")
            # print(f"Data keys: {data.get('data', {}).keys()}")
        else:
            print("Failed")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)
