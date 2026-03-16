import pandas as pd
import numpy as np
import matplotlib as plt
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

class Classifier():
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
        self.hX_train, self.hX_test, self.hy_train, self.hy_test = train_test_split(hX, hy, random_state = 24, test_size = 0.25)
        self.apX_train, self.apX_test, self.apy_train, self.apy_test = train_test_split(apX, apy, random_state = 24, test_size = 0.25)
    
    def _std_scale(self):
        self.h_scaler = StandardScaler()
        self.h_scaler.fit(hX_train)
        self.hX_train = self.h_scaler.transform(self.hX_train)
        self.hX_test = self.h_scaler.transform(self.hX_test)

        self.ap_scaler = StandardScaler()
        self.ap_scaler.fit(apX_train)
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
        print(f"H. score: {round(self.h_model.score(hX_test, hy_test)*100,2)}")
        print(f"Ap. score: {round(self.ap_model.score(apX_test, apy_test)*100,2)}")
    
    def set_randomforest(self):
        self._std_scale()
        self.h_model = RandomForestRegressor(random_state = 24, n_estimators = 300)
        self.ap_model = RandomForestRegressor(random_state = 24, n_estimators = 300)
        h_model.fit(hX_train, hy_train)
        ap_model.fit(apX_train, apy_train)
        print("RandomForest model trained: OK.")
        print(f"H. score: {round(self.h_model.score(hX_test, hy_test)*100,2)}")
        print(f"Ap. score: {round(self.ap_model.score(apX_test, apy_test)*100,2)}")