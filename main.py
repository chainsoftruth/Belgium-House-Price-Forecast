from data.manager import DataManager
from domain.links import Links
from domain.scraper import PropertyScraper
import pandas as pd

def update_links() -> list[str]:
    links = Links()
    print("SCRAPING...")
    links_list = links.scrape()
    print("SCRAPED: OK")
    return links_list

def update_dataset():
    links = DataManager.links_import()
    data_list = []
    for link in links:
        scraper = PropertyScraper(link)
        data_list.append(scraper.scrape())
    DataManager.data_csv_export(data_list)

data = DataManager.data_csv_import()
print(data)