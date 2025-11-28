import streamlit as st
import pandas as pd

from mi_engine import (
    load_global_price,
    load_competitor,
    load_sales,
    load_traffic,
    detect_price_gap,
    forecast_demand,
    generate_alerts,
    near_price_war,
    check_global_price_spike,
    check_traffic_drop,
    recommend_price,
    fetch_gold_price,
    fetch_usdidr
)

# ===========================================================
# UI SETUP
# ===========================================================
st.set_page_config(page_title="MI Logam Mulia", layout="wide")

premium_css = """
<style>
main > div { padding: 1rem 3rem; }

/* CARD STYLE */
.card {
    background: #ffffff;
    padding: 20px 25px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    border-left: 6px solid #F4A300;
    margin-bottom: 20px;
}

/* KPI STYLE */
.kpi {
    background: linear-gradient(135deg, #0A3D62, #145A8D);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.25);
}
.kpi h2 { font-size: 32px; margin: 0; font-weight: 700; }
.kpi p { font-size: 15px; margin: 0; opacity: 0.85; }

/* SECTION TITLE */
.section-title {
    font-size: 26px;
    font-weight: 700;
    color: #0A3D62;
    margin-top: 35px;
    margin-bottom: 15px;
}
</style>
"""

premium_css += """
<style>

.gold-card {
    background: linear-gradient(145deg, #f7d07a, #f0b63a);
    border-radius: 14px;
    padding: 18px 20px;
    text-align: center;
    color: #3a2f0b;
    box-shadow: 0 6px 18px rgba(0,0,0,0.25), 
                inset 0 2px 4px rgba(255,255,255,0.6);
    font-weight: 600;
    transition: transform .15s ease-in-out;
}
.gold-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 28px rgba(0,0,0,0.35);
}

.gold-title {
    font-size: 15px;
    opacity: 0.85;
}

.gold-value {
    font-size: 26px;
    font-weight: 800;
    margin-top: 6px;
    text-shadow: 0px 0px 3px rgba(255,255,255,0.7);
}

</style>
"""


st.markdown(premium_css, unsafe_allow_html=True)


# ===========================================================
# SIDEBAR
# ===========================================================
menu = st.sidebar.selectbox(
    "📌 Menu",
    ["Dashboard", "Competitor", "Forecast", "EWS", "Pricing"]
)

# ===========================================================
# LOAD DATA
# ===========================================================
g = load_global_price()
comp = load_competitor()
sales = load_sales()
traffic = load_traffic()

kitco = fetch_gold_price()
usdidr = fetch_usdidr()

lm_price = g["price"].iloc[-1]
gap = detect_price_gap(lm_price, comp)
forecast_df = forecast_demand(sales)

alerts = generate_alerts(
    check_global_price_spike(g.copy()),
    near_price_war(gap.copy()),
    check_traffic_drop(traffic.copy())
)

recommended_price = recommend_price(lm_price, comp)

# Kitco → IDR
if kitco.get("error"):
    kitco_idr = None
else:
    kitco_idr = kitco["mid"] * usdidr


# ===========================================================
# DASHBOARD PAGE
# ===========================================================
if menu == "Dashboard":

    st.title("📊 Dashboard Market Intelligence – Premium")

    # ===============================
    # FIX: DEFINE GOLD VARIABLES
    # ===============================
    gold_usd = kitco.get("mid", 0)
    gold_idr = gold_usd * usdidr
    gold_per_gram_usd = gold_usd / 31.1034768
    gold_per_gram_idr = gold_per_gram_usd * usdidr

    day1_usd = kitco.get("day1", None)
    day2_usd = kitco.get("day2", None)

    day1_idr = day1_usd * usdidr if day1_usd else None
    day2_idr = day2_usd * usdidr if day2_usd else None

    # HARGA EMAS - NEW CLEAN UI
    c1, c2, c3, c4, c5 = st.columns(5)

    
    # HARGA EMAS - NEW CLEAN UI

  # ================================
# GOLD PRICE – PREMIUM GOLD EDITION
# ================================

c1, c2, c3, c4, c5 = st.columns(5)

# Spot USD
with c1:
    st.markdown(f"""
    <div class="gold-card">
        <div class="gold-title">Spot (USD)</div>
        <div class="gold-value">${gold_usd:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

# Spot IDR
with c2:
    st.markdown(f"""
    <div class="gold-card">
        <div class="gold-title">Spot (IDR)</div>
        <div class="gold-value">Rp {gold_idr:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

# Per Gram IDR
with c3:
    st.markdown(f"""
    <div class="gold-card">
        <div class="gold-title">Per Gram (IDR)</div>
        <div class="gold-value">Rp {gold_per_gram_idr:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

# Day-1
with c4:
    if day1_usd:
        v = f"${day1_usd:,.2f}"
    else:
        v = "N/A"
    st.markdown(f"""
    <div class="gold-card">
        <div class="gold-title">Day-1 Price</div>
        <div class="gold-value">{v}</div>
    </div>
    """, unsafe_allow_html=True)

# Day-2
with c5:
    if day2_usd:
        v = f"${day2_usd:,.2f}"
    else:
        v = "N/A"
    st.markdown(f"""
    <div class="gold-card">
        <div class="gold-title">Day-2 Price</div>
        <div class="gold-value">{v}</div>
    </div>
    """, unsafe_allow_html=True)


    # Grafik & tabel setelah semua KPI
    st.markdown('<div class="section-title">📈 Tren Harga Global</div>', unsafe_allow_html=True)
    st.line_chart(g.set_index("date")["price"], use_container_width=True)

    st.markdown('<div class="section-title">🛒 Gap Kompetitor</div>', unsafe_allow_html=True)
    st.dataframe(gap.sort_values("gap"), use_container_width=True)



# ===========================================================
# COMPETITOR PAGE
# ===========================================================
elif menu == "Competitor":
    st.title("🏷 Competitor Intelligence")
    st.dataframe(gap.sort_values("gap"), use_container_width=True)


# ===========================================================
# FORECAST PAGE
# ===========================================================
elif menu == "Forecast":
    st.title("🔮 Forecast Demand Harian")

    st.line_chart(forecast_df["forecast_qty"], use_container_width=True)

    st.write("📌 *Model menggunakan regresi linear tanpa sklearn (lightweight mode).*")


# ===========================================================
# EWS PAGE
# ===========================================================
elif menu == "EWS":
    st.title("⚠ Early Warning System")

    if alerts:
        for a in alerts:
            st.error(a)
    else:
        st.success("Tidak ada alert. Semua stabil.")


# ===========================================================
# PRICING PAGE
# ===========================================================
elif menu == "Pricing":
    st.title("💰 Pricing Intelligence")

    st.metric("Harga Rekomendasi", f"Rp {recommended_price:,.0f}")

    st.markdown("### 📌 Gap Kompetitor")
    st.dataframe(gap.sort_values("gap"), use_container_width=True)

























