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
        data = data.replace([0, "To demolish", "Under construction", "To restore"], np.nan)
        condition = data["Type of property"] == "apartment"
        sublist = ["Surface of the land"]
        data.loc[condition, sublist] = data.loc[condition, sublist].fillna(0)
        data = data.drop(["Number of rooms", "Garden Area", "Terrace Area"], axis = 1)
        data = data.dropna()
        data = data.rename(columns = {
            "Post code": "code",
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
        data = DataCleaner.adjust_locality(data)
        data = DataCleaner.trim_edges(data, 0.005, 0.005)
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
        data = pd.concat(
            data[data.type == "appartment"],
            data[data.type == "house"].sort_values("land_area").iloc[
                trim_start : total_rows - trim_end, :]
        )
        print(f"Trimming: OK. {(trim_start + trim_end) * 3} rows removed.")
        return trimmed_data

    @staticmethod
    def adjust_locality(data: pd.DataFrame) -> pd.DataFrame:
        code_list = pd.read_csv("./data/external/postal_codes.csv")
        code_list.code = code_list.code.astype(str)
        with open("./data/raw/links.txt", "r", encoding="utf-8") as f:
            links = f.read()
            f.close()
        links = links.split('\n')
        codes = []
        names = []
        for line in links:
            codes.append(line.split("/")[7])
            names.append(line.split("/")[8])
        raw_data = {"code": codes, "locality": names}
        df = pd.DataFrame(raw_data)
        df = df.drop_duplicates("locality").reset_index(drop = True)
        data.locality = data.locality.apply(
            lambda x: 
            unidecode(x.lower().replace(" ", "-").replace("'", "-")))
        data.insert(0, "index", data.index)
        data = data.merge(df, how="left", on="locality")
        data = data.merge(code_list, how="left", on="code")
        data = data.drop(["locality", "code"], axis = 1)
        return data