import streamlit as st
import pandas as pd
import numpy as np

# ==========================================================
# PRIORITAS PRODUK UTAMA (PRODUCT PRIORITY SCORE – PPS)
# ==========================================================

def prioritas_produk_page():

    st.title("Prioritas Produk Utama")

    st.write("""
    Analisis prioritas produk LM berdasarkan volume penjualan, margin,
    pertumbuhan permintaan, volatilitas harga, dan popularitas retail.
    """)

    # ----------------------------------------------------------
    # 1. Generate Dummy Product Data (Auto)
    # ----------------------------------------------------------
    products = ["1g", "2g", "5g", "10g", "25g", "50g", "100g"]
    np.random.seed(42)

    df = pd.DataFrame({
        "Produk": products,
        "Volume": np.random.randint(5000, 50000, len(products)),
        "Margin": np.random.uniform(0.02, 0.12, len(products)),      # margin 2%–12%
        "Growth": np.random.uniform(-0.05, 0.25, len(products)),     # growth -5%–25%
        "Volatilitas": np.random.uniform(0.5, 1.5, len(products)),   # volatilitas skala
        "Popularity": np.random.randint(50, 100, len(products))      # tingkat preferensi 50–100
    })

    # Normalisasi setiap faktor agar setara
    for col in ["Volume", "Margin", "Growth", "Popularity"]:
        df[col + "_Norm"] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

    # Volatilitas → makin kecil makin bagus
    df["Volatilitas_Norm"] = 1 - (df["Volatilitas"] - df["Volatilitas"].min()) / (df["Volatilitas"].max() - df["Volatilitas"].min())

    # ----------------------------------------------------------
    # 2. Hitung Product Priority Score (PPS)
    # ----------------------------------------------------------
    df["PPS"] = (
        0.35 * df["Volume_Norm"] +
        0.30 * df["Margin_Norm"] +
        0.20 * df["Growth_Norm"] +
        0.10 * df["Popularity_Norm"] +
        0.05 * df["Volatilitas_Norm"]
    )

    df = df.sort_values("PPS", ascending=False)

    # ----------------------------------------------------------
    # 3. Tabel Hasil
    # ----------------------------------------------------------
    st.write("### 🥇 Ranking Prioritas Produk")

    st.dataframe(
        df[["Produk", "Volume", "Margin", "Growth", "Popularity", "PPS"]]
        .style.format({
            "Margin": "{:.2%}",
            "Growth": "{:.2%}",
            "PPS": "{:.3f}"
        }),
        use_container_width=True
    )

    # ----------------------------------------------------------
    # 4. Visualisasi
    # ----------------------------------------------------------
    st.write("### 📊 Grafik Kontribusi Volume")

    st.bar_chart(df.set_index("Produk")["Volume"])

    # ----------------------------------------------------------
    # 5. Insight Otomatis
    # ----------------------------------------------------------
    st.write("### 🔍 Insight Otomatis")

    top_product = df.iloc[0]["Produk"]
    top_growth = df.sort_values("Growth", ascending=False).iloc[0]["Produk"]
    lowest_volatil = df.sort_values("Volatilitas", ascending=True).iloc[0]["Produk"]

    st.success(f"Produk dengan prioritas tertinggi saat ini adalah **{top_product}** berdasarkan PPS.")
    st.info(f"Produk dengan pertumbuhan permintaan tertinggi adalah **{top_growth}**.")
    st.warning(f"Produk dengan volatilitas harga terendah (stabil) adalah **{lowest_volatil}**.")

