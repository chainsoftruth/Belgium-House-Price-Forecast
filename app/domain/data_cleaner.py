from unidecode import unidecode
import pandas as pd
import numpy as np
import math
import json

class DataCleaner():

    @staticmethod
    def check(data: pd.DataFrame):
        print("------DataFrame check------")
        print("Records count: ", data.shape[0], sep = '')
        print(data.head(10))
    
    @staticmethod
    def get_distance(dist: pd.DataFrame, code: str) -> float:
        dist["postcode"] = dist["postcode"].astype("string")
        return dist[dist.postcode == code]["distance"].iloc[0]

    @staticmethod
    def get_state_code(state: str) -> int:
        state = state.lower()
        match state:
            case "to rebuild":
                return 0
            case "to renovate" | "to be renovated":
                return 1
            case "normal" | "good": 
                return 2
            case "fully renovated":
                return 3
            case "excellent" | "new":
                return 4
    
    @staticmethod
    def get_subtype_code(subtype: str) -> int:
        subtypes = json.load(open("app/data/external/subtypes.json"))
        return subtypes[subtype]

    @staticmethod
    def optimize(data: pd.DataFrame) -> pd.DataFrame:
        dist = pd.read_csv("app/data/external/cords.csv")
        data = data.replace([0, "To demolish", "Under construction", "To restore"], np.nan)
        condition = data["Type of property"] == "apartment"
        sublist = ["Surface of the land"]
        data.loc[condition, sublist] = data.loc[condition, sublist].fillna(0)
        data = data.drop(["Number of rooms", "Garden Area", "Terrace Area"], axis = 1)
        data = data.rename(columns = {
            "Post code": "postcode",
            "Type of property": "type",
            "Subtype of property":"subtype",
            "Price": "price",
            "Living Area": "living_area",
            "Terrace": "terrace",
            "Garden": "garden",
            "Surface of the land": "land_area",
            "Number of facades": "facades",
            "State of the building": "state",
            "Furnished": "furnished",
            "Swimming pool": "pool"
        })
        data = data.dropna(subset = data.columns.drop(["state", "facades"]))
        data["postcode"] = data["postcode"].apply(lambda x: DataCleaner.get_distance(dist, x))
        data = data.rename(columns = {"postcode" : "distance"})
        data["subtype"] = data["subtype"].apply(get_state_code)
        data = data[
            (data.living_area != 1) &
            (data.living_area != data.land_area)
        ]
        data = DataCleaner.trim_edges(data, 0.0025, 0.0025)
        data = data.sort_values("price")
        data = data.reset_index(drop = True)
        dropped_values = data[(data.state.isna())|(data.facades.isna())]
        data = data.dropna()
        print("Optimizer: FINISHED")
        return data, dropped_values

    @staticmethod
    def trim_edges(data: pd.DataFrame, start_prs: float, end_prs: float) -> pd.DataFrame:
        if data is None or data.empty:
            print("ERROR TRIMMING: No data provided.")
            return data
        total_rows = len(data)
        trim_start = math.floor(total_rows * start_prs)
        trim_end = math.floor(total_rows * end_prs)
        if total_rows <= trim_start + trim_end:
            print("ERROR TRIMMING: Dataset is too small to trim values.")
            return data
        
        data = pd.concat([
            data[data.type == "apartment"].sort_values("price").iloc[
            trim_start : total_rows - trim_end, :],
            data[data.type == "house"].sort_values("price").iloc[
            trim_start : total_rows - trim_end, :]
        ])
        data = pd.concat([
            data[data.type == "apartment"].sort_values("living_area").iloc[
            trim_start : total_rows - trim_end, :],
            data[data.type == "house"].sort_values("living_area").iloc[
            trim_start : total_rows - trim_end, :]
        ])
        data = pd.concat([
            data[data.type == "apartment"],
            data[data.type == "house"].sort_values("land_area").iloc[
                trim_start : total_rows - trim_end, :]
        ])
        print(f"Trimming: OK. {total_rows - len(data)} rows removed.")
        return data