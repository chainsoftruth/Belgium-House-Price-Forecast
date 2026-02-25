from turtle import delay

import requests
from bs4 import BeautifulSoup
import re
import time
import random

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

    def scrape(self):
        delay = random.uniform(1, 2.5)
        time.sleep(delay)
        response = self.session.get(self.url)
        if "/detail/" not in response.url:
            print(f"Redirected to search page: {response.url} - skipping {self.url}")
            return None
        response.raise_for_status()
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.extract_locality()
        self.extract_property_subtype()
        self.extract_property_type(self.data['Subtype of property'])
        self.extract_price()
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


    def extract_locality(self):
        elem = self.soup.select_one('span.detail__header_title_main span.d-none.d-lg-inline')
        if elem:
            raw_text = elem.get_text(strip=True)
            cleaned_text = re.sub(r'^-\s+', '', raw_text)
            self.data['Locality'] = cleaned_text


    def extract_property_subtype(self):
        match = re.search(r'/detail/([^/]+)/', self.url)
        if match:
                self.data['Subtype of property'] = match.group(1)


    def extract_property_type(self, subtype):
        house_subtypes = [
        'residence', 'villa', 'bungalow', 'chalet', 'cottage',
        'master-house', 'mansion', 'mixed-building', 'house'
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
            self.data['Type of property'] = None

    def extract_price(self):
        elem = self.soup.select_one('span.detail__header_price_data')
        if elem:
            text = elem.get_text(strip=True)
            clean_text = re.sub(r'[^\d]', '', text)
            if clean_text:
                self.data['Price'] = int(clean_text)
            else:
                self.data['Price'] = "None"


    def extract_number_of_rooms(self):
        rows = self.soup.select("div.data-row-wrapper > div")

        for row in rows:
            title = row.select_one("h4")
            if title and "Number of bedrooms" in title.get_text():
                value = row.select_one("p")
                raw_text = value.get_text(strip=True)
                clean_text = re.sub(r'[^\d]', '', raw_text)
                self.data["Number of rooms"] = int(clean_text) if clean_text else None


    def extract_living_area(self):
        rows = self.soup.select("div.data-row-wrapper > div")

        for row in rows:
            title = row.select_one("h4")
            if title and "Livable surface" in title.get_text():
                value = row.select_one("p")
                raw_text = value.get_text(strip=True)
                clean_text = re.sub(r'[^\d]', '', raw_text)
                self.data["Living Area"] = int(clean_text) if clean_text else None


    def extract_surface_of_the_land(self):
        rows = self.soup.select("div.data-row-wrapper > div")

        for row in rows:
            title = row.select_one("h4")
            if title and "Total land surface" in title.get_text():
                value = row.select_one("p")
                raw_text = value.get_text(strip=True)
                clean_text = re.sub(r'[^\d]', '', raw_text)
                self.data["Surface of the land"] = int(clean_text) if clean_text else None


    def extract_number_of_facades(self):
        rows = self.soup.select("div.data-row-wrapper > div")

        for row in rows:
            title = row.select_one("h4")
            if title and "Number of facades" in title.get_text():
                value = row.select_one("p")
                raw_text = value.get_text(strip=True)
                clean_text = re.sub(r'[^\d]', '', raw_text)
                self.data["Number of facades"] = int(clean_text) if clean_text else None


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


    def extract_state_of_the_building(self):
        rows = self.soup.select("div.data-row-wrapper > div")

        for row in rows:
            title = row.select_one("h4")
            if title and "State of the property" in title.get_text():
                value = row.select_one("p")
                raw_text = value.get_text(strip=True)
                self.data["State of the building"] = raw_text if raw_text else None


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