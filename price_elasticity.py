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
# HELPERS
# ============================
def fetch_json(url):
    try:
        return requests.get(url, timeout=10).json()
    except:
        return {}


def calculate_premium(price, spot_gram):
    if not price or spot_gram <= 0:
        return None
    return (price / spot_gram) - 1


def recommend_price(my_price, competitor_avg, elasticity=0.3):
    adjustment = (competitor_avg - my_price) * elasticity
    return round(my_price + adjustment)


def get_world_gold():
    data = fetch_json(URL_SPOT)
    return data.get("gram", None)


# ============================
# FIXED SCRAPERS (gunakan sama seperti app.py)
# ============================
def get_indogold():
    data = fetch_json(URL_INDOGOLD)
    return {
        "jual": data.get("jual"),
        "beli": data.get("beli")
    }


def get_hrta():
    data = fetch_json(URL_HRTA)
    return {
        "jual": data.get("jual"),
        "beli": data.get("beli"),
    }


def get_galeri24():
    data = fetch_json(URL_GALERI24)
    return {
        "jual": data.get("jual"),
        "beli": data.get("beli")
    }


# ============================
# MAIN FUNCTION FOR STREAMLIT
# ============================
def run_price_elasticity(spot_per_gram):

    st.subheader("📉 Price Elasticity Analysis")

    st.write(f"Spot Gold (IDR per gram): **Rp {spot_per_gram:,.0f}**")

    # Gunakan scraper yg sama dengan Competitor Page
    indogold = get_indogold()
    hartadinata = get_hrta()
    galeri24 = get_galeri24()

    competitors = {
        "IndoGold": indogold["jual"],
        "Hartadinata": hartadinata["jual"],
        "Galeri24": galeri24["jual"]
    }

    st.write("### Premium vs Spot")
    for name, price in competitors.items():
        premium = calculate_premium(price, spot_per_gram)
        if premium is not None:
            st.write(f"- **{name}**: {premium*100:.2f}%")
        else:
            st.write(f"- **{name}**: N/A")

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
    else:
        st.error("Tidak ada data competitor valid.")


