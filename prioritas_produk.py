import streamlit as st
import pandas as pd
import numpy as np

def prioritas_produk_page():

    st.subheader("🏅 Ranking Prioritas Produk")

    st.caption("Model prioritas ini menggunakan perhitungan berbobot dengan normalisasi otomatis untuk menghasilkan skor yang lebih akurat.")

    # ===========================
    # DATA PRODUK (dummy sementara)
    # ===========================
    data = {
        "Produk": ["1g", "2g", "5g", "10g", "25g", "50g", "100g"],
        "Volume": [20795, 5860, 43158, 49732, 16284, 11265, 21850],
        "Margin": [3.00, 6.59, 5.34, 3.43, 8.51, 2.56, 9.22],
        "Growth": [23.16, -4.98, 24.77, 13.52, 13.35, -4.79, -2.31],
        "Popularity": [93, 52, 86, 56, 70, 58, 88]
    }

    df = pd.DataFrame(data)

    # ===========================
    # PENGATURAN BOBOT (interaktif)
    # ===========================
    st.write("### ⚙️ Pengaturan Bobot Prioritas")

    col1, col2, col3, col4 = st.columns(4)
    w_volume = col1.slider("Bobot Volume", 0.0, 1.0, 0.35)
    w_margin = col2.slider("Bobot Margin", 0.0, 1.0, 0.25)
    w_growth = col3.slider("Bobot Growth", 0.0, 1.0, 0.20)
    w_popularity = col4.slider("Bobot Popularity", 0.0, 1.0, 0.20)

    # Normalisasi bobot
    total = w_volume + w_margin + w_growth + w_popularity
    w_volume /= total
    w_margin /= total
    w_growth /= total
    w_popularity /= total

    # ===========================
    # NORMALISASI NILAI
    # ===========================
    def normalize(series):
        return (series - series.min()) / (series.max() - series.min())

    df["N_Volume"] = normalize(df["Volume"])
    df["N_Margin"] = normalize(df["Margin"])
    df["N_Growth"] = normalize(df["Growth"])
    df["N_Popularity"] = normalize(df["Popularity"])

    # ===========================
    # SKOR PRIORITAS
    # ===========================
    df["PPS"] = (
        df["N_Volume"] * w_volume +
        df["N_Margin"] * w_margin +
        df["N_Growth"] * w_growth +
        df["N_Popularity"] * w_popularity
    )

    df_sorted = df.sort_values("PPS", ascending=False)

    # ===========================
    # TAMPILKAN TABEL RANKING
    # ===========================
    st.write("### 📊 Tabel Ranking Prioritas Produk")
    st.dataframe(
        df_sorted[["Produk", "Volume", "Margin", "Growth", "Popularity", "PPS"]],
        use_container_width=True
    )

    # ===========================
    # VISUALISASI GRAFIK
    # ===========================
    st.write("### 📈 Grafik Prioritas Produk (PPS Score)")
    st.bar_chart(df_sorted.set_index("Produk")["PPS"])

    st.info("💡 Anda dapat menyesuaikan bobot untuk melihat bagaimana perubahan strategi mempengaruhi prioritas produk.")



