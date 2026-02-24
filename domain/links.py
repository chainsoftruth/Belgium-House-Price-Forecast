import requests
import re
from bs4 import BeautifulSoup as bs
from domain.scraper import PropertyScraper
from domain.price_range import PriceRanges as pr

class Links():
    _LINK = [
        ("https://immovlan.be/en/real-estate?transactiontypes=for-sale&prop"
        "ertytypes=house,apartment&minprice="),
        "&maxprice=", "&page=", "&sortdirection=ascending&sortby=price&noindex=1"
        ]
    _session = requests.Session()
    _headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
        "537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36")
        }
    
    def __init__(self):
        self._links: list[str] = []
        page = self.get_page(
            "https://immovlan.be/en/real-estate?transactiontypes=for-sale&property"
            "types=house,apartment&sortdirection=descending&sortby=price&noindex=1"
        ).content
        search_results = bs(page, "html.parser").find(
            "section", attrs = {"id": "search-results"})
        articles = search_results.find_all("article")
        self._absolute_max = self.get_price(articles[0].get("data-url"))


    def scrape(self) -> list[str]:
        price_range = {"min": 1, "max": self._absolute_max}
        results_left = pr.check_range(price_range["min"], price_range["max"], self._session)
        print(results_left)
        while results_left > 0:
            print("all goes good")
            pages = results_left // 20 
            if results_left % 20 > 0:
                pages += 1
            if pages > 50:
                pages = 50
            links_list = self.scrape_range(
                price_range["min"],
                price_range["max"],
                pages
            )
            self._links.extend(links_list)
            index = -1
            while True:
                if self.get_price(self._links[index]) == "None" \
                    or self.get_price(self._links[index]) == None:
                    index -= 1
                    continue
                price_range["min"] = self.get_price(self._links[index])
                break
            if price_range["min"] == price_range["max"]:
                break
            results_left = pr.check_range(price_range["min"], price_range["max"], self._session)
            print("------results_left ", results_left)
            print(price_range["min"], price_range["max"])
        self.cleaner()
        return self._links

    @classmethod
    def get_page(cls, link):
        return cls._session.get(link, headers = cls._headers)

    @classmethod
    def scrape_range(cls, minprice: int, maxprice: int, pages: int) -> list[str]:
        links = []
        for index in range(pages):
            page = cls.get_page(
                cls._LINK[0]
                + str(minprice)
                + cls._LINK[1]
                + str(maxprice)
                + cls._LINK[2]
                + str(index + 1)
                + cls._LINK[3]
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
