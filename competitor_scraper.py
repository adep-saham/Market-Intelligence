import requests

# ===================================================
# 1. SCRAPER INDOGOLD
# ===================================================
def get_indogold_price():
    """
    Mengambil harga BELI & JUAL dari IndoGold.
    Harga terbaru berada di candle: [timestamp, open, high, low, close].
    close adalah harga terbaru.
    """

    try:
        url_beli  = "https://www.indogold.id/ajax/chart_interval/GOLD/7"   # Harga beli
        url_jual  = "https://www.indogold.id/ajax/chart_interval/GOLD/10"  # Harga jual

        headers = {"User-Agent": "Mozilla/5.0"}

        # GET data jual
        jual_res = requests.get(url_jual, headers=headers, timeout=10).json()
        beli_res = requests.get(url_beli, headers=headers, timeout=10).json()

        # Validasi response format
        if not jual_res or not beli_res:
            return None
        
        # Ambil harga CLOSE terakhir → elemen ke-1 → CLOSE = index ke-4
        jual_candle = jual_res[0]["data"][-1]
        beli_candle = beli_res[0]["data"][-1]

        harga_jual = jual_candle[4]
        harga_beli = beli_candle[4]

        return {
            "jual": harga_jual,
            "beli": harga_beli
        }

    except Exception as e:
        print("Error IndoGold:", e)
        return None


# ===================================================
# 2. SCRAPER HARTADINATA (emasmu.co.id)
# ===================================================
def get_hartadinata_price():
    """
    Endpoint resmi Hartadinata (Emasku.co.id)
    Mengambil harga 1 gram sebagai standar.
    """

    try:
        url = "https://emasku.co.id/api/prices"
        headers = {"User-Agent": "Mozilla/5.0"}

        res = requests.get(url, headers=headers, timeout=10)
        data = res.json()

        if "data" not in data:
            return None

        gold_series = data["data"][0]   # Ambil series Gold
        prices = gold_series.get("prices", [])

        for item in prices:
            if float(item["gramasi"]) == 1.0:  # Gunakan gramasi 1 gram
                return {
                    "jual": item["price"],
                    "beli": item["buyback_price"]
                }

        return None

    except Exception as e:
        print("Error Hartadinata:", e)
        return None


# ===================================================
# 3. GABUNGAN (UNTUK API ROUTE)
# ===================================================
def get_all_competitors():
    """
    API gabungan untuk dipakai di Cloudflare Worker atau Streamlit.
    Mengembalikan semua harga sekaligus.
    """
    return {
        "indogold": get_indogold_price(),
        "hartadinata": get_hartadinata_price(),
        # "ubs": get_ubs_price()   ← nanti kalau sudah siap UBS
    }
