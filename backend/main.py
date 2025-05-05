from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
import finnhub
import os
import finnhub
import time
import yfinance as yf
import requests

from predictor import Predictor

app = FastAPI()

# Ideally store your key in an environment variable
API_KEY = os.getenv("TWELVE_API_KEY", "9a04cd0f7ac843b29155f97d6ef84d2a")

finnhub_client = finnhub.Client(api_key=API_KEY)


@app.get("/api/stocks/{symbol}")
def get_symbol_stock_price(symbol: str, interval: str = "1week", outputsize: int = 30):
    try:

        url = f"https://api.twelvedata.com/time_series"

        params = {
            "symbol": symbol,
            "interval": interval,
            "outputsize": outputsize,
            "apikey": API_KEY,
            "format": "JSON"
        }

        response = requests.get(url, params=params)
        data = response.json()

        if "values" in data:

            predictor = Predictor(data["values"])
            predictor.preprocess()
            predictor.train()
            prediction = predictor.predict_next()
            n_prediction = predictor.predict_next_n(5)

            return {
                "symbol": symbol,
                "data": data["values"],
                "predicted_close_price_next_day": round(prediction, 2),
                "predicted_close_price_next_5_days": [round(p, 2) for p in n_prediction]
            }

            # return {"symbol": symbol, "data": data["values"]}
        else:
            return {"error": data.get("message", "Unknown error")}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}
    
@app.get("/api/stocks")
def get_symbol_stock_price():
    try:

        url = f"https://api.twelvedata.com/stocks"

        params = {
            "apikey": API_KEY,
            "format": "JSON"
        }

        response = requests.get(url, params=params)
        data = response.json()

        return {"data": data}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}