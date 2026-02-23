import requests
from bs4 import BeautifulSoup
import re
class PropertyScraper:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.data = {}
        self.scrape()

    def scrape(self):
        print(f"Scraping data from {self.url}...")
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        response = requests.get(self.url, headers=headers)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.extract_locality()
        print("Scraping completed.")

    def extract_locality(self):
            elem = self.soup.select_one('span.detail__header_title_main span.d-none.d-lg-inline')
    
            if elem:
                raw_text = elem.get_text(strip=True)
                cleaned_text = re.sub(r'^-\s+', '', raw_text)
                self.data['Locality'] = cleaned_text
                print(f"  Found locality: {self.data['Locality']}")




url = "https://immovlan.be/en/detail/apartment/for-sale/1081/koekelberg/vbd48962"
scraper = PropertyScraper(url)

# Print the result
print(f"Data dictionary: {scraper.data}")