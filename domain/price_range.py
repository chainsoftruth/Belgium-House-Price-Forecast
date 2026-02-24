class PriceRanges():

    def init(self):
        self._step = .1

    def check_range(self, minprice: int, maxprice: int) -> bool:
        pass

    def adjust_range(self, min_max: list[int], increase: bool) -> list[int]:


    def append_ranges(self, minprice: int, maxprice: int, results_amount: int):
        pass


import requests
from bs4 import BeautifulSoup
import re

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