import requests
from bs4 import BeautifulSoup
import re

class PropertyScraper:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
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
            'Number of facades': None,
            'State of the building': None,
            
            # Boolean fields (default 0 = No)
            'Furnished': 0,
            'Terrace': 0,
            'Garden': 0,
            'Swimming pool': 0
        }
        self.scrape()

    def scrape(self):
        print(f"Scraping data from {self.url}...")
        response = self.session.get(self.url)
        response.raise_for_status()
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.extract_locality()
        self.extract_property_subtype()
        self.extract_property_type(self.data['Subtype of property'])
        self.extract_price()
        self.extract_sale_type()
        self.extract_number_of_rooms()
        self.extract_living_area()
        self.extract_surface_of_the_land()
        self.extract_terrace()
        self.extract_garden()
        self.extract_number_of_facades()
        self.extract_state_of_the_building()
        self.extract_furnished()  
        self.extract_swimming_pool()
        return self.data 
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
        rows = self.soup.select("div.data-row-wrapper > div")

        for row in rows:
            title = row.select_one("h4")
            if title and "Number of bedrooms" in title.get_text():
                value = row.select_one("p")
                raw_text = value.get_text(strip=True)
                clean_text = re.sub(r'[^\d]', '', raw_text)
                self.data["Number of rooms"] = int(clean_text) if clean_text else None
                print(f"Found number of rooms: {self.data['Number of rooms']}")


    def extract_living_area(self):
        rows = self.soup.select("div.data-row-wrapper > div")

        for row in rows:
            title = row.select_one("h4")
            if title and "Livable surface" in title.get_text():
                value = row.select_one("p")
                raw_text = value.get_text(strip=True)
                clean_text = re.sub(r'[^\d]', '', raw_text)
                self.data["Living Area"] = int(clean_text) if clean_text else None
                print(f"Found living area: {self.data['Living Area']}")


    def extract_surface_of_the_land(self):
        rows = self.soup.select("div.data-row-wrapper > div")

        for row in rows:
            title = row.select_one("h4")
            if title and "Total land surface" in title.get_text():
                value = row.select_one("p")
                raw_text = value.get_text(strip=True)
                clean_text = re.sub(r'[^\d]', '', raw_text)
                self.data["Surface of the land"] = int(clean_text) if clean_text else None
                print(f"Found surface of the land: {self.data['Surface of the land']}")


    def extract_number_of_facades(self):
        rows = self.soup.select("div.data-row-wrapper > div")

        for row in rows:
            title = row.select_one("h4")
            if title and "Number of facades" in title.get_text():
                value = row.select_one("p")
                raw_text = value.get_text(strip=True)
                clean_text = re.sub(r'[^\d]', '', raw_text)
                self.data["Number of facades"] = int(clean_text) if clean_text else None
                print(f"Found number of facades: {self.data['Number of facades']}")


    def extract_terrace(self):
        rows = self.soup.select("div.data-row-wrapper > div")

        for row in rows:
            title = row.select_one("h4")
            if title and "Terrace" in title.get_text():
                value = row.select_one("p")
                raw_text = value.get_text(strip=True)
                if raw_text.lower() == "yes":
                    self.data["Terrace"] = 1
            title2 = row.select_one("h4")
            if title2 and "Surface terrace" in title2.get_text():
                value2 = row.select_one("p")
                raw_text2 = value2.get_text(strip=True)
                clean_text = re.sub(r'[^\d]', '', raw_text2)
                self.data["Terrace Area"] = int(clean_text) if clean_text else None
                print(f"Found terrace area: {self.data['Terrace Area']}")
                

    def extract_garden(self):
        rows = self.soup.select("div.data-row-wrapper > div")

        for row in rows:
            title = row.select_one("h4")
            if title and "Garden" in title.get_text():
                value = row.select_one("p")
                raw_text = value.get_text(strip=True)
                if raw_text.lower() == "yes":
                    self.data["Garden"] = 1
            title2 = row.select_one("h4")
            if title2 and "Surface garden" in title2.get_text():
                value2 = row.select_one("p")
                raw_text2 = value2.get_text(strip=True)
                clean_text = re.sub(r'[^\d]', '', raw_text2)
                self.data["Garden Area"] = int(clean_text) if clean_text else None
                print(f"Found garden area: {self.data['Garden Area']}")


    def extract_state_of_the_building(self):
        rows = self.soup.select("div.data-row-wrapper > div")

        for row in rows:
            title = row.select_one("h4")
            if title and "State of the property" in title.get_text():
                value = row.select_one("p")
                raw_text = value.get_text(strip=True)
                self.data["State of the building"] = raw_text if raw_text else None
                print(f"Found state of the building: {self.data['State of the building']}")


    def extract_furnished(self):
        rows = self.soup.select("div.data-row-wrapper > div")

        for row in rows:
            title = row.select_one("h4")
            if title and "Furnished" in title.get_text():
                    value = row.select_one("p")
                    raw_text = value.get_text(strip=True)
                    if raw_text.lower() == "yes":
                        self.data["Furnished"] = 1


    def extract_swimming_pool(self):
        rows = self.soup.select("div.data-row-wrapper > div")

        for row in rows:
            title = row.select_one("h4")
            if title and "Swimming pool" in title.get_text():
                    value = row.select_one("p")
                    raw_text = value.get_text(strip=True)
                    if raw_text.lower() == "yes":
                        self.data["Swimming pool"] = 1



# url = "https://immovlan.be/en/detail/apartment/for-sale/1081/koekelberg/vbd48962"
# url = "https://immovlan.be/en/detail/residence/for-sale/1180/ukkel/vbd21625"
# url = "https://immovlan.be/en/detail/ground-floor/for-sale/1030/schaarbeek/vbd13483"
# url = "https://immovlan.be/en/detail/apartment/for-sale/1080/sint-jans-molenbeek/vbd65143"
# url = "https://immovlan.be/en/detail/studio/for-sale/1000/brussels/vbd48521"
# url = "https://immovlan.be/en/detail/villa/for-sale/1170/watermaal-bosvoorde/vbd82581"
# url = "https://immovlan.be/en/detail/apartment/for-sale/8670/koksijde/rbv12584"
# url = "https://immovlan.be/en/detail/apartment/for-sale/8370/blankenberge/rbu86234"

# scraper = PropertyScraper(url)
# # Print the result
# print(f"Data locality: {scraper.data['Locality']}")
# print(f"Data property subtype: {scraper.data['Subtype of property']}")
# print(f"Data property type: {scraper.data['Type of property']}")
# print(f"Data price: {scraper.data['Price']}")
# print(f"Data sale type: {scraper.data['Type of sale']}")
# print(f"Data number of rooms: {scraper.data['Number of rooms']}")
# print(f"Data living area: {scraper.data['Living Area']}")
# print(f"Data surface of the land: {scraper.data['Surface of the land']}")
# print(f"Data terrace: {scraper.data['Terrace']}")
# print(f"Data terrace area: {scraper.data['Terrace Area']}")
# print(f"Data garden: {scraper.data['Garden']}")
# print(f"Data garden area: {scraper.data['Garden Area']}")
# print(f"Data number of facades: {scraper.data['Number of facades']}")
# print(f"Data state of the building: {scraper.data['State of the building']}")   
# print(f"Data furnished: {scraper.data['Furnished']}")
# print(f"Data swimming pool: {scraper.data['Swimming pool']}")
# print(scraper.data)