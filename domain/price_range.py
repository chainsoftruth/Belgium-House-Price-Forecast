import requests
from bs4 import BeautifulSoup
import re

class PriceRanges():

    def __init__(self):
        #self.ranges = []
        #self._prev_adj = {"increase": True, "num": 50000}
        #self._absolute_max = 50000000
        #self._session = requests.Session()
        pass

    @staticmethod
    def check_range(self, minprice: int, maxprice: int, session: requests.Session()) -> int:
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

    # def adjust_range(
    #     self, min_max: dict[str: int], increase: bool) -> dict[str: int]:
    #     # adjust_range({"minprice": n, "maxprice: m"}, True/False)
    #     if increase and self._prev_adj["increase"]:
    #         self._prev_adj["num"] *= 2
    #         min_max["maxprice"] += self._prev_adj["num"]
    #     elif not increase and self._prev_adj["increase"]:
    #         self._prev_adj["increase"] = False
    #         self._prev_adj["num"] //= 2
    #         min_max["maxprice"] -= self._prev_adj["num"]
    #     elif increase and not self._prev_adj["increase"]:
    #         self._prev_adj["increase"] = True
    #         self._prev_adj["num"] //= 2
    #         min_max["maxprice"] += self._prev_adj["num"]
    #     elif not increase and not self._prev_adj["increase"]:
    #         min_max["maxprice"] -= self._prev_adj["num"]
    #     return min_max

    # def append_range(self, minprice: int, maxprice: int, results_amount: int):
    #     self.ranges.append(
    #         {
    #             "minprice": minprice,
    #             "maxprice": maxprice,
    #             "results_amount": results_amount
    #         }
    #     )

    # def fill_ranges(self):
    #     min_max = {"minprice": 1, "maxprice": 100000}
    #     if self.ranges != []:
    #         min_max["minprice"] = self.ranges[-1]["maxprice"] + 1
    #     while True:
    #         amount = self.check_range(min_max["minprice"], min_max["maxprice"])
    #         if amount > 800 and amount < 1000:
    #             append_range(min_max["minprice"], min_max["maxprice"], amount)
    #             break
    #         elif amount < 800:
    #             min_max = adjust_range({
    #                 "minprice": min,
    #                 "maxprice": max
    #             }, True)
    #         elif amount > 1000:
    #             min_max = adjust_range({
    #                 "minprice": min,
    #                 "maxprice": max
    #             }, False)

# ranges = PriceRanges()
# results = ranges.check_range(1, 100000)
# print(results)