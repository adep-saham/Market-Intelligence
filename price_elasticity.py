import streamlit as st
import requests

# ============================
# API ENDPOINTS
# ============================
URL_INDOGOLD = "https://old-river-ece0.best-adeprasetyo.workers.dev/indogold"
URL_HRTA = "https://old-river-ece0.best-adeprasetyo.workers.dev/hartadinata"
URL_GALERI24 = "https://old-river-ece0.best-adeprasetyo.workers.dev/galeri24"


# ============================
# HELPERS
# ============================
def fetch_json(url):
    try:
        return requests.get(url, timeout=10).json()
    except:
        return {}


def calculate_premium(price, spot_gram):
    if price is None or spot_gram is None or spot_gram <= 0:
        return None
    return (price / spot_gram) - 1


def recommend_price(my_price, competitor_avg, elasticity=0.3):
    adjustment = (competitor_avg - my_price) * elasticity
    return round(my_price + adjustment)


# ============================
# SCRAPERS (SAMA DENGAN app.py)
# ============================
def get_indogold():
    d = fetch_json(URL_INDOGOLD)
    return {"jual": d.get("jual"), "beli": d.get("beli")}


def get_hartadinata():
    d = fetch_json(URL_HRTA)
    return {"jual": d.get("jual"), "beli": d.get("beli")}


def get_galeri24():
    d = fetch_json(URL_GALERI24)
    return {"jual": d.get("jual"), "beli": d.get("beli")}


# ============================
# MAIN FUNCTION DIPANGGIL DARI app.py
# ============================
def run_price_elasticity(spot_per_gram):

    st.subheader("📉 Price Elasticity Analysis")
    st.write(f"Spot Gold (IDR per gram): **Rp {spot_per_gram:,.0f}**")

    # Ambil data kompetitor
    indogold = get_indogold()
    hartadinata = get_hartadinata()
    galeri24 = get_galeri24()

    competitors = {
        "IndoGold": indogold["jual"],
        "Hartadinata": hartadinata["jual"],
        "Galeri 24": galeri24["jual"]
    }

    # ============================
    # PREMIUM VS SPOT
    # ============================
    st.write("### Premium vs Spot")

    for name, price in competitors.items():
        premium = calculate_premium(price, spot_per_gram)
        if premium is not None:
            st.write(f"- **{name}**: {premium*100:.2f}%")
        else:
            st.write(f"- **{name}**: N/A")

    # ============================
    # INPUT USER
    # ============================
    st.write("### Input Harga Kamu")
    my_price = st.number_input("Harga Kamu (Rp)", min_value=0, value=1000000)

    # Hitung average competitor
    valid_prices = [p for p in competitors.values() if p]
    if not valid_prices:
        st.error("Tidak ada data competitor valid.")
        return

    avg_comp = sum(valid_prices) / len(valid_prices)
    rec_price = recommend_price(my_price, avg_comp)

    st.write("### Rekomendasi AI")
    st.write(f"- Rata-rata Competitor: Rp {avg_comp:,.0f}")
    st.write(f"- Harga Kamu: Rp {my_price:,.0f}")
    st.success(f"Rekomendasi AI: **Rp {rec_price:,.0f}**")
