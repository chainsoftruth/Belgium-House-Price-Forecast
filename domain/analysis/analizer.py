import pandas as pd

class Analizer:
    def __init__(self, data: pd.DataFrame):
        self._data = data

    def print_statistics():
        print("\n--- Statistics for given DataFrame ---\n")
        print(data.info())