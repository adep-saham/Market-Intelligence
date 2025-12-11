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

# =====================================
# FUNGSI LOADER XLSX HARUS ADA DI SINI
# =====================================
def convert_number(x):
    if not isinstance(x, str):
        return x

    x = x.strip()

    # Jika hanya huruf → bukan angka
    if re.match(r'^[A-Za-z ]+$', x):
        return x

    # Format 1.234.567,89 → 1234567.89
    if re.match(r'^\d[\d\.]*,\d+$', x):
        x = x.replace('.', '').replace(',', '.')
        try:
            return float(x)
        except:
            return x

    # Format 1.234.567 → 1234567
    if re.match(r'^\d[\d\.]+$', x):
        try:
            return float(x.replace('.', ''))
        except:
            return x

    return x

@st.cache_data(show_spinner=False)
def load_xlsx_cached(file):
    return load_xlsx(file)

# ============================
# FINAL LOADER EXCEL (AMAN)
# ============================
def load_xlsx(file):
    try:
        # Baca awal tanpa header
        df_raw = pd.read_excel(file, header=None)

        # Cari baris header paling valid
        header_row = df_raw.applymap(lambda x: isinstance(x, str)).sum(axis=1).idxmax()

        # Baca ulang dengan header final
        df = pd.read_excel(file, header=header_row)

        # Hapus kolom "Unnamed"
        df = df.loc[:, ~df.columns.str.contains("Unnamed")]

        # Isi semua sel kosong dengan "data kosong"
        df = df.fillna("data kosong")

        # Konversi angka format Indonesia → float
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].apply(convert_number)

        return df

    except Exception as e:
        st.error(f"❌ Error membaca file: {e}")
        return pd.DataFrame()

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
    [
        "Dashboard",
        "Competitor",
        "Customer & Product Intelligence",
        "EWS",
        "Analisa Tantangan Manajemen"
    ]
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

    # DEFINE GOLD VARIABLES (pastikan ini sudah ada)
    gold_usd = kitco.get("mid", 0)
    gold_idr = gold_usd * usdidr
    gold_per_gram_usd = gold_usd / 31.1034768
    gold_per_gram_idr = gold_per_gram_usd * usdidr

    day1_usd = kitco.get("day1", None)
    day2_usd = kitco.get("day2", None)

    day1_idr = day1_usd * usdidr if day1_usd else None
    day2_idr = day2_usd * usdidr if day2_usd else None

    # ================================
    # GOLD PRICE – PREMIUM GOLD EDITION
    # ================================
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.markdown(f"""
        <div class="gold-card">
            <div class="gold-title">Spot (USD)</div>
            <div class="gold-value">${gold_usd:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="gold-card">
            <div class="gold-title">Spot (IDR)</div>
            <div class="gold-value">Rp {gold_idr:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="gold-card">
            <div class="gold-title">Per Gram (IDR)</div>
            <div class="gold-value">Rp {gold_per_gram_idr:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        v = f"${day1_usd:,.2f}" if day1_usd else "N/A"
        st.markdown(f"""
        <div class="gold-card">
            <div class="gold-title">Day-1 Price</div>
            <div class="gold-value">{v}</div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        v = f"${day2_usd:,.2f}" if day2_usd else "N/A"
        st.markdown(f"""
        <div class="gold-card">
            <div class="gold-title">Day-2 Price</div>
            <div class="gold-value">{v}</div>
        </div>
        """, unsafe_allow_html=True)

    # JANGAN HILANGKAN TUTUP IF DI ATAS SEBELUM MASUK ke HALAMAN LAIN
    

    st.markdown('<div class="section-title">📈 Tren Harga Global</div>', unsafe_allow_html=True)

   

    # === Grafik menggunakan Plotly ===
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=g["date"],
        y=g["price"],
        mode="lines",
        line=dict(color="#1f77b4", width=3)
    ))
    
    fig.update_layout(
        title="",
        height=260,
        width=450,   # << ukuran grafik 1/3 layar
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(title=""),
        yaxis=dict(title="")
    )

    st.markdown("<div style='width:33%; float:left;'>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=False)
    st.markdown("</div><div style='clear:both;'></div>", unsafe_allow_html=True)
 
    
    st.markdown('<div class="section-title">🛒 Gap Kompetitor</div>', unsafe_allow_html=True)
    st.dataframe(gap.sort_values("gap"), use_container_width=True)

# ===========================================================
# COMPETITOR PAGE
# ===========================================================

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
    # HARTADINATA (EMASKU)
    # ============================
    with col2:
        st.write("### Hartadinata (Emasku)")
        st.metric("Harga Jual", f"Rp {hartadinata['jual']:,}" if hartadinata else "N/A")
        st.metric("Harga Beli", f"Rp {hartadinata['beli']:,}" if hartadinata else "N/A")
        st.caption(f"Update: {hartadinata['last_update']}" if hartadinata else "Update: —")
    
    # ============================
    # GALERI 24 (Pegadaian)
    # ============================
    with col3:
        st.write("### Galeri 24 (Pegadaian)")
        st.metric("Harga Jual", f"Rp {int(galeri24['jual']):,}" if galeri24 else "N/A")
        st.metric("Harga Beli", f"Rp {int(galeri24['beli']):,}" if galeri24 else "N/A")
        st.caption(f"Update: {galeri24['last_update']}" if galeri24 else "Update: —")

    # ===========================================================
    # PRICE ELASTICITY (INLINE SECTION)
    # ===========================================================

    st.write("---")
    st.title("🏷 Price Elasticity")

    # Hitung spot gold IDR per gram
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
    # AI PRICE RECOMMENDATION BY GPT-4o-mini
    # ===========================================================
    st.write("---")
    st.subheader("🤖 Rekomendasi Harga (Berdasarkan AI)")
    
    from pricing_ai import local_intelligence_recommendation

    if st.button("Generate with Ade AI"):
        ai_text = local_intelligence_recommendation(
            spot_per_gram_idr,
            competitors["IndoGold"],
            competitors["Hartadinata"],
            competitors["Galeri 24"],
            my_price
        )
        st.success(ai_text)



      

# ===========================================================
# CUSTOMER & PRODUCT INTELLIGENCE PAGE
# ===========================================================
elif menu == "Customer & Product Intelligence":

    st.title("Segmentasi Pelanggan LM, Forecast Demand, Prioritas Produk Utama")
    st.write("Analitik terpadu untuk memahami pelanggan, memprediksi permintaan, dan menentukan prioritas produk utama.")

    st.write("---")

    col1, col2, col3 = st.columns(3)

    # ==========================================
    # Segmentasi Pelanggan LM
    # ==========================================
    st.write("---")
    segmentasi_pelanggan_lm()
   

    # ==========================================
    # Forecast Demand
    # ==========================================
    
    st.write("---")
    forecast_demand_page()   
    
    # ==========================================
    # Prioritas Produk Utama
    # ==========================================
    
    st.write("---")
    prioritas_produk_page()
   
# ===========================================================
# EWS PAGE
# ===========================================================

# ==========================================
# EWS PAGE
# ==========================================

elif menu == "EWS":
    st.title("🔍 Hasil Analisis EWS Pro")

     # ==========================================
    # DETEKSI KOLOM TRAFFIC YANG VALID
    # ==========================================
    col_visits = None  # default agar tidak NameError

    traffic_cols = [c.lower() for c in traffic.columns]

    if "visits" in traffic_cols:
        col_visits = traffic.columns[traffic_cols.index("visits")]
    elif "visit" in traffic_cols:
        col_visits = traffic.columns[traffic_cols.index("visit")]
    elif "traffic" in traffic_cols:
        col_visits = traffic.columns[traffic_cols.index("traffic")]
    
    alerts = ews_pro(g, comp, traffic)

    if not alerts:
        st.success("Semua indikator stabil — tidak ada Early Warning.")
    
        st.subheader("📊 Mengapa dianggap stabil?")
    
        # 1. GLOBAL PRICE CHECK
        gold_change = g["price"].pct_change().iloc[-1] * 100
        if abs(gold_change) < 1:
            st.info(f"🟢 **Harga Global Stabil** — perubahan harian hanya {gold_change:.2f}%.")
        else:
            st.write(f"Perubahan harga global {gold_change:.2f}% (di bawah batas Early Warning).")
    
        # 2. COMPETITOR PRICE GAP
        gap_df = comp.copy()
        gap_df["gap"] = abs(gap_df["price"] - g["price"].iloc[-1])
        avg_gap = gap_df["gap"].mean()
    
        if avg_gap < 3000:
            st.info(f"🟢 **Gap Harga Kompetitor Stabil** — rata-rata selisih hanya Rp {avg_gap:,.0f}.")
        else:
            st.write(f"Selisih harga kompetitor Rp {avg_gap:,.0f} (masih di bawah ambang).")
    
        # ==========================================
        # TRAFFIC TREND CHECK
        # ==========================================
        if col_visits is None:
            st.warning("⚠ Tidak dapat menganalisis traffic — kolom visits tidak ditemukan.")
        else:
            traffic_change = traffic[col_visits].pct_change().iloc[-1] * 100
        
            if abs(traffic_change) < 5:
                st.info(f"🟢 Traffic Stabil — perubahan terakhir {traffic_change:.2f}%.")
            else:
                st.warning(f"🟠 Traffic berubah {traffic_change:.2f}% (masih dalam ambang aman).")


# ====================================================
# 4. MENU BARU: ANALISA TANTANGAN MANAJEMEN
# ====================================================
       
elif menu == "Analisa Tantangan Manajemen":

    st.title("Analisa Data")
    st.write("Analisa otomatis menggunakan 3 dataset 2024: Harga Emas, Pelanggan & Transaksi.")

    # Uploaders
    harga_file = st.file_uploader("Upload Data Harga Emas", type=["xlsx"])
    transaksi_file = st.file_uploader("Upload Data Transaksi Penjualan", type=["xlsx"])
    pelanggan_file = st.file_uploader("Upload Data Pelanggan", type=["xlsx"])

    if harga_file and transaksi_file and pelanggan_file:
        st.success("✔ Semua file sudah diupload. Siap dianalisa.")
        
        # =============================
        # Load data Excel (tanpa mi_engine)
        # =============================

        # ============================
        # TOMBOL ANALISA
        # ============================
        if st.button("🚀 Mulai Analisa"):
        
            # ========== VALIDASI FILE ==========
            if harga_file is None:
                st.error("❌ File harga belum diupload.")
                st.stop()
        
            if transaksi_file is None:
                st.error("❌ File transaksi belum diupload.")
                st.stop()
        
            if pelanggan_file is None:
                st.error("❌ File pelanggan belum diupload.")
                st.stop()
        
            # ========== LOAD FILE ==========
            df_harga = load_xlsx_cached(harga_file)
            df_trans = load_xlsx_cached(transaksi_file)
            df_pelanggan = load_xlsx_cached(pelanggan_file)
        
            # ========== DEBUG ==========
            st.write("Ukuran Data Harga:", df_harga.shape)
            st.write("Ukuran Data Transaksi:", df_trans.shape)
            st.write("Ukuran Data Pelanggan:", df_pelanggan.shape)
        
            # ========== VALIDASI DATAFRAME ==========
            if df_harga.empty:
                st.error("❌ Data Harga kosong atau format tidak terbaca.")
                st.stop()
        
            if df_trans.empty:
                st.error("❌ Data Transaksi kosong atau format tidak terbaca.")
                st.stop()
        
            if df_pelanggan.empty:
                st.error("❌ Data Pelanggan kosong atau format tidak terbaca.")
                st.stop()
        
            # ========== JALANKAN ANALISA ==========
            run_analisa(df_harga, df_trans, df_pelanggan)


































































































































