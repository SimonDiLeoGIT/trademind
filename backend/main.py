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

app = FastAPI()

# Ideally store your key in an environment variable
API_KEY = os.getenv("TWELVE_API_KEY", "9a04cd0f7ac843b29155f97d6ef84d2a")

finnhub_client = finnhub.Client(api_key=API_KEY)


@app.get("/api/stock/{symbol}")
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
            return {"symbol": symbol, "data": data["values"]}
        else:
            return {"error": data.get("message", "Unknown error")}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}