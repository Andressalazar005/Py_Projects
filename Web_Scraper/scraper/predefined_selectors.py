# scraper/predefined_selectors.py

PREDEFINED_SELECTORS = {
    'amazon': {
        'product_name': 'span.a-text-normal',
        'price': 'span.a-price-whole',
        'rating': 'span.a-icon-alt',
        'reviews': 'span.a-size-base',
        'link': 'a.a-link-normal'
    }
}

def get_predefined_selectors(site_name):
    return PREDEFINED_SELECTORS.get(site_name, {})