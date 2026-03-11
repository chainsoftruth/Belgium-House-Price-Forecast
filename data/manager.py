from datetime import datetime
import pandas as pd
import numpy as np
import csv

class DataManager():

    @staticmethod
    def links_export(links: list[str]):
        """Exporting links to .txt"""
        with open("./data/raw/links.txt", "w") as file:
            for link in links:
                file.write(f"{link}\n")
        print("links.txt updated.")
    
    @staticmethod
    def links_import() -> list[str]:
        """Importing links from .txt"""
        with open("./data/raw/links.txt", "r") as file:
            lines = [line.strip() for line in file if line.strip()]
        print("Links import: OK")
        return lines

    @staticmethod
    def data_csv_export(data: list[dict[str: any]], filename: str):
        """Exporting data list (list of dicts) into .csv"""
        date_str = datetime.now().strftime("%d-%m-%Y")
        file_name = f"./data/raw/{filename}_{date_str}.csv"
        columns = list(data[0].keys())
        file = open(file_name, "w", newline="", encoding="utf-8")
        writer = csv.DictWriter(file, columns)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        file.close()
        print("CSV updated.")

    @staticmethod
    def dataframe_csv_export(data: pd.DataFrame, filename: str):
        """Export cleaned pandas DataFrame into ./data/{filename}.csv"""
        if data is None or data.empty:
            print("No data to export.")
            return
        file_name = f"./data/{filename}.csv"
        data.to_csv(file_name, index=False)
        print("DataFrame export: OK")

    @staticmethod
    def raw_data_csv_import() -> pd.DataFrame:
        """
        - Importing data from "./data/raw/raw_dataset.csv".
        - Converting all values to its' types.
        - Clearnig set from priceless records.

        Return: pandas.DataFrame - data from file.
        """
        dataset = pd.read_csv("./data/raw/raw_dataset.csv", na_values = ["None", "", "unknown"])
        strings = ["Locality", "Type of property", "Subtype of property", 
        "State of the building"]
        numbers = ["Price", "Number of rooms", "Living Area", "Terrace Area",
        "Garden Area", "Surface of the land", "Number of facades"]
        booleans = ["Furnished", "Terrace", "Garden", "Swimming pool"]
        dataset[strings] = dataset[strings].astype("string")
        dataset[numbers] = dataset[numbers].astype("Int64")
        dataset[booleans] = dataset[booleans].astype("boolean")
        dataset = dataset[dataset["Price"] > 0]
        dataset = dataset.sort_values(by = "Price")
        print("Import: OK")
        return dataset
    
    def csv_import(filename: str) -> pd.DataFrame:
        data = pd.read_csv(f"./data/{filename}.csv")
        return data