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
    recommend_price
)

# ======================================
# PREMIUM THEME (CSS)
# ======================================
st.set_page_config(page_title="MI Logam Mulia", layout="wide")

premium_css = """
<style>
/* Remove Streamlit default padding */
main > div { padding: 1rem 3rem; }

/* Card Style */
.card {
    background: #ffffff;
    padding: 20px 25px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    border-left: 6px solid #F4A300;
    margin-bottom: 20px;
}

/* KPI Style */
.kpi {
    background: linear-gradient(135deg, #0A3D62, #145A8D);
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    color: white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.25);
}
.kpi h2 { font-size: 32px; margin: 0; font-weight: 700; }
.kpi p { font-size: 16px; margin: 0; }

/* Section Title */
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

# ======================================
# SIDEBAR MENU
# ======================================
menu = st.sidebar.selectbox(
    "📌 Menu",
    ["Dashboard", "Competitor", "Forecast", "EWS", "Pricing"]
)

# Load data
try:
    global_price = load_global_price()
    competitor = load_competitor()
    sales = load_sales()
    traffic = load_traffic()
except Exception as e:
    st.error(f"Gagal memuat data: {e}")
    st.stop()

lm_price = global_price["price"].iloc[-1]
gap_df = detect_price_gap(lm_price, competitor)
forecast_df = forecast_demand(sales)
alerts = generate_alerts(
    check_global_price_spike(global_price.copy()),
    near_price_war(gap_df.copy()),
    check_traffic_drop(traffic.copy())
)
recommended_price = recommend_price(lm_price, competitor)

# ======================================
# DASHBOARD PAGE
# ======================================
if menu == "Dashboard":
    st.title("📊 Dashboard Market Intelligence – Premium View")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="kpi"><p>Harga Global</p><h2>Rp {:,.0f}</h2></div>'.format(lm_price), unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="kpi"><p>Rata-rata Kompetitor</p><h2>Rp {:,.0f}</h2></div>'.format(competitor["price"].mean()), unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="kpi"><p>Rekomendasi Harga</p><h2>Rp {:,.0f}</h2></div>'.format(recommended_price), unsafe_allow_html=True)

    st.markdown('<div class="section-title">📈 Tren Harga Global</div>', unsafe_allow_html=True)
    st.line_chart(global_price.set_index("date")["price"])

    st.markdown('<div class="section-title">🛒 Gap Kompetitor</div>', unsafe_allow_html=True)
    st.dataframe(gap_df)

# ======================================
# COMPETITOR PAGE
# ======================================
elif menu == "Competitor":
    st.title("🏷 Competitor Intelligence")

    st.markdown('<div class="card">Analisis harga kompetitor berdasarkan gap terhadap Logam Mulia.</div>', unsafe_allow_html=True)
    st.dataframe(gap_df)

# ======================================
# FORECAST PAGE
# ======================================
elif menu == "Forecast":
    st.title("🔮 Forecast Demand")

    st.markdown('<div class="section-title">Prediksi Permintaan 7 Hari</div>', unsafe_allow_html=True)
    st.line_chart(forecast_df["forecast_qty"])

# ======================================
# EWS PAGE
# ======================================
elif menu == "EWS":
    st.title("⚠ Early Warning System")

    if alerts:
        for a in alerts:
            st.error(a)
    else:
        st.success("Tidak ada alert. Kondisi stabil.")

# ======================================
# PRICING PAGE
# ======================================
elif menu == "Pricing":
    st.title("💰 Pricing Intelligence")

    st.markdown('<div class="card">Rekomendasi harga berdasarkan data kompetitor & global.</div>', unsafe_allow_html=True)

    st.metric("Harga Rekomendasi", f"Rp {recommended_price:,.0f}")
    st.dataframe(gap_df)
