import pandas as pd
import math

class DataCleaner():

    @staticmethod
    def check(data: pd.DataFrame):
        print("------DataFrame check------")
        print("Empty values:")
        for col in data:
            print(f"{col}: {data[col].isna().sum()}")
    
    @staticmethod
    def optimize(data: pd.DataFrame) -> pd.DataFrame:
        pass

    @staticmethod
    def trim_data_edges(data):
        """
        Removes 5% of the data from the beginning and 5% from the end.
        Returns the trimmed list.
        """

        if data is None or data.empty:
            print("No data provided.")
            return data

        total_rows = len(data)
        trim_count = math.floor(total_rows * 0.05)

        if total_rows <= trim_count * 2:
            print("Dataset too small to trim 5% from both ends.")
            return data

        trimmed_data = data.iloc[trim_count: total_rows - trim_count]

        print(f"Trimmed {trim_count} rows from start and end.")
        return trimmed_data