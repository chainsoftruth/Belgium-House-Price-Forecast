import requests
import re
from bs4 import BeautifulSoup as bs
from scraper.py import PropertyScraper
from price_range.py import PriceRanges as pr

class Links():
    _LINK = [
        ("https://immovlan.be/en/real-estate?transactiontypes=for-sale&prop"
        "ertytypes=house,apartment&minprice="),
        "&maxprice=", "&page=", "&noindex=1"
        ]
    _session = requests.Session()
    _headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
        "537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36")
        }
    
    def __init__(self):
        self._links: list[str] = []

    def scrape(self) -> list[str]:
        price_range = {"min": 1, "max": 50000000}
        results_left = pr.check_range(price_range["min"], price_range["max"])
        while results_left > 0:
            pages = results_left // 20 
            + (1 if results_left % 20 else 0)
            if pages > 50:
                pages = 50
            links_list = self.scrape_range(
                price_range["min"],
                price_range["max"],
                pages
            )
            self._links.extend(links_list)
            price_range["min"] = self.get_price(self._links[-1])
            results_left = pr.check_range(price_range["min"], price_range["max"])
        self.cleaner()
        return self._links

    @classmethod
    def scrape_range(cls, minprice: int, maxprice: int, pages: int) -> list[str]:
        links = []
        for index in range(pages):
            page = cls._session.get(
                cls._LINK[0]
                + str(minprice)
                + cls._LINK[1]
                + str(maxprice)
                + cls._LINK[2]
                + str(index + 1)
                + cls._LINK[3],
                headers = cls._headers
            ).content
            search_results = bs(page, "html.parser").find(
                "section", attrs = {"id": "search-results"})
            articles = search_results.find_all("article")
            for article in articles:
                if article != None:
                    links.append(article.get("data-url"))
        return links
    
    @staticmethod
    def get_price(link: str) -> int:
        prop_scraper = PropertyScraper(link)
        return prop_scraper.data["Price"]

    def cleaner(self):
        values = self._links
        result = []
        for v in values:
            if v != None and v.find("projectdetail") == -1 and v not in result:
                result.append(v)
        self._links = result
