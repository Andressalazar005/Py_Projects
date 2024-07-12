import requests
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from random import randint

def initial_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

def request_with_user_agent(url):
    try:
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the URL with user agent: {e}")
        return None

def request_with_delay(url):
    try:
        time.sleep(randint(1, 5))
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the URL with delay: {e}")
        return None

def request_with_selenium(url):
    try:
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(randint(2, 5))
        html = driver.page_source
        driver.quit()
        return html
    except Exception as e:
        print(f"Error fetching the URL with Selenium: {e}")
        return None
