import pandas as pd
import time
import pyfiglet
from fx_thereyougo_scraper_template import *

def main() -> None:
    """
    This function loops through all the page links to scrape data
    """
    
    page_url = "https://www.thereyougo.in/collections/all-products?page=1"
    
    while True:
        
        print(f'Scraping Page URL: {page_url}')
        
        content = extract_content(page_url)
        scrape_content(content)
        time.sleep(0.5)
        
        print(f'Total Products Collected: {len(all_products)}')
        print('\n')
        
        if extract_nextpage_link(page_url) == None:
            break
        else:
            next_page_link = extract_nextpage_link(page_url)
            page_url = next_page_link
    return

def load_data() -> None:
    """
    This function loads the scraped data into a CSV file
    """
    
    quotes_df = pd.DataFrame(all_products)
    quotes_df.to_csv('thereyougo_products_raw_data.csv', encoding='utf-8', index=False)
    return

if __name__ == '__main__':
    
    scraper_title = "THERE! PRODUCTS COLLECTOR"
    ascii_art_title = pyfiglet.figlet_format(scraper_title, font='small')
    
    print('\n\n')
    print(ascii_art_title)
    print('Collecting Products...')
    
    start_time = datetime.now()
    
    main()
    
    end_time = datetime.now()
    scraping_time = end_time - start_time
    
    print('\n')
    print('All Products Collected...')
    print(f'Time spent on scraping: {scraping_time}')
    print(f'Total products collected: {len(all_products)}')
    print('\n')
    print('Loading data into CSV...')
    
    load_data()
    
    print('Data Exported to CSV...')
    print('Webscraping Completed !!!')