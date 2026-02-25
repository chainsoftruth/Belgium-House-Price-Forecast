import pandas as pd

class DataManager():

    @staticmethod
    def links_export(links: list[str]):
        """Exporting links to .txt"""
        with open("./data/links.txt", "w") as file:
            for link in links:
                file.write(f"{link}\n")
    
    @staticmethod
    def links_import() -> list[str]:
        """Importing links from .txt"""
        with open("./data/links.txt", "r") as file:
            lines = [line.strip() for line in file if line.strip()]
        return lines

    @staticmethod
    def data_csv_export(data):
        """Exporting data list (list of dicts) into ./data/dataset.csv"""
        pass
    
    @staticmethod
    def data_csv_import() -> pd.DataFrame:
        dataset = pd.read_csv("./data/dataset.csv", na_values = ["None", ""])
        strings = ["Locality", "Type of property", "Subtype of property", 
        "Type of sale", "State of the building"]
        numbers = ["Price", "Number of rooms", "Living Area", "Terrace Area",
        "Garden Area", "Surface of the land", "Number of facades"]
        booleans = ["Furnished", "Terrace", "Garden", "Swimming pool"]
        dataset[strings] = dataset[strings].astype(str)
        dataset[numbers] = dataset[numbers].astype(int)
        dataset[booleans] = dataset[booleans].astype(bool)

        dataset = dataset[dataset["Price"] > 0]
        print("Import: OK")
        print(f"Rows: {len(dataset)}")
        return dataset
        