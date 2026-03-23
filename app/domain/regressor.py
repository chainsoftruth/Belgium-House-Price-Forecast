import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.pipeline import Pipeline

class Regressor():

    def __init__(self, df):
        self._houses = df[df.type == "house"].iloc[:,1:]
        self._apartments = df[df.type == "apartment"].iloc[:,1:]
        hy = self._houses.price
        hX = self._houses.drop("price", axis=1)
        apy = self._apartments.price
        apX = self._apartments.drop("price", axis=1)
        self.hX_train, self.hX_test, self.hy_train, self.hy_test = train_test_split(hX, hy, random_state = 24, test_size = 0.25)
        self.apX_train, self.apX_test, self.apy_train, self.apy_test = train_test_split(apX, apy, random_state = 24, test_size = 0.25)
        self._subtypes = self._subtype_fit(
            np.concatenate((self.hX_train, self.apX_train), axis=0), 
            np.concatenate((self.hy_train, self.apy_train)))
        self.apX_train = self.apX_train.drop("land_area", axis = 1)
        self.apX_test = self.apX_test.drop("land_area", axis = 1)
        self.hX_train["subtype"] = self.hX_train["subtype"].apply(self._subtype_transform)
        self.hX_test["subtype"] = self.hX_test["subtype"].apply(self._subtype_transform)
        self.apX_train["subtype"] = self.apX_train["subtype"].apply(self._subtype_transform)
        self.apX_test["subtype"] = self.apX_test["subtype"].apply(self._subtype_transform)
        
    
    def _std_scale(self):
        self.h_scaler = StandardScaler()
        self.h_scaler.fit(self.hX_train)
        self.hX_train = self.h_scaler.transform(self.hX_train)
        self.hX_test = self.h_scaler.transform(self.hX_test)
        self.ap_scaler = StandardScaler()
        self.ap_scaler.fit(self.apX_train)
        self.apX_train = self.ap_scaler.transform(self.apX_train)
        self.apX_test = self.ap_scaler.transform(self.apX_test)

    def set_linear(self):
        self._std_scale()
        self.h_model = Pipeline([
            ("poly", PolynomialFeatures(degree = 2)),
            ("model", LinearRegression())
        ])
        self.ap_model = Pipeline([
            ("poly", PolynomialFeatures(degree = 2)),
            ("model", LinearRegression())
        ])
        self.h_model.fit(self.hX_train, self.hy_train)
        self.ap_model.fit(self.apX_train, self.apy_train)
        print("Linear model trained: OK.")
        print(f"H. score: {round(self.h_model.score(self.hX_test, self.hy_test)*100,2)}")
        print(f"Ap. score: {round(self.ap_model.score(self.apX_test, self.apy_test)*100,2)}")
    
    def set_randomforest(self):
        self._std_scale()
        self.h_model = RandomForestRegressor(random_state = 24, n_estimators = 300)
        self.ap_model = RandomForestRegressor(random_state = 24, n_estimators = 300)
        self.h_model.fit(self.hX_train, self.hy_train)
        self.ap_model.fit(self.apX_train, self.apy_train)
        print("RandomForest model trained: OK.")
        print(f"H. score: {round(self.h_model.score(self.hX_test, self.hy_test)*100,2)}")
        print(f"Ap. score: {round(self.ap_model.score(self.apX_test, self.apy_test)*100,2)}")

    def set_gradientboosting(self):
        self._std_scale()
        self.h_model = GradientBoostingRegressor(random_state = 24, n_estimators = 300)
        self.ap_model = GradientBoostingRegressor(random_state = 24, n_estimators = 300)
        self.h_model.fit(self.hX_train, self.hy_train)
        self.ap_model.fit(self.apX_train, self.apy_train)
        print("GradientBoosting model trained: OK.")
        print(f"H. score: {round(self.h_model.score(self.hX_test, self.hy_test)*100,2)}")
        print(f"Ap. score: {round(self.ap_model.score(self.apX_test, self.apy_test)*100,2)}")
    
    def _subtype_fit(self, data, prices):
        df = pd.DataFrame(data).iloc[:,0].to_frame()
        df.columns = ["subtype"]
        df["price"] = prices
        subtypes = {}
        types_list = df.groupby("subtype")["price"].mean().sort_values().reset_index()["subtype"]
        for i, value in enumerate(types_list):
            subtypes[value] = i
        json.dump(subtypes, open("app/data/external/subtypes.json", "w"))
        return subtypes

    def _subtype_transform(self, value):
        return self._subtypes[value]