import requests
import json
import re

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
        import requests
        import json

        url = "https://www.indogold.id/home/get_data_pricelist"

        # Payload EXACT dari browser
        payload = "type=pricelist&type_gold=ubs"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://www.indogold.id",
            "Referer": "https://www.indogold.id/harga-emas-fisik/",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "*/*",
        }

        response = requests.post(url, data=payload, headers=headers, timeout=10)

        print("DEBUG UBS RAW:", response.text[:300])  # Debug penting

        data = json.loads(response.text)

        one_gram = data["data"]["data_denom"]["1.0"]["Tahun 2025"]

        jual = clean_rupiah(one_gram["harga"])
        beli = clean_rupiah(one_gram["harga_buyback"])

        return {"jual": jual, "beli": beli}

    except Exception as e:
        print("UBS ERROR =>", e)
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















