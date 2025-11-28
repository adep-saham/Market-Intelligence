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

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="kpi">
            <p>Harga Global (CSV)</p>
            <h2>Rp {lm_price:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi">
            <p>Avg Kompetitor</p>
            <h2>Rp {comp["price"].mean():,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi">
            <p>Harga Rekomendasi</p>
            <h2>Rp {recommended_price:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col4:

        # ==========================
        # Yahoo Gold (COMEX)
        # ==========================
        if kitco["mid"] > 0:
            st.markdown(f"""
            <div class="kpi">
                <p>Yahoo Gold (COMEX)</p>
                <h2>${kitco["mid"]:.2f}</h2>
            </div>
            """, unsafe_allow_html=True)

            # Konversi ke IDR
            gold_idr = kitco["mid"] * usdidr
            st.metric("Gold Price (IDR)", f"Rp {gold_idr:,.0f}")

        else:
            st.markdown("""
            <div class="kpi">
                <p>Yahoo Gold (COMEX)</p>
                <h2>N/A</h2>
            </div>
            """, unsafe_allow_html=True)
           
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











