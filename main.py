from data.manager import DataManager
from domain.links import Links
from domain.scraper import PropertyScraper
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests


def update_ranges():
    pass

def update_links() -> list[str]:
    links = Links()
    print("SCRAPING...")
    links_list = links.scrape()
    print("SCRAPED: OK")
    return links_list

def scrape_property(link):
    try:
        scraper = PropertyScraper(link) 
        return scraper.scrape()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 410:
            print(f"Property removed (410): {link}")
            return None  # skip permanently
        else:
            raise  # re-raise other HTTP errors
    except Exception as e:
        print(f"Error scraping {link}: {e}")
        return None
    
# links = update_links()
# DataManager.links_export(links)
# OR 
links = DataManager.links_import()
links = links[:100]
data_list = []
with ThreadPoolExecutor(max_workers=10) as executor:
    # Submit all links as futures
    futures = [executor.submit(scrape_property, link) for link in links]

    # Process results as soon as each future completes
    for future in tqdm(as_completed(futures), total=len(futures)):
        data = future.result()
        if data is not None:
            data_list.append(data)
for data in data_list:
    print(data)