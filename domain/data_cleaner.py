import pandas as pd

class DataCleaner():

    @staticmethod
    def check(data: pd.DataFrame):
        print("------DataFrame check------")
        print("Empty values:")
        for col in data:
            print(f"{col}: {col}")
    
    @staticmethod
    def optimize(data: pd.DataFrame) -> pd.DataFrame:
        pass