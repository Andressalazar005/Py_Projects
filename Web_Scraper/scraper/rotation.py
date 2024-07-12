import random
import requests
from fake_useragent import UserAgent

def get_random_headers():
    ua = UserAgent()
    return {
        'User-Agent': ua.random,
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

def make_request_with_rotation(url, proxies, max_retries=5, backoff_factor=1):
    for attempt in range(max_retries):
        headers = get_random_headers()
        proxy = random.choice(proxies)
        try:
            response = requests.get(url, headers=headers, proxies={'http': proxy, 'https': proxy})
            if response.status_code == 200:
                return response
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {backoff_factor * (2 ** attempt)} seconds...")
            time.sleep(backoff_factor * (2 ** attempt))
    return None
