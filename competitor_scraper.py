import requests

BASE = "https://old-river-ece0.best-adeprasetyo.workers.dev"  # ganti sesuai worker kamu


def get_indogold_price():
    try:
        r = requests.get(f"{BASE}/indogold", timeout=10)
        d = r.json()
        return {
            "jual": d["jual"],
            "beli": d["beli"],
            "last_update": d.get("last_update", "—")
        }
    except:
        return None


def get_hartadinata_price():
    try:
        r = requests.get(f"{BASE}/hartadinata", timeout=10)
        d = r.json()
        return {
            "jual": d["jual"],
            "beli": d["beli"],
            "last_update": d.get("last_update", "—")
        }
    except:
        return None


def get_galeri24_price():
    try:
        r = requests.get(f"{BASE}/galeri24", timeout=10)
        d = r.json()
        return {
            "jual": d["jual"],
            "beli": d["beli"],
            "last_update": d.get("last_update", "—")
        }
    except:
        return None
