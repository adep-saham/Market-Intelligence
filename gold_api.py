import requests
import pandas as pd
from datetime import date

# =================================================
# GOLD OHLC API (STABIL)
# =================================================
RAPIDAPI_HOST = "gold-price-api.p.rapidapi.com"
RAPIDAPI_KEY = ""  # ← KOSONGKAN, AMBIL DARI ENV


def fetch_gold_ohlc(interval="1d", limit=200):
    """
    interval tidak dipakai (disimpan untuk kompatibilitas app)
    limit    tidak dipakai (history API pakai tanggal)
    """

    # ambil 1 tahun ke belakang
    end_date = date.today()
    start_date = date(end_date.year - 1, end_date.month, end_date.day)

    url = f"https://{RAPIDAPI_HOST}/v1/gold/history"
    params = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat()
    }

    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": requests.utils.get_environ_proxies(url).get(
            "RAPIDAPI_KEY", ""
        ) or None
    }

    # fallback: ambil dari environment langsung
    if not headers["x-rapidapi-key"]:
        import os
        headers["x-rapidapi-key"] = os.getenv("RAPIDAPI_KEY")

    if not headers["x-rapidapi-key"]:
        raise RuntimeError("RAPIDAPI_KEY environment variable not set")

    r = requests.get(url, headers=headers, params=params, timeout=30)
    r.raise_for_status()

    j = r.json()

    if "history" not in j:
        raise RuntimeError(f"Invalid response from Gold API: {j}")

    df = pd.DataFrame(j["history"])

    # normalisasi kolom → sesuai app.py
    df["time"] = pd.to_datetime(df["date"])
    df = df.rename(columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close"
    })

    return df[["time", "Open", "High", "Low", "Close"]].sort_values("time")
