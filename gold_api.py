import requests
import pandas as pd

RAPIDAPI_KEY = "ISI_API_KEY_KAMU"
RAPIDAPI_HOST = "gold-price-xauusd-ohcl-api.p.rapidapi.com"

def fetch_gold_ohlc(interval="1d", limit=200):
    url = "https://gold-price-xauusd-ohcl-api.p.rapidapi.com/ohlc"

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    params = {
        "interval": interval,
        "limit": limit
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data)
    df["time"] = pd.to_datetime(df["time"], unit="s")

    df = df.rename(columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close"
    })

    return df.sort_values("time")
