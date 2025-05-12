import requests
from fastapi import APIRouter
from app.core.config import settings

TWELVE_API_KEY = settings.TWELVE_API_KEY

router = APIRouter()

# /api/stocks/{symbol}
@router.get("/{symbol}")
def get_symbol_stock_price(symbol: str, interval: str = "1week", outputsize: int = 30):
    try:

        url = f"https://api.twelvedata.com/time_series"

        params = {
            "symbol": symbol,
            "interval": interval,
            "outputsize": outputsize,
            "apikey": TWELVE_API_KEY,
            "format": "JSON"
        }

        response = requests.get(url, params=params)
        data = response.json()

        if "values" in data:

            return {
                "symbol": symbol,
                "data": data["values"],
                "interval": interval,
                "outputsize": outputsize
            }

            # return {"symbol": symbol, "data": data["values"]}
        else:
            return {"error": data.get("message", "Unknown error")}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}
    

# /api/stocks
@router.get("/")
def get_symbol_stock_price():
    try:

        url = f"https://api.twelvedata.com/stocks"

        params = {
            "apikey": TWELVE_API_KEY,
            "format": "JSON"
        }

        response = requests.get(url, params=params)
        data = response.json()

        return {"data": data}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}