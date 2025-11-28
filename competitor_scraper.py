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

def get_ubs_price():
    try:
        url = "https://www.indogold.id/home/get_data_pricelist"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://www.indogold.id",
            "Referer": "https://www.indogold.id/",
        }

        resp = requests.post(url, headers=headers, timeout=10)
        print("RAW UBS:", resp.text[:500])
        if resp.status_code != 200:
            print("UBS Error: status", resp.status_code)
            return None

        data = resp.json()

        # Pastikan struktur JSON benar
        if "data" not in data or "data_denom" not in data["data"]:
            print("UBS Error: struktur tidak sesuai", data)
            return None

        denom = data["data"]["data_denom"]

        # Ambil pecahan 1 gram
        if "1.0" not in denom:
            print("UBS Error: tidak ada '1.0' dalam denom:", denom.keys())
            return None
        
        dat = denom["1.0"]["Tahun 2025"]

        harga_jual = int(dat["harga"].replace("Rp.", "").replace(" ", "").replace(",", ""))
        harga_beli = int(dat["harga_buyback"].replace("Rp.", "").replace(" ", "").replace(",", ""))

        return {"jual": harga_jual, "beli": harga_beli}

    except Exception as e:
        print("UBS ERROR:", e)
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











