import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class Predictor:
    def __init__(self, historical_data: list[dict]):
        self.df = pd.DataFrame(historical_data)
        self.df["datetime"] = pd.to_datetime(self.df["datetime"])
        self.df.sort_values("datetime", inplace=True)
        self.model = LinearRegression()

    def preprocess(self):
        self.df["timestamp"] = self.df["datetime"].astype(np.int64) // 10**9  # seconds
        self.df["close"] = self.df["close"].astype(float)

    def train(self):
        X = self.df[["timestamp"]]
        y = self.df["close"]
        self.model.fit(X, y)

    def predict_next(self):
        last_ts = self.df["timestamp"].iloc[-1]
        next_ts = last_ts + 86400  # add one day (in seconds)
        prediction = self.model.predict([[next_ts]])
        return float(prediction[0])

    def predict_next_n(self, n: int):
        last_ts = self.df["timestamp"].iloc[-1]
        next_ts = last_ts + 86400  # add one day (in seconds)
        predictions = []
        for i in range(n):
            prediction = self.model.predict(pd.DataFrame({"timestamp": [next_ts]}))
            predictions.append(float(prediction[0]))
            next_ts += 86400  # add one day (in seconds)
        return predictions