import requests

URL_INDOGOLD = "https://old-river-ece0.best-adeprasetyo.workers.dev/indogold"
URL_HRTA = "https://old-river-ece0.best-adeprasetyo.workers.dev/hartadinata"
URL_GALERI24 = "https://old-river-ece0.best-adeprasetyo.workers.dev/galeri24"

def _fetch_json(url):
    try:
        return requests.get(url, timeout=10).json()
    except:
        return {}

def get_indogold_price():
    d = _fetch_json(URL_INDOGOLD)
    return {
        "jual": d.get("jual"),
        "beli": d.get("beli"),
        "last_update": d.get("last_update")
    }

def get_hartadinata_price():
    d = _fetch_json(URL_HRTA)
    return {
        "jual": d.get("jual"),
        "beli": d.get("beli"),
        "last_update": d.get("last_update")
    }

def get_galeri24_price():
    d = _fetch_json(URL_GALERI24)
    return {
        "jual": d.get("jual"),
        "beli": d.get("beli"),
        "last_update": d.get("last_update")
    }
