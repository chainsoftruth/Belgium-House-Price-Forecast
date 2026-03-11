from unidecode import unidecode
import pandas as pd
import numpy as np
import math

class DataCleaner():

    @staticmethod
    def check(data: pd.DataFrame):
        print("------DataFrame check------")
        print("Records count: ", data.shape[0], sep = '')
        print(data.head(10))
    
    @staticmethod
    def optimize(data: pd.DataFrame) -> pd.DataFrame:
        dist = pd.read_csv("data/external/cords.csv")
        dist["postcode"] = dist["postcode"].astype("string")
        data = data.replace([0, "To demolish", "Under construction", "To restore"], np.nan)
        condition = data["Type of property"] == "apartment"
        sublist = ["Surface of the land"]
        data.loc[condition, sublist] = data.loc[condition, sublist].fillna(0)
        data = data.drop(["Number of rooms", "Garden Area", "Terrace Area"], axis = 1)
        data = data.dropna()
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
        data = data.merge(dist[["postcode", "distance"]], on = "postcode", how = "left")
        data = data.drop("postcode", axis = 1)
        data = data.replace({
            "To renovate": 2,
            "To be renovated": 2,
            "Normal": 4,
            "Fully renovated": 6,
            "Excellent": 8,
            "New": 8
        })
        data = data[
            (data.living_area != 1) &
            (data.living_area != data.land_area)
        ]
        data.price = (data.price / data.living_area) // 1
        data = data.rename(columns={
            "price":"price_m2"
        })
        data = data.reset_index(drop = True)
        data = DataCleaner.trim_edges(data, 0.005, 0.005)
        data = data.sort_values("price_m2")
        data = data.reset_index(drop = True)
        print("Optimizer: FINISHED")
        return data

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
        data = data.sort_values("price_m2").iloc[
            trim_start : total_rows - trim_end, :]
        data = data.sort_values("living_area").iloc[
            trim_start : total_rows - trim_end, :]
        data = pd.concat([
            data[data.type == "apartment"],
            data[data.type == "house"].sort_values("land_area").iloc[
                trim_start : total_rows - trim_end, :]
        ])
        print(f"Trimming: OK. {total_rows - len(data)} rows removed.")
        return data