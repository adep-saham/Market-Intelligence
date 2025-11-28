import streamlit as st
import pandas as pd
from mi_single_python import (
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

# ============================================
# CONFIG
# ============================================
st.set_page_config(page_title="MI Logam Mulia", layout="wide")

st.title("📊 Modernisasi Market Intelligence – UBPP Logam Mulia")
st.write("Versi Stabil – Dashboard MI berbasis data CSV & dummy.")

# ============================================
# LOAD DATA (DENGAN ERROR HANDLING)
# ============================================
try:
    global_price = load_global_price()
    competitor = load_competitor()
    sales = load_sales()
    traffic = load_traffic()
    st.success("✔ Data berhasil dimuat")
except Exception as e:
    st.error(f"❌ Gagal memuat data: {e}")
    st.stop()

# ============================================
# DISPLAY RAW DATA
# ============================================
with st.expander("📂 Lihat Data Mentah"):
    st.write("**Harga Global**")
    st.dataframe(global_price)
    st.write("**Kompetitor**")
    st.dataframe(competitor)
    st.write("**Penjualan LM**")
    st.dataframe(sales)
    st.write("**Traffic Website**")
    st.dataframe(traffic)

# ============================================
# HARGA GLOBAL & GAP KOMPETITOR
# ============================================
st.header("📈 Harga Emas Global & Gap Kompetitor")

lm_price = global_price["price"].iloc[-1]
gap_df = detect_price_gap(lm_price, competitor)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Grafik Harga Global")
    st.line_chart(global_price.set_index("date")["price"])

with col2:
    st.subheader("Analisis Gap Kompetitor")
    st.dataframe(gap_df)

# ============================================
# FORECAST PERMINTAAN
# ============================================
st.header("🔮 Forecast Permintaan 7 Hari")

try:
    forecast_df = forecast_demand(sales)
    st.line_chart(forecast_df["forecast_qty"])
except Exception as e:
    st.error(f"❌ Forecast error: {e}")

# ============================================
# EARLY WARNING SYSTEM (EWS)
# ============================================
st.header("⚠ Early Warning System")

alerts = generate_alerts(
    check_global_price_spike(global_price.copy()),
    near_price_war(gap_df.copy()),
    check_traffic_drop(traffic.copy())
)

if alerts:
    for a in alerts:
        st.error(a)
else:
    st.success("Tidak ada alert. Sistem stabil.")

# ============================================
# REKOMENDASI HARGA HARlAN
# ============================================
st.header("💰 Rekomendasi Harga Harian")

try:
    recommended = recommend_price(lm_price, competitor)
    st.metric("Harga Rekomendasi", f"Rp {recommended:,.0f}")
except Exception as e:
    st.error(f"❌ Error rekomendasi harga: {e}")

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.write("© 2024 UBPP Logam Mulia – Market Intelligence System")
