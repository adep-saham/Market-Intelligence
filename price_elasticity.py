import streamlit as st
import requests

# ============================
# API ENDPOINTS
# ============================
URL_INDOGOLD = "https://old-river-ece0.best-adeprasetyo.workers.dev/indogold"
URL_HRTA = "https://old-river-ece0.best-adeprasetyo.workers.dev/hartadinata"
URL_GALERI24 = "https://old-river-ece0.best-adeprasetyo.workers.dev/galeri24"

def run_price_elasticity(spot_price_from_app):
    st.subheader("📈 Price Elasticity Modeling (AI)")

    if spot_price_from_app is None or spot_price_from_app <= 0:
        st.error("Gagal mengambil harga spot emas")
        return

    spot_price = spot_price_from_app
    st.metric("Harga Spot per Gram", f"Rp {spot_price:,}")


# ============================
# HELPERS
# ============================
def fetch_json(url):
    try:
        res = requests.get(url, timeout=10)
        return res.json()
    except:
        return {}


def calculate_premium(price, spot_gram):
    if spot_gram <= 0:
        return 0
    return (price / spot_gram) - 1


def recommend_price(my_price, competitor_avg, elasticity=0.3):
    adjustment = (competitor_avg - my_price) * elasticity
    return round(my_price + adjustment)


# ============================
# STREAMLIT MAIN FUNCTION
# ============================
def run_price_elasticity():

    st.subheader("📈 Price Elasticity Modeling (AI)")

    # fetch data
    indogold = fetch_json(URL_INDOGOLD)
    hrta = fetch_json(URL_HRTA)
    g24 = fetch_json(URL_GALERI24)
    spot = fetch_json(URL_SPOT)

    if "gram" not in spot:
        st.error("Gagal mengambil harga spot emas")
        return

    spot_price = spot["gram"]

    st.metric("Harga Spot per Gram", f"Rp {spot_price:,}")

    st.divider()

    # competitor section
    st.write("### 🔹 Competitor Prices")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("### IndoGold")
        st.metric("Jual", f"Rp {indogold.get('jual', 0):,}")
        st.metric("Beli", f"Rp {indogold.get('beli', 0):,}")

    with col2:
        st.write("### Hartadinata")
        st.metric("Jual", f"Rp {hrta.get('jual', 0):,}")
        st.metric("Beli", f"Rp {hrta.get('beli', 0):,}")

    with col3:
        st.write("### Galeri 24")
        st.metric("Jual", f"Rp {g24.get('jual', 0):,}")
        st.metric("Beli", f"Rp {g24.get('beli', 0):,}")

    competitor_avg = (
        indogold.get("jual", 0) +
        hrta.get("jual", 0) +
        g24.get("jual", 0)
    ) / 3

    st.divider()
    st.metric("Rata-rata Harga Competitor", f"Rp {competitor_avg:,.0f}")

    st.divider()

    st.write("### 🔹 Input Harga Kamu")
    my_price = st.number_input("Harga Jual Kamu (Rp)", value=2300000)

    recommended = recommend_price(my_price, competitor_avg)

    st.write("### 🔹 AI Recommendation")
    st.metric("Harga Rekomendasi AI", f"Rp {recommended:,}")

    elasticity_score = min(1, abs(my_price - competitor_avg) / competitor_avg)

    st.caption(f"Elasticity Score: {elasticity_score:.3f} (0 = aman, 1 = sensitif)")

    st.divider()

    st.write("### 🔹 Premium vs Spot")

    prem_ig = calculate_premium(indogold.get("jual", 0), spot_price)
    prem_hr = calculate_premium(hrta.get("jual", 0), spot_price)
    prem_g24 = calculate_premium(g24.get("jual", 0), spot_price)

    st.write(f"- IndoGold: **{prem_ig*100:.2f}%**")
    st.write(f"- Hartadinata: **{prem_hr*100:.2f}%**")
    st.write(f"- Galeri 24: **{prem_g24*100:.2f}%**")

