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
        url = "https://emasku.co.id/price"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(res.text, "html.parser")

        # Cari semua <td> yang mengandung teks "1 gr"
        td = soup.find("td", string=lambda x: x and ("1 gr" in x or "1gr" in x))
        if not td:
            print("Tidak menemukan baris 1 gr!")
            return None

        row = td.find_parent("tr")
        cols = row.find_all("td")

        # Kolom biasanya:
        # 0 = Gramasi
        # 1 = Basic Price
        # 2 = Buyback Price
        harga_jual = int(cols[1].text.replace("Rp", "").replace(".", "").strip())
        harga_beli = int(cols[2].text.replace("Rp", "").replace(".", "").strip())

        return {
            "jual": harga_jual,
            "beli": harga_beli
        }

    except Exception as e:
        print("ERROR HARTADINATA:", e)
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





