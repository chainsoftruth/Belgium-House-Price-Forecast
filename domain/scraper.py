import requests
from bs4 import BeautifulSoup
import re
class PropertyScraper:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.data = {
            # Non-boolean fields (default None)
            'Locality': None,
            'Type of property': None,
            'Subtype of property': None,
            'Price': None,
            'Type of sale': "Normal sale",
            'Number of rooms': None,
            'Living Area': None,
            'Terrace Area': None,
            'Garden Area': None,
            'Surface of the land': None,
            'Surface area of the plot of land': None,
            'Number of facades': None,
            'State of the building': None,
            
            # Boolean fields (default 0 = No)
            'Fully equipped kitchen': 0,
            'Furnished': 0,
            'Open fire': 0,
            'Terrace': 0,
            'Garden': 0,
            'Swimming pool': 0
        }
        self.scrape()

    def scrape(self):
        print(f"Scraping data from {self.url}...")
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        response = requests.get(self.url, headers=headers)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.extract_locality()
        self.extract_property_subtype()
        self.extract_property_type(self.data['Subtype of property'])
        self.extract_price()
        self.extract_sale_type()
        self.extract_number_of_rooms()
        print("Scraping completed.")


    def extract_locality(self):
        elem = self.soup.select_one('span.detail__header_title_main span.d-none.d-lg-inline')
        if elem:
            raw_text = elem.get_text(strip=True)
            cleaned_text = re.sub(r'^-\s+', '', raw_text)
            self.data['Locality'] = cleaned_text
            print(f"  Found locality: {self.data['Locality']}")


    def extract_property_subtype(self):
        match = re.search(r'/detail/([^/]+)/', self.url)
        if match:
                self.data['Subtype of property'] = match.group(1)
                print(f"  Found property subtype from URL: {self.data['Subtype of property']}")

    def extract_property_type(self, subtype):
        house_subtypes = [
        'residence', 'villa', 'bungalow', 'chalet', 'cottage',
        'master-house', 'mansion', 'mixed-buildings', 'house'
        ]
    
        apartment_subtypes = [
        'apartment', 'ground-floor', 'penthouse', 'duplex',
        'triplex', 'studio', 'loft'
        ]

        if subtype in house_subtypes:
            self.data['Type of property'] = "house"
        elif subtype in apartment_subtypes:
            self.data['Type of property'] = "apartment"
        else:
            self.data['Type of property'] = "unknown"

    def extract_price(self):
        elem = self.soup.select_one('span.detail__header_price_data')
        if elem:
            text = elem.get_text(strip=True)
            clean_text = re.sub(r'[^\d]', '', text)
            if clean_text:
                self.data['Price'] = int(clean_text)
            else:
                self.data['Price'] = "None"
            print(f"  Found price: {self.data['Price']}")

    def extract_sale_type(self):
        financial = self.soup.find('div', class_='financial')

        list_items = financial.find_all('li')
    
        # Life sale indicators (if ANY of these exist, it's a life sale)
        life_sale_indicators = [
            'monthly annuity',
            'number of sellers',
            'indexed pension',
            'maximal duration of annuity',
            'age 1st annuitant',
            'age 2nd annuitant',
        ]
    

        for li in list_items:
            li_text = li.get_text(strip=True).lower()
            
            for indicator in life_sale_indicators:
                if indicator in li_text:
                    self.data['Type of sale'] = 'Life sale'
                    break

    def extract_number_of_rooms(self):
        elem = self.soup.select_one('div.data-row-wrapper:has(h4:contains("Number of bedrooms")) p')
        if elem:
            raw_text = elem.get_text(strip=True)
            print(f"  Raw number of rooms text: '{raw_text}'")
            clean_text = re.sub(r'[^\d]', '', raw_text)
            if clean_text:
                self.data['Number of rooms'] = int(clean_text)
            else:
                self.data['Number of rooms'] = "None"
            print(f"  Found number of rooms: {self.data['Number of rooms']}")




# url = "https://immovlan.be/en/detail/apartment/for-sale/1081/koekelberg/vbd48962"
url = "https://immovlan.be/en/detail/residence/for-sale/1180/ukkel/vbd21625"
# url = "https://immovlan.be/en/detail/ground-floor/for-sale/1030/schaarbeek/vbd13483"
# url = "https://immovlan.be/en/detail/apartment/for-sale/1080/sint-jans-molenbeek/vbd65143"
scraper = PropertyScraper(url)

# Print the result
print(f"Data locality: {scraper.data['Locality']}")
print(f"Data property subtype: {scraper.data['Subtype of property']}")
print(f"Data property type: {scraper.data['Type of property']}")
print(f"Data price: {scraper.data['Price']}")
print(f"Data sale type: {scraper.data['Type of sale']}")
print(f"Data number of rooms: {scraper.data['Number of rooms']}")