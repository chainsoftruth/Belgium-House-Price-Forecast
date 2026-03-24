from app.data.manager import DataManager
from app.data.property_model import *
from app.domain.links import Links
from app.domain.scraper import PropertyScraper
from app.domain.data_cleaner import DataCleaner
from app.domain.regressor import Regressor
from app.domain.classifier import Classifier

from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from fastapi import FastAPI, HTTPException
import requests
import pandas as pd

# -------------------------------
# CREATE FASTAPI APP
# -------------------------------

app = FastAPI()

# -------------------------------
# TRAIN MODEL ON STARTUP
# -------------------------------

print("Loading dataset and training model...")

df = DataManager.csv_import("clean_dataset")

regressor = Regressor(df)
regressor.set_gradientboosting()

# Store trained models and scalers
h_model = regressor.h_model
h_scaler = regressor.h_scaler

ap_model = regressor.ap_model
ap_scaler = regressor.ap_scaler

print("Models ready ✅")

# -------------------------------
# SCRAPING FUNCTIONS (OPTIONAL)
# -------------------------------

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

# -------------------------------
# DATA CLEANING
# -------------------------------

def clear_data() -> pd.DataFrame:
    data = DataManager.raw_data_csv_import("raw_dataset")
    clean_data, dropped_data = DataCleaner.optimize(data)
    DataManager.dataframe_csv_export(clean_data, "clean_dataset")
    DataManager.dataframe_csv_export(dropped_data, "dropped_data")
    DataCleaner.check(clean_data)

# -------------------------------
# FEATURE ENGINEERING
# -------------------------------

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
            pd.read_csv("app/data/external/cords.csv"),
            str(value.zip_code)
        )
    ]).to_frame().T

    X.columns = [
        'subtype', 'living_area', 'land_area', 'facades', 'state',
        'furnished', 'terrace', 'garden', 'pool', 'distance'
    ]

    return X

# -------------------------------
# PREDICTION LOGIC
# -------------------------------

def predict_price(df: pd.DataFrame, property_type: str) -> float:

    if property_type == "HOUSE":
        X_scaled = h_scaler.transform(df)
        prediction = h_model.predict(X_scaled)[0]

    else:
        # Apartments do not use land_area
        df = df.drop("land_area", axis=1, errors="ignore")
        X_scaled = ap_scaler.transform(df)
        prediction = ap_model.predict(X_scaled)[0]

    return prediction

# -------------------------------
# API ROUTES
# -------------------------------

@app.get("/")
def root():
    return {"status": "alive"}

@app.get("/predict")
def predict_info():
    return {
        "message": "Send a POST request with property data in JSON format"
    }

@app.post("/predict")
def predict_endpoint(request: PropertyRequest):
    try:
        df = _extract_data(request)
        property_type = request.data.property_type
        price = predict_price(df, property_type)

        return {
            "prediction": float(price),
            "status_code": 200
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

print("RUNNING FILE: app/main.py")
