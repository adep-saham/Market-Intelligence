import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}

# ===========================
# UBS Gold
# ===========================
def get_ubs_gold():
    try:
        url = "https://www.ubsgold.com/id/harga-emas"
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        price = soup.select_one(".price-current")
        if price:
            return price.text.strip()

        return None
    except:
        return None


# ===========================
# King Halim
# ===========================
def get_king_halim():
    try:
        url = "https://kinghalim.com/price/emas"
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        price = soup.select_one(".harga-emas")
        if price:
            return price.text.strip()

        return None
    except:
        return None


# ===========================
# Hartadinata
# ===========================
def get_hartadinata():
    try:
        url = "https://hartadinata.com/harga-emas"
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        price = soup.select_one(".gold-price")
        if price:
            return price.text.strip()

        return None
    except:
        return None


# ===========================
# IndoGold
# ===========================
def get_indogold():
    try:
        url = "https://www.indogold.id/ajax/pricelist"
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()

        return data.get("emas_antam", {}).get("buyback", None)
    except:
        return None


# ===========================
# Antam Butik
# ===========================
def get_antam_butik():
    try:
        url = "https://butikemas.com/harga-emas-hari-ini/"
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        price = soup.select_one(".pricelist-value")
        if price:
            return price.text.strip()

        return None
    except:
        return None
