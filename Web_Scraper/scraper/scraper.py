import requests
from fake_useragent import UserAgent
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging
import re
from scraper.predefined_selectors import get_predefined_selectors
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initial_request(url, proxies=None):
    try:
        logging.info("Starting initial request.")
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
        logging.info("Initial request successful.")
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching the URL: {e}")
        return None

def request_with_user_agent(url, proxies=None):
    try:
        logging.info("Starting request with user agent.")
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        response = requests.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()
        logging.info("Request with user agent successful.")
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching the URL with user agent: {e}")
        return None

def request_with_delay(url, proxies=None):
    try:
        logging.info("Starting request with delay.")
        time.sleep(5)
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
        logging.info("Request with delay successful.")
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching the URL with delay: {e}")
        return None

def request_with_selenium(url):
    try:
        logging.info("Starting request with Selenium.")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(5)  # Wait for the page to fully load
        response = driver.page_source
        driver.quit()
        logging.info("Request with Selenium successful.")
        return response
    except Exception as e:
        logging.error(f"Error fetching the URL with Selenium: {e}")
        return None

def extract_page_title(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.title.string if soup.title else "No title found"
        return title
    except Exception as e:
        logging.error(f"Error extracting page title: {e}")
        return "No title found"

def parse_site_name(url):
    domain = re.findall(r"https?://(www\.)?([^/]+)", url)
    if domain:
        return domain[0][1].split('.')[0]
    return ""

def scrape_website(url, selectors=None):
    logging.info(f"Starting to scrape website: {url}")
    site_name = url.split('//')[-1].split('/')[0].split('.')[1]
    predefined_selectors = get_predefined_selectors(site_name)

    response = initial_request(url)
    if not response:
        response = request_with_user_agent(url)
    if not response:
        response = request_with_delay(url)
    if not response:
        response = request_with_selenium(url)
        if isinstance(response, str):
            html_content = response
        else:
            return None

    html_content = response.content if not isinstance(response, str) else response
    page_title = extract_page_title(html_content)
    logging.info(f"Page title extracted: {page_title}")

    soup = BeautifulSoup(html_content, 'html.parser')
    scraped_data = []

    if selectors:
        item_selector = predefined_selectors.get('item', 'div')  # Use the predefined item container selector
        items = soup.select(item_selector)
        for item in items:
            item_data = {}
            valid_data = True  # Flag to check if item contains valid data

            for selector_name, include in selectors:
                selector = predefined_selectors.get(selector_name, selector_name)
                element = item.select_one(selector)
                if element:
                    if selector_name == 'price':
                        whole = item.select_one('span.a-price-whole')
                        fraction = item.select_one('span.a-price-fraction')
                        if whole and fraction:
                            item_data['price'] = f"{whole.text.strip()}.{fraction.text.strip()}"
                        elif whole:
                            item_data['price'] = whole.text.strip()
                        else:
                            item_data['price'] = None
                        logging.info(f"Extracted price: {item_data['price']}")
                    else:
                        item_data[selector_name] = element.get_text(strip=True) if include else str(element)
                else:
                    logging.warning(f"Element not found for selector: {selector_name}")
                    valid_data = False  # Mark as invalid data if any selector is not found

            link_element = item.select_one('a.a-link-normal')
            if link_element and 'href' in link_element.attrs:
                item_data['URL'] = urljoin(url, link_element['href'])
            else:
                item_data['URL'] = url  # fallback to the main page URL if item URL is not found

            if valid_data and len(item_data) > 1:
                # Check if the current item_data already exists in scraped_data
                composite_key = tuple(item_data.get(selector_name) for selector_name, _ in selectors)
                if not any(composite_key == tuple(scraped_item.get(selector_name) for selector_name, _ in selectors) for scraped_item in scraped_data):
                    scraped_data.append(item_data)
                    logging.info(f"Scraped data: {item_data}")
                else:
                    logging.info(f"Duplicate found and ignored: {item_data}")

    return {'title': page_title, 'data': scraped_data}