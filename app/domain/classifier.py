import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

class Classifier():
    def __init__(self, df):
        self.data = df
        self.y1 = self.data.facades
        self.y2 = self.data.state
        self.X = self.data.drop(["facades", "state", "furnished", "type"], axis = 1)
        self.X = pd.get_dummies(self.X, columns = ["subtype"], drop_first = True)
        self._std_scale()
    
    def _std_scale(self):
        self.scaler = StandardScaler()
        self.X = self.scaler.fit_transform(self.X)
    
    def set_randomforest(self):
        self.model1 = RandomForestClassifier(random_state = 24, n_estimators = 250)
        self.model1.fit(self.X, self.y1)
        self.model2 = RandomForestClassifier(random_state = 24, n_estimators = 250)
        self.model2.fit(self.X, self.y2)
        print("RandomForest models trained: OK.")

    def predict(self, data):
        data = data.drop(["facades", "state", "furnished", "type"], axis = 1)
        data = pd.get_dummies(data, columns = ["subtype"], drop_first = True)
        self.scaler.transform(data)
        return self.model1.predict(data), self.model2.predict(data)