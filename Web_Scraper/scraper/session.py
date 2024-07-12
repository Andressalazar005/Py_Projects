import requests
import time

def make_request_with_session(url, session, headers, max_retries=5, backoff_factor=1):
    for attempt in range(max_retries):
        try:
            response = session.get(url, headers=headers)
            if response.status_code == 200:
                return response
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {backoff_factor * (2 ** attempt)} seconds...")
            time.sleep(backoff_factor * (2 ** attempt))
    return None
