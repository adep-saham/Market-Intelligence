import streamlit as st
from mi_single_python import run_mi_system

st.set_page_config(page_title="MI Logam Mulia", layout="wide")

st.title("📊 Modernisasi Market Intelligence - UBPP Logam Mulia")

# Jalankan sistem
result = run_mi_system()

# ===============================
#   HARGA GLOBAL & KOMPETITOR
# ===============================
st.subheader("📈 Harga Global & Gap Kompetitor")
st.dataframe(result["price_gap"])

# ===============================
#   FORECAST
# ===============================
st.subheader("🔮 Forecast Permintaan 7 Hari")
st.line_chart(result["forecast"]["forecast_qty"])

# ===============================
#   EARLY WARNING SYSTEM
# ===============================
st.subheader("⚠ Early Warning System")
if result["alerts"]:
    for alert in result["alerts"]:
        st.error(alert)
else:
    st.success("Tidak ada alert. Kondisi stabil.")

# ===============================
#   REKOMENDASI HARGA
# ===============================
st.subheader("💰 Rekomendasi Harga Harian")
st.metric(label="Harga Rekomendasi", value=f"Rp {result['recommended_price']:,}")
