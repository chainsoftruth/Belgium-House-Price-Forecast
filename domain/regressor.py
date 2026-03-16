import pandas as pd
import numpy as np
import matplotlib as plt
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

class Regressor():

    def __init__(self, df):
        self._houses = df[df.type == "house"].iloc[:,1:]
        self._apartments = df[df.type == "apartment"].iloc[:,1:]
        self._apartments = self._apartments.drop("land_area", axis = 1)
        self._houses["subtype"] = self._houses["subtype"].apply(lambda x: Regressor._subtype_replace(x))
        self._apartments["subtype"] = self._apartments["subtype"].apply(lambda x: Regressor._subtype_replace(x))
        hy = self._houses.price
        apy = self._apartments.price
        hX = self._houses.drop("price", axis=1)
        apX = self._apartments.drop("price", axis=1)
        self.hX_train, self.hX_test, self.hy_train, self.hy_test = train_test_split(hX, hy, random_state = 24, test_size = 0.2)
        self.apX_train, self.apX_test, self.apy_train, self.apy_test = train_test_split(apX, apy, random_state = 24, test_size = 0.2)
    
    def set_linear(self, property: dict) -> int:
        self.h_scaler = StandardScaler()
        self.h_scaler.fit(hX_train)
        self.hX_train = self.h_scaler.transform(self.hX_train)
        self.hX_test = self.h_scaler.transform(self.hX_test)
        self.ap_scaler = StandardScaler()
        self.ap_scaler.fit(apX_train)
        self.apX_train = self.ap_scaler.transform(self.apX_train)
        self.apX_test = self.ap_scaler.transform(self.apX_test)
        self.h_pipeline = Pipeline([
            ("poly", PolynomialFeatures(degree = 2)),
            ("model", LinearRegression())
        ])
        self.ap_pipeline = Pipeline([
            ("poly", PolynomialFeatures(degree = 2)),
            ("model", LinearRegression())
        ])
        self.h_pipeline.fit(self.hX_train, self.hy_train)
        self.ap_pipeline.fit(self.apX_train, self.apy_train)
        print("Model trained: OK.")
        print(f"H. score: {self.h_pipeline.score(self.hX_test, hy_test)}")
        print(f"Ap. score: {self.ap_pipeline.score(self.apX_test, self.apy_test)}")

    @staticmethod
    def _subtype_replace(str):
        match str:
            case "studio" | "chalet" | "ground-floor" | "apartment" | "bungalow":
                return 1
            case "triplex" | "duplex" | "residence" | "mixed-building" | "loft":
                return 2
            case "cottage" | "penthouse" | "master-house" | "villa" | "mansion":
                return 3