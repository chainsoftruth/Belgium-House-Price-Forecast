from data.manager import DataManager
from domain.links import Links
from domain.scraper import PropertyScraper
from domain.data_cleaner import DataCleaner
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import pandas as pd

def update_links() -> list[str]:
    links = Links()
    print("SCRAPING...")
    links_list = links.scrape()
    print("SCRAPED: OK")
    DataManager.links_export(links_list)
    return links_list

def _scrape_property(link):
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

def update_dataset():
    links = DataManager.links_import()
    links = links[:500]
    data_list = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(_scrape_property, link) for link in links]
        for future in tqdm(as_completed(futures), total=len(futures)):
            data = future.result()
            if data is not None:
                data_list.append(data)
    DataManager.data_csv_export(data_list, "raw_dataset")
    
def clear_data() -> pd.DataFrame:
    data = DataManager.raw_data_csv_import()
    clean_data = DataCleaner.optimize(data)
    DataManager.dataframe_csv_export(clean_data, "clean_dataset")
    DataCleaner.check(clean_data)