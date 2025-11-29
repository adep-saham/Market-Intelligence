import streamlit as st
import requests

# ============================
# API ENDPOINTS
# ============================
URL_INDOGOLD = "https://old-river-ece0.best-adeprasetyo.workers.dev/indogold"
URL_HRTA = "https://old-river-ece0.best-adeprasetyo.workers.dev/hartadinata"
URL_GALERI24 = "https://old-river-ece0.best-adeprasetyo.workers.dev/galeri24"
URL_SPOT = "https://data-asli-kamu.com/api/spot"

# ============================
# HELPER FUNCTION
# ============================
def fetch_json(url):
    try:
        return requests.get(url, timeout=10).json()
    except:
        return {}

def calculate_premium(price, spot_gram):
    if spot_gram <= 0:
        return 0
    return (price / spot_gram) - 1

def recommend_price(my_price, competitor_avg, elasticity=0.3):
    adjustment = (competitor_avg - my_price) * elasticity
    return round(my_price + adjustment)

def get_world_gold():
    """
    Ambil spot emas dari API Anda (IDR/gram).
    Return: dict {"gram": ...}
    """
    data = fetch_json(URL_SPOT)
    if "gram" in data:
        return data
    return None


# ============================
# MAIN ELASTICITY FUNCTION (untuk app.py)
# ============================
def run_price_elasticity(spot_per_gram):

    st.subheader("📉 Price Elasticity Analysis")

    st.write(f"Spot Gold (IDR per gram): **Rp {spot_per_gram:,.0f}**")

    # Ambil data kompetitor
    indogold = fetch_json(URL_INDOGOLD)
    hartadinata = fetch_json(URL_HRTA)
    galeri24 = fetch_json(URL_GALERI24)

    competitors = {
        "IndoGold": indogold.get("jual"),
        "Hartadinata": hartadinata.get("jual"),
        "Galeri24": galeri24.get("jual")
    }

    st.write("### Premium vs Spot")
    for name, price in competitors.items():
        if price:
            premium = calculate_premium(price, spot_per_gram)
            st.write(f"- **{name}**: {premium*100:.2f}%")

    st.write("### Input Harga Kamu")
    my_price = st.number_input("Harga Kamu (Rp)", min_value=0, value=1000000)

    valid_prices = [p for p in competitors.values() if p]
    if valid_prices:
        avg_comp = sum(valid_prices) / len(valid_prices)
        rec_price = recommend_price(my_price, avg_comp)

        st.write("### Rekomendasi AI")
        st.write(f"- Rata-rata Competitor: Rp {avg_comp:,.0f}")
        st.write(f"- Harga Kamu: Rp {my_price:,.0f}")
        st.success(f"Rekomendasi AI: **Rp {rec_price:,.0f}**")

