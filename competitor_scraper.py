import requests
import json
import re
import cloudscraper


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
        url = "https://emasku.co.id/api/v1/branding/prices/one"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10).json()

        if res.get("code") != 200:
            return None

        data = res.get("data", {})

        return {
            "jual": int(data.get("latest_price")),
            "beli": int(data.get("buyback_price"))
        }

    except Exception as e:
        print("ERROR Hartadinata:", e)
        return None

def clean_rupiah(text):
    if not text:
        return None
    return int(re.sub(r"[^\d]", "", text))


def get_ubs_price():
    try:
        url = "https://www.indogold.id/home/get_data_pricelist"

        headers = {
            "Origin": "https://www.indogold.id",
            "Referer": "https://www.indogold.id/harga-emas-hari-ini",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "*/*"
        }

        form = {
            "form": '{"product":"UBS_5"}',
            "simulasi-token": "de15246fb6f274dbd807684c0ca0b807"
        }

        response = requests.post(url, data=form, headers=headers, timeout=10)
        print("UBS RAW:", response.text)   # debugging

        data = response.json()

        # gunakan pecahan 1 gram (atau yang paling sering dipakai)
        denom = data["data"]["data_denom"]["1.0"]["Tahun 2025"]

        harga_jual = int(denom["harga"].replace("Rp. ", "").replace(".", ""))
        harga_beli = int(denom["harga_buyback"].replace("Rp. ", "").replace(".", ""))

        return {"jual": harga_jual, "beli": harga_beli}

    except Exception as e:
        print("UBS Error:", e)
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


















