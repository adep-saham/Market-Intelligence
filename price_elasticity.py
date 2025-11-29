import streamlit as st
from competitor_scraper import (
    get_indogold_price,
    get_hartadinata_price,
    get_galeri24_price
)

def calculate_premium(price, spot_gram):
    if price is None or spot_gram is None or spot_gram <= 0:
        return None
    try:
        return (float(price) / float(spot_gram)) - 1
    except:
        return None

def recommend_price(my_price, competitor_avg, elasticity=0.3):
    try:
        adjustment = (competitor_avg - my_price) * elasticity
        return round(my_price + adjustment)
    except:
        return my_price

def run_price_elasticity(spot_per_gram):

    st.subheader("📉 Price Elasticity Analysis")
    st.write(f"Spot Gold (IDR per gram): **Rp {spot_per_gram:,.0f}**")

    # Ambil harga kompetitor (PAKAI SCRAPER!!)
    indogold = get_indogold_price()
    hartadinata = get_hartadinata_price()
    galeri24 = get_galeri24_price()

    competitors = {
        "IndoGold": indogold["jual"],
        "Hartadinata": hartadinata["jual"],
        "Galeri 24": galeri24["jual"]
    }

    st.write("### Premium vs Spot")

    # Hitung premium
    premium_map = {}
    for name, price in competitors.items():
        p = calculate_premium(price, spot_per_gram)
        premium_map[name] = p

        if p is None:
            st.write(f"- {name}: N/A")
        else:
            st.write(f"- {name}: **{p*100:.2f}%**")

    # Input user
    st.write("### Input Harga Kamu")
    my_price = st.number_input("Harga Kamu (Rp)", min_value=0, value=1000000)

    # Hitung harga rata-rata kompetitor
    valid_prices = [p for p in competitors.values() if p is not None]

    if not valid_prices:
        st.error("Tidak ada data competitor valid.")
        return

    avg_comp = sum(valid_prices) / len(valid_prices)
    rec = recommend_price(my_price, avg_comp)

    st.write("### Rekomendasi AI")
    st.write(f"- Rata-rata Competitor: Rp {avg_comp:,.0f}")
    st.success(f"Rekomendasi Harga: **Rp {rec:,.0f}**")
