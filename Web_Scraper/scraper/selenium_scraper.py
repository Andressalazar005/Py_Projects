try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
except ImportError as e:
    webdriver = None
    Options = None
    print("Selenium is not installed. Please install it to use this feature.")
    
from bs4 import BeautifulSoup

def make_request_with_selenium(url):
    if webdriver is None or Options is None:
        print("Selenium is not available. Skipping Selenium tier.")
        return None
    
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return soup
