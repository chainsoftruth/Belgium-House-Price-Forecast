from app.data.manager import DataManager
from app.data.property_model import *
from app.domain.links import Links
from app.domain.scraper import PropertyScraper
from app.domain.data_cleaner import DataCleaner
from app.domain.regressor import Regressor
from app.domain.classifier import Classifier

from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from fastapi import FastAPI
from fastapi.responses import FileResponse
import requests
import pandas as pd
import joblib

def update_links() -> list[str]:
    links = Links()
    print("SCRAPING...")
    links_list = links.scrape()
    print("SCRAPED: OK")
    DataManager.links_export(links_list)
    return links_list

def _scrape_property(link):
    try:
        scraper = PropertyScraper(link) 
        return scraper.scrape()
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        if status in (404, 410):
            print(f"Skipping {status} page: {link}")
            return None
        else:
            raise
    except Exception as e:
        print(f"Error scraping {link}: {e}")
        return None

def update_dataset():
    links = DataManager.links_import()
    data_list = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(_scrape_property, link) for link in links]
        for future in tqdm(as_completed(futures), total=len(futures)):
            data = future.result()
            if data is not None:
                data_list.append(data)
    DataManager.data_csv_export(data_list, "raw_dataset")
    
def clear_data() -> pd.DataFrame:
    data = DataManager.raw_data_csv_import("raw_dataset")
    clean_data, dropped_data = DataCleaner.optimize(data)
    DataManager.dataframe_csv_export(clean_data, "clean_dataset")
    DataManager.dataframe_csv_export(dropped_data, "dropped_data")
    DataCleaner.check(clean_data)

def classify_facadesNstate():
    data = DataManager.csv_import("clean_dataset")
    classifier = Classifier(data)
    classifier.set_randomforest()
    dropped_data = DataManager.csv_import("dropped_data")
    facades, state = classifier.predict(dropped_data)
    dropped_data["facades"] = facades
    dropped_data["state"] = state
    print(dropped_data.head(50))
    print(dropped_data.shape)

def train_regression():
    data = DataManager.csv_import("clean_dataset")
    regressor = Regressor(data)
    regressor.set_gradientboosting()
    # Can create model files here

def _extract_data(value: PropertyRequest) -> pd.DataFrame:
    value = value.data
    X = pd.Series([
        DataCleaner.get_subtype_code(value.property_subtype.lower()),
        value.area,
        value.land_area,
        value.facades_number,
        DataCleaner.get_state_code(value.building_state),
        value.furnished,
        value.terrace,
        value.garden,
        value.swimming_pool,
        DataCleaner.get_distance(
            pd.read_csv("app/data/external/cords.csv"), str(value.zip_code))
    ]).to_frame().T
    X.columns = ['subtype', 'living_area', 'land_area', 'facades', 'state', 
        'furnished', 'terrace', 'garden', 'pool', 'distance']
    return X

print("RUNNING FILE: app/main.py")