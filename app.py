import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io
import tempfile
import zipfile
import xml.etree.ElementTree as ET
import re
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

from competitor_scraper import get_indogold_price, get_hartadinata_price, get_galeri24_price
from forecast_demand import forecast_demand_page
from prioritas_produk import prioritas_produk_page
from segmentasi import segmentasi_pelanggan_lm
from ews_module import ews_pro
from analisa_tantangan import run_analisa

# =====================
# GOLD OHLC API (BARU)
# =====================
from gold_api import fetch_gold_ohlc

# =====================
# UTIL
# =====================
def convert_number(x):
    if not isinstance(x, str):
        return x
    x = x.strip()
    if re.match(r'^[A-Za-z ]+$', x):
        return x
    if re.match(r'^\d[\d\.]*,\d+$', x):
        return float(x.replace('.', '').replace(',', '.'))
    if re.match(r'^\d[\d\.]+$', x):
        return float(x.replace('.', ''))
    return x


@st.cache_data(show_spinner=False)
def load_xlsx(file):
    df_raw = pd.read_excel(file, header=None)
    header_row = df_raw.applymap(lambda x: isinstance(x, str)).sum(axis=1).idxmax()
    df = pd.read_excel(file, header=header_row)
    df = df.loc[:, ~df.columns.str.contains("Unnamed")]
    df = df.fillna("data kosong")
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].apply(convert_number)
    return df


# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="MI Logam Mulia",
    layout="wide"
)

# =====================
# SIDEBAR
# =====================
menu = st.sidebar.selectbox(
    "📌 Menu",
    [
        "Dashboard",
        "Competitor",
        "Customer & Product Intelligence",
        "EWS",
        "Analisa Tantangan Manajemen"
    ]
)

# =====================
# LOAD DATA CORE
# =====================
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

# =====================
# DASHBOARD
# =====================
if menu == "Dashboard":

    st.title("📊 Dashboard Market Intelligence – Logam Mulia")

    # ===== GOLD KPI =====
    gold_usd = kitco.get("mid", 0)
    gold_idr = gold_usd * usdidr
    gold_per_gram_idr = (gold_usd / 31.1034768) * usdidr

    c1, c2, c3 = st.columns(3)
    c1.metric("Gold Spot (USD)", f"${gold_usd:,.2f}")
    c2.metric("Gold Spot (IDR)", f"Rp {gold_idr:,.0f}")
    c3.metric("Gold / gram (IDR)", f"Rp {gold_per_gram_idr:,.0f}")

    # ===== GLOBAL PRICE TREND =====
    st.markdown("### 📈 Tren Harga Global")

    fig_global = go.Figure()
    fig_global.add_trace(go.Scatter(
        x=g["date"],
        y=g["price"],
        mode="lines",
        line=dict(width=3)
    ))
    fig_global.update_layout(height=260)
    st.plotly_chart(fig_global, use_container_width=True)

    # ===== GOLD OHLC =====
        
    with col_t:
        st.markdown("### 🟡 Gold OHLC – XAUUSD")
    
    with col_tf:
        gold_tf = st.selectbox(
            "TF",
            ["1m", "5m", "15m", "1h", "4h", "1d"],
            index=5,
            key="gold_tf_main"
        )
        
    try:
        df_gold = fetch_gold_ohlc(interval=gold_tf, limit=200)

        fig_gold = go.Figure(data=[
            go.Candlestick(
                x=df_gold["time"],
                open=df_gold["Open"],
                high=df_gold["High"],
                low=df_gold["Low"],
                close=df_gold["Close"],
                name="XAUUSD"
            )
        ])

        fig_gold.update_layout(
            height=420,
            xaxis_rangeslider_visible=False,
            template="plotly_dark"
        )

        st.plotly_chart(fig_gold, use_container_width=True)

    except Exception as e:
        st.error(f"Gagal load Gold OHLC: {e}")

    # ===== COMPETITOR GAP =====
    st.markdown("### 🛒 Gap Kompetitor")
    st.dataframe(gap.sort_values("gap"), use_container_width=True)


