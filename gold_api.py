import requests
import pandas as pd

# =================================================
# GOLD API VIA CLOUDFLARE WORKER (NO API KEY)
# =================================================
WORKER_URL = "https://odd-queen-ae24.best-adeprasetyo.workers.dev/"

def fetch_gold_ohlc(interval="1d", limit=200):
    """
    interval & limit disimpan untuk kompatibilitas app.py
    Data diambil dari Cloudflare Worker
    """

    r = requests.get(WORKER_URL, timeout=30)
    r.raise_for_status()

    j = r.json()

    if "ohlc" not in j:
        raise RuntimeError(f"Invalid response from worker: {j}")

    df = pd.DataFrame(j["ohlc"])
    df["time"] = pd.to_datetime(df["time"])

    # Sesuaikan dengan app.py kamu
    df = df.rename(columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close"
    })

    return df.sort_values("time")
