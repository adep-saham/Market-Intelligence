import streamlit as st
import pandas as pd

# Import dari modul MI (pastikan file bernama mi_engine.py)
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

st.set_page_config(page_title="MI Logam Mulia", layout="wide")

st.title("📊 Modernisasi Market Intelligence – UBPP Logam Mulia")

# ===== Load Data =====
try:
    global_price = load_global_price()
    competitor = load_competitor()
    sales = load_sales()
    traffic = load_traffic()
    st.success("Data berhasil dimuat.")
except Exception as e:
    st.error(f"Data error: {e}")
    st.stop()

# ===== Analisis =====
lm_price = global_price["price"].iloc[-1]
gap_df = detect_price_gap(lm_price, competitor)
forecast_df = forecast_demand(sales)

alerts = generate_alerts(
    check_global_price_spike(global_price.copy()),
    near_price_war(gap_df.copy()),
    check_traffic_drop(traffic.copy())
)

recommended = recommend_price(lm_price, competitor)

# ===== Display =====
st.header("📈 Harga Global")
st.line_chart(global_price.set_index("date")["price"])

st.header("📉 Gap Kompetitor")
st.dataframe(gap_df)

st.header("🔮 Forecast Permintaan")
st.line_chart(forecast_df["forecast_qty"])

st.header("⚠ Early Warning System")
if alerts:
    for a in alerts:
        st.error(a)
else:
    st.success("Tidak ada alert.")

st.header("💰 Rekomendasi Harga")
st.metric("Harga rekomendasi", f"Rp {recommended:,.0f}")
