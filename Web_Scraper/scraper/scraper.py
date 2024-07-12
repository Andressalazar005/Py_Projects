import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def scrape_website(url, selectors):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = []
    
    for selector, include in selectors:
        if include:
            elements = soup.select(selector)
            for element in elements:
                if element.name == "a":
                    results.append(urljoin(url, element.get('href')))
                elif element.name == "img":
                    results.append(urljoin(url, element.get('src')))
                else:
                    results.append(element.get_text(strip=True))
    
    return results
