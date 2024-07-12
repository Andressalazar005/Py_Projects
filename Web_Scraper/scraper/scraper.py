import logging
import requests
from bs4 import BeautifulSoup
from scraper.tiered_requests import initial_request, request_with_user_agent, request_with_delay, request_with_selenium

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_website(url, selectors):
    logging.info(f"Starting to scrape the website: {url}")

    response = initial_request(url)
    if not response:
        logging.warning("Initial request failed, trying with user agent...")
        response = request_with_user_agent(url)

    if not response:
        logging.warning("User agent request failed, trying with delay...")
        response = request_with_delay(url)

    if not response:
        logging.warning("Delayed request failed, trying with Selenium...")
        response = request_with_selenium(url)

    if not response:
        logging.error("All request methods failed. Cannot scrape the website.")
        return "Error"

    if isinstance(response, str):
        soup = BeautifulSoup(response, 'html.parser')
    else:
        soup = BeautifulSoup(response.content, 'html.parser')

    data = []
    for selector, include in selectors:
        logging.debug(f"Processing selector: {selector} (include: {include})")
        elements = soup.select(selector)
        if include:
            for element in elements:
                text = element.get_text(strip=True)
                data.append(text)
                logging.debug(f"Found data: {text}")

    logging.info("Scraping completed.")
    return data
