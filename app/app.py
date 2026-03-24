from fastapi import FastAPI
from pydantic import BaseModel, Field
import pandas as pd
import joblib
from enum import Enum
from typing import Optional

from app.domain.data_cleaner import DataCleaner

class PropertyType(str, Enum):
    APARTMENT = "APARTMENT"
    HOUSE = "HOUSE"

class PropertySubtype(str, Enum):
    STUDIO = "STUDIO"
    CHALET = "CHALET"
    GROUND_FLOOR = "GROUND-FLOOR"
    APARTMENT = "APARTMENT"
    BUNGALOW = "BUNGALOW"
    TRIPLEX = "TRIPLEX"
    DUPLEX = "DUPLEX"
    RESIDENCE = "RESIDENCE"
    MIXED_BUILDING = "MIXED-BUILDING"
    LOFT = "LOFT"
    COTTAGE = "COTTAGE"
    PENTHOUSE = "PENTHOUSE"
    MASTER_HOUSE = "MASTER-HOUSE"
    VILLA = "VILLA"
    MANSION = "MANSION"

class PropertyState(str, Enum):
    NEW = "NEW"
    GOOD = "GOOD"
    TO_RENOVATE = "TO RENOVATE"
    JUST_RENOVATED = "JUST RENOVATED"
    TO_REBUILD = "TO REBUILD"
    EXCELLENT = "EXCELLENT"

class PropertyData(BaseModel):
    area: int
    property_type : PropertyType = Field(alias = "property-type")
    property_subtype : PropertySubtype = Field(alias = "property-subtype")
    rooms_number : Optional[int] = Field(alias = "rooms-number")
    zip_code : int = Field(alias = "zip-code")
    land_area : Optional[int] = Field(default = 0, alias = "land-area")
    garden : bool
    garden_area : Optional[int] = Field(alias = "garden-area")
    equipped_kitchen : Optional[bool] = Field(alias = "equipped-kitchen")
    full_address : Optional[str] = Field(alias = "full-address")
    swimming_pool : bool = Field(alias = "swimming-pool")
    furnished : bool
    open_fire : Optional[bool] = Field(alias = "open-fire")
    terrace : bool
    terrace_area : Optional[int] = Field(alias = "terrace-area")
    facades_number : int = Field(alias = "facades-number")
    building_state : PropertyState = Field(alias = "building-state")
    
    class Config:
        extra = "forbid"

class PropertyInput(BaseModel):
    data: PropertyData

h_model = joblib.load("h_regressorion.joblib")
ap_model = joblib.load("ap_regressorion.joblib")

app = FastAPI(title="Belgium House Price Prediction")

@app.get("/")
def root():
    return "alive"

@app.get("/predict")
def predict_get():
    return {
        "info": "Send a POST request with JSON like: { 'data': { 'area': int, 'property-type': 'HOUSE' or 'APARTMENT', ... } }",
        "output": { "prediction": "float", "status_code": "int" }
    }

def prepare_features(value: PropertyData) -> pd.DataFrame:
    X = pd.DataFrame([{
        "subtype": DataCleaner.get_subtype_code(value.property_subtype.value.lower()),  # use subtype now
        "living_area": value.area,
        "land_area": value.land_area or 0,
        "facades": value.facades_number or 0,
        "state": DataCleaner.get_state_code(value.building_state.value) if value.building_state else 0,
        "furnished": int(value.furnished),
        "terrace": int(value.terrace),
        "garden": int(value.garden),
        "pool": int(value.swimming_pool),
        "distance": DataCleaner.get_distance(
            pd.read_csv("app/data/external/cords.csv"), str(value.zip_code)
        )
    }])
    return X

@app.post("/predict")
def predict_price(property_input: PropertyInput):
    value = property_input.data
    X = prepare_features(value)

    # Remove land_area column for apartments
    if value.property_type == PropertyType.APARTMENT:
        if "land_area" in X.columns:
            X = X.drop(columns=["land_area"])

    # Select model
    property_type = value.property_type.lower()
    if property_type == "house":
        scaler = h_model["scaler"]
        model = h_model["model"]
    elif property_type == "apartment":
        scaler = ap_model["scaler"]
        model = ap_model["model"]
    else:
        return {"prediction": None, "status_code": 400}

    # Scale & predict
    X_scaled = scaler.transform(X)
    prediction = model.predict(X_scaled)

    return {"prediction": prediction.tolist()[0], "status_code": 200}