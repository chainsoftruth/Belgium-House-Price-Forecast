from data.manager import DataManager
from domain.links import Links
from domain.scraper import PropertyScraper
from domain.data_cleaner import DataCleaner as dc
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

def update_links() -> list[str]:
    links = Links()
    print("SCRAPING...")
    links_list = links.scrape()
    print("SCRAPED: OK")
    DataManager.links_export(links_list)
    return links_list

def update_dataset():
    links = DataManager.links_import()
    data_list = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit all links as futures
        futures = [executor.submit(scrape_property, link) for link in links]
        # Process results as soon as each future completes
        for future in tqdm(as_completed(futures), total=len(futures)):
            data = future.result()
            if data is not None:
                data_list.append(data)
    DataManager.data_csv_export(data_list)

def scrape_property(link):
    try:
        scraper = PropertyScraper(link) 
        return scraper.scrape()
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        if status in (404, 410):
            print(f"Skipping {status} page: {link}")
            return None
        else:
            raise
    except Exception as e:
        print(f"Error scraping {link}: {e}")
        return None
    
def trim_data():
    data = DataManager.data_csv_import()
    trimmed_data = dc.trim_data_edges(data)
    DataManager.clean_data_csv_export(trimmed_data)
    print(trimmed_data)
    dc.check(trimmed_data)

# Uncomment to update data:
# update_links()
# update_dataset()
# trim_data()