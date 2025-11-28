import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# =========================================================
# 1. IndoGold Scraper
# =========================================================
def get_indogold_price():
    try:
        url = "https://www.indogold.id/harga-emas-hari-ini"
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # ambil harga per gram
        price_tag = soup.find("td", string="1 Gram").find_next("td")
        price = price_tag.get_text(strip=True).replace(".", "").replace(",", "")
        return int(price)
    except Exception as e:
        print("IndoGold Error:", e)
        return None


# =========================================================
# 2. Hartadinata Scraper
# =========================================================
def get_hartadinata_price():
    try:
        url = "https://hartadinata.com/harga-emas"
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # ambil harga jual per gram
        row = soup.find("td", string="1 gr").parent
        price_td = row.find_all("td")[2]   # kolom harga jual
        price = price_td.get_text(strip=True).replace(".", "").replace(",", "")
        return int(price)
    except Exception as e:
        print("Hartadinata Error:", e)
        return None


# =========================================================
# 3. UBS Gold Scraper
# =========================================================
def get_ubs_price():
    try:
        url = "https://www.ubslifestyle.com/id/produk/logam-mulia"
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # contoh ambil harga UBS 1g
        price_node = soup.find("span", class_="price")
        price = price_node.get_text(strip=True).replace("Rp", "").replace(".", "").replace(",", "")

        return int(price)
    except Exception as e:
        print("UBS Error:", e)
        return None
