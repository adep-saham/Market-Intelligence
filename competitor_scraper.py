import requests
import re

# -----------------------------
# Helper: Safe request
# -----------------------------
def safe_get(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.text
    except:
        return None

# -----------------------------
# UBS GOLD
# -----------------------------
def get_ubs_gold():
    try:
        url = "https://www.ubsgold.com/id/harga-emas"
        html = safe_get(url)
        if not html:
            return None

        m = re.search(r'price-current[^>]*>(.*?)<', html)
        if m:
            price = m.group(1).strip().replace(".", "")
            return int(price)
        return None
    except:
        return None


# -----------------------------
# KING HALIM
# -----------------------------
def get_king_halim():
    try:
        url = "https://kinghalim.com/price/emas"
        html = safe_get(url)
        if not html:
            return None

        m = re.search(r'(?i)harga[^>]*>(.*?)<', html)
        if m:
            price = m.group(1).replace(".", "").strip()
            return int(price)
        return None
    except:
        return None


# -----------------------------
# HARTADINATA
# -----------------------------
def get_hartadinata():
    try:
        url = "https://hartadinata.com/harga-emas"
        html = safe_get(url)
        if not html:
            return None

        m = re.search(r'class=".*?price.*?">(.*?)<', html)
        if m:
            price = m.group(1).replace(".", "").strip()
            return int(price)
        return None
    except:
        return None


# -----------------------------
# INDOGOLD (JSON - stabil)
# -----------------------------
def get_indogold():
    try:
        r = requests.get("https://www.indogold.id/ajax/pricelist", timeout=10).json()
        price = r.get("emas_antam", {}).get("buyback")
        return int(price) if price else None
    except:
        return None


# -----------------------------
# BUTIK ANTAM
# -----------------------------
def get_antam_butik():
    try:
        url = "https://butikemas.com/harga-emas-hari-ini/"
        html = safe_get(url)
        if not html:
            return None

        m = re.search(r'pricelist-value[^>]*>(.*?)<', html)
        if m:
            price = m.group(1).replace(".", "").strip()
            return int(price)
        return None
    except:
        return None


# -----------------------------
# TOKO LM ONLINE (placeholder)
# Bisa diisi ketika ada URL fix
# -----------------------------
def get_tokolm():
    return None


# =============================
# 🔥 MAIN WRAPPER
# =============================
def get_all_competitor_prices():
    return {
        "UBS Gold": get_ubs_gold(),
        "King Halim": get_king_halim(),
        "Hartadinata": get_hartadinata(),
        "IndoGold": get_indogold(),
        "Antam Butik": get_antam_butik(),
        "Toko LM Online": get_tokolm()
    }

