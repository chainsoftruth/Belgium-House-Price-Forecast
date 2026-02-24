import requests
from bs4 import BeautifulSoup
import re

class PriceRanges():

    def init(self):
        self.ranges = []
        self._prev_adj = {"increase": True, "num": 50000}
        self._absolute_max = 50000000

    def check_range(self, minprice: int, maxprice: int) -> int:
        """
        Returns:
        amount of results
        """

        url = (
        "https://immovlan.be/en/real-estate"
        "?transactiontypes=for-sale"
        "&propertytypes=house,apartment"
        f"&minprice={minprice}"
        f"&maxprice={maxprice}"
        "&noindex=1"
    )

def get_results_count(minprice, maxprice):
    url = (
        "https://immovlan.be/en/real-estate"
        "?transactiontypes=for-sale"
        "&propertytypes=house,apartment"
        f"&minprice={minprice}"
        f"&maxprice={maxprice}"
        "&noindex=1"
    )

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    search_results = soup.find("section", id="search-results")
    if not search_results:
        return 0

    results_div = search_results.find("div", class_="col-12 mb-2")
    if not results_div:
        return 0

    text = results_div.get_text(" ", strip=True).lower()

    match = re.search(r"(\d+)\s+results", text)
    if match:
        return int(match.group(1))

    return 0

tests = [
    (1, 100000),
    (100000, 200000),
    (200000, 300000),
]

for minp, maxp in tests:
    count = get_results_count(minp, maxp)
    print(f"Test {minp} - {maxp} → {count} résultats")


#_________________________________________________


    def adjust_range(
        self, min_max: dict[str: int], increase: bool) -> dict[str: int]:
        # adjust_range({"minprice": n, "maxprice: m"}, True/False)
        if increase and self._prev_adj["increase"]:
            self._prev_adj["num"] *= 2
            min_max["maxprice"] += self._prev_adj["num"]
        elif not increase and self._prev_adj["increase"]:
            self._prev_adj["increase"] = False
            self._prev_adj["num"] //= 2
            min_max["maxprice"] -= self._prev_adj["num"]
        elif increase and not self._prev_adj["increase"]:
            self._prev_adj["increase"] = True
            self._prev_adj["num"] //= 2
            min_max["maxprice"] += self._prev_adj["num"]
        elif not increase and not self._prev_adj["increase"]:
            min_max["maxprice"] -= self._prev_adj["num"]
        return min_max

    def append_range(self, minprice: int, maxprice: int, results_amount: int):
        self.ranges.append(
            {
                "minprice": minprice,
                "maxprice": maxprice,
                "results_amount": results_amount
            }
        )

    def fill_ranges(self):
        """
        Method creates all ranges from lowest price to highest
        It creates range
        checks it with check_range()
        adjust_range() if needed
        append_range when OK.
        """
        min_max = {"minprice": 1, "maxprice": 100000}
        if self.ranges != []:
            min_max["minprice"] = self.ranges[-1]["maxprice"] + 1
        while True:
            amount = self.check_range(min_max["minprice"], min_max["maxprice"])
            if amount > 800 and amount < 1000:
                append_range(min_max["minprice"], min_max["maxprice"], amount)
                break
            elif amount < 800:
                min_max = adjust_range({
                    "minprice": min,
                    "maxprice": max
                }, True)
            elif amount > 1000:
                min_max = adjust_range({
                    "minprice": min,
                    "maxprice": max
                }, False)

#_______________________________________________________
def get_results_count(minprice, maxprice):
    # Construire l'URL avec les paramètres de prix
    url = (
        "https://www.immovlan.be/en/real-estate"
        "?transactiontypes=for-sale"
        "&propertytypes=house,apartment"
        f"&minprice={minprice}"
        f"&maxprice={maxprice}"
    )

    # Envoyer la requête HTTP
    response = requests.get(url)

    # Vérifier si la page a bien été chargée
    if response.status_code != 200:
        return 0

    # Parser le HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Récupérer tout le texte visible
    text = soup.get_text(separator=" ").lower()

    # Chercher une phrase du type "xxx results"
    match = re.search(r"(\d+)\s+results", text)

    if match:
        return int(match.group(1))
    else:
        return 0

# Coeur du Proframme
price_ranges = []

minprice = 0
MAX_PRICE = 2000000
STEP = 50000

while minprice < MAX_PRICE:
    maxprice = minprice + STEP

    results = get_results_count(minprice, maxprice)
    print(f"Test {minprice} - {maxprice} → {results} résultats")

    if 800 <= results <= 1000:
        price_ranges.append({
            "minprice": minprice,
            "maxprice": maxprice,
            "results": results
        })
        minprice = maxprice + 1
    else:
        maxprice += STEP
        minprice = maxprice


print("\nRÉSULTATS FINAUX :")
for r in price_ranges:
    print(r)

    import requests
from bs4 import BeautifulSoup
import re


def get_results_count(minprice, maxprice):
    url = (
        "https://immovlan.be/en/real-estate"
        "?transactiontypes=for-sale"
        "&propertytypes=house,apartment"
        f"&minprice={minprice}"
        f"&maxprice={maxprice}"
        "&noindex=1"
    )

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    search_results = soup.find("section", id="search-results")
    if search_results is None:
        return 0

    results_div = search_results.find("div", class_="col-12 mb-2")
    if results_div is None:
        return 0

    text = results_div.get_text(separator=" ", strip=True).lower()
    match = re.search(r"(\d+)\s+results", text)

    if match:
        return int(match.group(1))

    return 0


tests = [
    (1, 100000),
    (100000, 200000),
    (200000, 300000),
]

for minp, maxp in tests:
    count = get_results_count(minp, maxp)
    print(f"Test {minp} - {maxp} → {count} résultats")