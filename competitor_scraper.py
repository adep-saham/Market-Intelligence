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

        # STEP 1 → Ambil cookie dari halaman Indogold
        session = requests.Session()
        session.get("https://www.indogold.id/harga-emas-fisik/", headers={
            "User-Agent": "Mozilla/5.0"
        })

        # Cookie akan otomatis tersimpan di session.cookies

        # STEP 2 → POST untuk ambil harga UBS
        url = "https://www.indogold.id/home/get_data_pricelist"
        payload = "type=pricelist&type_gold=ubs"

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://www.indogold.id",
            "Referer": "https://www.indogold.id/harga-emas-fisik/",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "*/*",
        }

        response = session.post(url, data=payload, headers=headers, timeout=10)

        # Debug response
        print("DEBUG UBS RAW:", response.text[:400])
        print("DEBUG UBS COOKIES:", session.cookies.get_dict())

        data = json.loads(response.text)

        first_key = list(data["data"]["data_denom"].keys())[0]
        one_gram_data = data["data"]["data_denom"][first_key]["Tahun 2025"]

        jual = clean_rupiah(one_gram_data["harga"])
        beli = clean_rupiah(one_gram_data["harga_buyback"])

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
















