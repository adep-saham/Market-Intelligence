import requests

HEADERS = {
    "x-requested-with": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0"
}

def parse_indogold_chart(json_data):
    try:
        data = json_data[0]["data"]
        last_entry = data[-1]  # ambil baris terbaru
        return last_entry[4]   # ambil nilai CLOSE (harga final)
    except:
        return None

# =============================
# HARGA BELI (BUY)
# =============================
def get_indogold_buy_price():
    url = "https://www.indogold.id/ajax/chart_interval/GOLD/7"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            return parse_indogold_chart(r.json())
    except:
        pass
    return None

# =============================
# HARGA JUAL (SELL)
# =============================
def get_indogold_sell_price():
    url = "https://www.indogold.id/ajax/chart_interval/GOLD/7"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            return parse_indogold_chart(r.json())
    except:
        pass
    return None
