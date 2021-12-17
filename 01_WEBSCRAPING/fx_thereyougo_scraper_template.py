import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone, timedelta

SESSION = requests.Session()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "accept-language": "en-US"
}

all_products = []

def extract_content(page_url: str) -> str:
    """
    This function takes the page URL as an input and returns the HTML content that has all the products and their related attributes from that page.
    Args:
        page_url (str): The page URL
    Returns:
        str: HTML content only having the quotes and related details 
    """
    
    response = SESSION.get(page_url, headers=HEADERS)
    
    soup = BeautifulSoup(response.content, 'lxml')
    
    content = soup.select('a.grid-view-item__link')
    return content

def scrape_content(content: str) -> None:   
    """
    This functions takes the HTML content of a specific page URL as an input argument; scrapes the products along with their related attributes and stores it in 'all_products' list
    Args:
        content (str): The HTML content having the quotes and their related attributes from a specific page
    Returns:
        None: This function returns nothing but adds the scraped content into 'all_books' list
    """
    
    root_url = 'https://www.thereyougo.in'
    
    ist_timezone = timezone(timedelta(hours=5.5))
    current_ist_timestamp = datetime.now(ist_timezone).strftime('%d-%b-%Y %H:%M:%S')
    
    for product in content:
        product_name = product.find('div', class_ = 'grid-view-item__title').text
        price = product.find('span', class_ = 'money').text.replace('Rs.', '').replace(',','').strip()
        product_details_link = urljoin(root_url, product['href'])
        product_image_link = 'https:' + product.find('img')['src']
        
        product_details={
            'product_name': product_name,
            'price': price,
            'product_details_link': product_details_link,
            'product_image_link': product_image_link,
            'last_updated_at_IST': current_ist_timestamp
        }
        
        all_products.append(product_details)
    return

def extract_nextpage_link(page_url: str) -> str:
    """
    This function checks whether the "next page" button is present in the webpage or, not and returns the value accordingly.
    Args:
        page_url (str): This is the input page URL
    Returns:
        str: next page URL; if it exists, otherwise, the function will return "None"
    """

    root_url = 'https://www.thereyougo.in'
    
    response = SESSION.get(page_url, headers=HEADERS)
    
    soup = BeautifulSoup(response.content, 'lxml')
    
    if len(soup.select('ul.list--inline.pagination li:last-child a')) != 0:
        next_page_partial_link = soup.select('ul.list--inline.pagination li:last-child a')[0]['href']
        next_page_link = urljoin(root_url, next_page_partial_link)
    else:
        next_page_link = None
    return next_page_link

# Testing the scraper template #
# ---------------------------- #

if __name__ == '__main__':
    
    page_url = 'https://www.thereyougo.in/collections/all-products?page=11'
    
    print('\n')
    print(f'Page URL to scrape: {page_url}')
    print('\n')
    
    content = extract_content(page_url)
    scrape_content(content)
    
    print('\n')
    print(f'Total quotes scraped: {len(all_products)}')
    print('\n')
    print(all_products)
    
    print('\n')
    print(f"Does next page exists? : {extract_nextpage_link(page_url) != None}")
    print('\n')
    print(f"Next Page URL: {extract_nextpage_link(page_url) }")