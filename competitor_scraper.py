import requests

# ===============================
# COMPETITOR PRICE API FUNCTIONS
# ===============================

def get_indogold_price():
    """Harga emas per gram dari IndoGold"""
    try:
        url = "https://indogold.id/api/sell/xau"
        r = requests.get(url, timeout=10)
        data = r.json()
        return data.get("price")
    except Exception:
        return None


def get_hartadinata_price():
    """Harga emas per gram dari Hartadinata"""
    try:
        url = "https://harga.hartadinata.com/api/price"
        r = requests.get(url, timeout=10)
        data = r.json()
        return data.get("sell")
    except Exception:
        return None


def get_ubs_price():
    """Harga emas per gram dari UBS Gold"""
    try:
        url = "https://www.ubslifestyle.com/api/pricelist"
        r = requests.get(url, timeout=10)
        data = r.json()
        return data["gold"]["price_sell"]
    except Exception:
        return None
