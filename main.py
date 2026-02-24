from data.manager import DataManager
from domain.links import Links
from domain.scraper import PropertyScraper

def update_ranges():
    pass

def update_links(price_ranges: list[dict[str: int]]) -> list[str]:
    links = Links(price_ranges)
    print("SCRAPING...")
    links_list = links.scrape()
    print("SCRAPED: OK")
    return links_list
    
price_ranges = [
    {"minprice": 1, "maxprice": 100000, "amount": 943}
    # {"minprice": 100001, "maxprice": 135000, "amount": 989},
    # {"minprice": 135001, "maxprice": 150000, "amount": 867}
]
# links = update_links(price_ranges)
# DataManager.links_export(links)
# OR 
links = DataManager.links_import()
links = links[:50]
print(links)
data_list = []
for link in links:
    scraper = PropertyScraper(link)
    data_list.append(scraper.scrape())
print(data_list)