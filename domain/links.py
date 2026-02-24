import requests
from bs4 import BeautifulSoup as bs
import re

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
    
    def __init__(self, price_ranges: list[dict[str:int]]):
        self.price_ranges: list[dict[str:int]] = price_ranges
        self._links: list[str] = []

    def scrape(self) -> list[str]:
        for range_dict in self.price_ranges:
            pages = range_dict["amount"] // 20 
            + (1 if range_dict["amount"] else 0)
            links_list = self.scrape_range(
                range_dict["minprice"],
                range_dict["maxprice"],
                pages
            )
            self._links.extend(links_list)
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
    
    def cleaner(self):
        values = self._links
        result = []
        for v in values:
            if v != None and v.find("projectdetail") == -1:
                result.append(v)
        self._links = result
