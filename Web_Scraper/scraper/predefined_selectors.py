# scraper/predefined_selectors.py

PREDEFINED_SELECTORS = {
    'amazon': {
        'name': 'span.a-text-normal',
        'price': 'span.a-price-whole',
        'rating': 'span.a-icon-alt',
        'reviews': 'span.a-size-base',
    },
    'ebay': {
        'name': 'h3.s-item__title',
        'price': 'span.s-item__price',
        'rating': 'div.x-star-rating span.clipped',
        'reviews': 'span.s-item__reviews-count',
    },
    'walmart': {
        'name': 'a.product-title-link span',
        'price': 'span.price-main span.price-characteristic',
        'rating': 'span.stars-reviews-count-node',
        'reviews': 'span.stars-reviews-count',
    },
    'bestbuy': {
        'name': 'h4.sku-header a',
        'price': 'div.priceView-hero-price span',
        'rating': 'div.c-ratings-reviews a',
        'reviews': 'span.c-reviews',
    },
    'aliexpress': {
        'name': 'a._18_85',
        'price': 'div._12A8D span._1kNf9',
        'rating': 'span.eXPaM',
        'reviews': 'a._2_R_D',
    },
    'target': {
        'name': 'a.h-display-block',
        'price': 'span.h-text-bs',
        'rating': 'span[aria-label*="out of 5 stars"]',
        'reviews': 'span.h-text-sm',
    },
    'indeed': {
        'title': 'h2.jobTitle span',
        'location': 'div.companyLocation',
        'pay': 'span.salary-snippet',
        'remote': 'span.remote',
        'benefits': 'div.job-snippet ul'
    },
    'linkedin': {
        'title': 'h3.result-card__title',
        'location': 'span.job-result-card__location',
        'pay': 'span.salary',
        'remote': 'span.remote',
        'benefits': 'ul.job-criteria__list'
    },
    'glassdoor': {
        'title': 'a.jobLink span',
        'location': 'span.jobLoc',
        'pay': 'span.salaryText',
        'remote': 'span.remote',
        'benefits': 'div.job-snippet'
    },
    'monster': {
        'title': 'h2.title',
        'location': 'div.location',
        'pay': 'div.salary',
        'remote': 'div.remote',
        'benefits': 'div.benefits'
    },
    'ziprecruiter': {
        'title': 'h2.job_title',
        'location': 'p.location',
        'pay': 'p.salary',
        'remote': 'span.remote_icon',
        'benefits': 'div.snippet_container'
    }
}

def get_predefined_selectors(site_name):
    return PREDEFINED_SELECTORS.get(site_name, {})