# =====================
# COMPETITOR PAGE
# =====================
elif menu == "Competitor":

    st.title("🏷 Competitor & Pricing Intelligence")

    indogold = get_indogold_price()
    hartadinata = get_hartadinata_price()
    galeri24 = get_galeri24_price()

    st.subheader("📦 Price Comparison (API)")

    col1, col2, col3 = st.columns(3)

    # ============================
    # INDO GOLD
    # ============================
    with col1:
        st.write("### IndoGold")
        st.metric("Harga Jual", f"Rp {indogold['jual']:,}" if indogold else "N/A")
        st.metric("Harga Beli", f"Rp {indogold['beli']:,}" if indogold else "N/A")
        st.caption("Update: —")

    # ============================
    # HARTADINATA
    # ============================
    with col2:
        st.write("### Hartadinata (Emasku)")
        st.metric("Harga Jual", f"Rp {hartadinata['jual']:,}" if hartadinata else "N/A")
        st.metric("Harga Beli", f"Rp {hartadinata['beli']:,}" if hartadinata else "N/A")
        st.caption(f"Update: {hartadinata['last_update']}" if hartadinata else "Update: —")

    # ============================
    # GALERI 24
    # ============================
    with col3:
        st.write("### Galeri 24 (Pegadaian)")
        st.metric("Harga Jual", f"Rp {int(galeri24['jual']):,}" if galeri24 else "N/A")
        st.metric("Harga Beli", f"Rp {int(galeri24['beli']):,}" if galeri24 else "N/A")
        st.caption(f"Update: {galeri24['last_update']}" if galeri24 else "Update: —")

    # ===========================================================
    # PRICE ELASTICITY
    # ===========================================================
    st.write("---")
    st.title("🏷 Price Elasticity")

    gold_usd = kitco.get("mid", 0)
    usdidr = fetch_usdidr()
    gold_per_gram_usd = gold_usd / 31.1034768
    spot_per_gram_idr = gold_per_gram_usd * usdidr

    st.metric("Spot Gold (IDR/gram)", f"Rp {spot_per_gram_idr:,.0f}")

    st.write("### Premium vs Spot")

    competitors = {
        "IndoGold": indogold["jual"] if indogold else None,
        "Hartadinata": hartadinata["jual"] if hartadinata else None,
        "Galeri 24": galeri24["jual"] if galeri24 else None
    }

    def calc_premium(price, spot):
        if not price or not spot:
            return None
        return (price / spot) - 1

    for name, price in competitors.items():
        premium = calc_premium(price, spot_per_gram_idr)
        if premium is None:
            st.write(f"- {name}: N/A")
        else:
            st.write(f"- {name}: **{premium*100:.2f}%**")

    st.write("### Input Harga Kamu")
    my_price = st.number_input("Harga Kamu (Rp)", min_value=0, value=2300000)

    # ===========================================================
    # AI PRICE RECOMMENDATION
    # ===========================================================
    st.write("---")
    st.subheader("🤖 Rekomendasi Harga (Berdasarkan AI)")

    from pricing_ai import aiml_price_ai

    if st.button("Generate with Ade AI"):
        ai_text = aiml_price_ai(
            spot_per_gram_idr,
            competitors["IndoGold"],
            competitors["Hartadinata"],
            competitors["Galeri 24"],
            my_price
        )
        st.success(ai_text)


# =====================
# CUSTOMER & PRODUCT
# =====================
elif menu == "Customer & Product Intelligence":

    st.title("Customer & Product Intelligence")

    segmentasi_pelanggan_lm()
    forecast_demand_page()
    prioritas_produk_page()


# =====================
# EWS
# =====================
elif menu == "EWS":

    st.title("🔍 Early Warning System")
    alerts = ews_pro(g, comp, traffic)

    if not alerts:
        st.success("Semua indikator stabil")
    else:
        st.warning("Early Warning Terdeteksi")
        st.dataframe(alerts)


# =====================
# ANALISA TANTANGAN
# =====================
elif menu == "Analisa Tantangan Manajemen":

    st.title("Analisa Tantangan Manajemen")

    harga_file = st.file_uploader("Upload Data Harga", type=["xlsx"])
    transaksi_file = st.file_uploader("Upload Data Transaksi", type=["xlsx"])
    pelanggan_file = st.file_uploader("Upload Data Pelanggan", type=["xlsx"])

    if harga_file and transaksi_file and pelanggan_file:
        if st.button("🚀 Mulai Analisa"):
            df_harga = load_xlsx(harga_file)
            df_trans = load_xlsx(transaksi_file)
            df_pelanggan = load_xlsx(pelanggan_file)

            run_analisa(df_harga, df_trans, df_pelanggan)








































































































































