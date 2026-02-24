from data.manager import DataManager
from domain.links import Links
from domain.scraper import PropertyScraper

def update_ranges():
    pass

def update_links() -> list[str]:
    links = Links()
    print("SCRAPING...")
    links_list = links.scrape()
    print("SCRAPED: OK")
    return links_list

links = update_links()
DataManager.links_export(links)
# OR 
# links = DataManager.links_import()
# links = links[:50]
# print(links)
# data_list = []
# for link in links:
#     scraper = PropertyScraper(link)
#     data_list.append(scraper.scrape())
# print(data_list)