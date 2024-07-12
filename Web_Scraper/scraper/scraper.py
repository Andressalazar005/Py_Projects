import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href=True)
    return [urljoin(url, link['href']) for link in links]  # Convert relative URLs to full URLs
