import requests

# ===================================================
# 1. SCRAPER INDOGOLD
# ===================================================
def get_indogold_price():
    try:
        url_jual = "https://www.indogold.id/ajax/chart_interval/GOLD/7"
        url_beli = "https://www.indogold.id/ajax/chart_interval/GOLD/7"

        data_jual = requests.get(url_jual, timeout=10).json()
        data_beli = requests.get(url_beli, timeout=10).json()

        last_jual = data_jual[0]["data"][-1]   # high = index 2
        last_beli = data_beli[0]["data"][-1]   # low  = index 3

        harga_jual = last_jual[2]   # high
        harga_beli = last_beli[3]   # low

        return {
            "jual": harga_jual,
            "beli": harga_beli
        }

    except:
        return None



# ===================================================
# 2. SCRAPER HARTADINATA (emasmu.co.id)
# ===================================================
def get_hartadinata_price():
    try:
        url = "https://emasku.co.id/api/prices"

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Origin": "https://emasku.co.id",
            "Referer": "https://emasku.co.id/",
            "X-Requested-With": "XMLHttpRequest"
        }

        res = requests.get(url, headers=headers, timeout=10)

        # DEBUG print
        print("HARTADINATA RAW:", res.text)

        data = res.json()

        if "data" not in data or len(data["data"]) == 0:
            return None

        # Ambil Gold Series (biasanya index 0)
        gold_series = data["data"][0]
        prices = gold_series.get("prices", [])

        # Cari gramasi 1 gram
        for item in prices:
            if float(item.get("gramasi", 0)) == 1.0:
                return {
                    "jual": item["price"],
                    "beli": item["buyback_price"]
                }

        return None

    except Exception as e:
        print("ERROR HARTADINATA:", e)
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


