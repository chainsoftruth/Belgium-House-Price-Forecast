import requests
from bs4 import BeautifulSoup
import re

class PriceRanges():

    @staticmethod
    def check_range(minprice: int, maxprice: int, session: requests.Session()) -> int:
        """Returns amount of results"""
        url = (
            "https://immovlan.be/en/real-estate"
            "?transactiontypes=for-sale"
            "&propertytypes=house,apartment"
            f"&minprice={minprice}"
            f"&maxprice={maxprice}"
            "&noindex=1"
        )
        headers = {
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
            "537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36")
        }
        response = session.get(url, headers = headers)
        soup = BeautifulSoup(response.text, "html.parser")
        search_results = soup.find("section", attrs = {"id": "search-results"})
        if not search_results:
            return -1
        results_div = search_results.find("div", attrs = {"class": "col-12 mb-2"})
        if not results_div:
            return -2
        text = results_div.get_text(" ", strip = True).lower()
        match = re.search(r"(\d+)\s+results", text)
        if match:
            return int(match.group(1))
        return -3