import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==========================================================
# FORECAST DEMAND – AUTO SIMULATION MODEL
# ==========================================================

def forecast_demand_page():

    st.title("Forecast Demand")

    st.write("""
    Model prediksi permintaan emas LM secara otomatis menggunakan simulasi musiman,
    volatilitas harga global, dan pola pembelian historis.
    """)

    # ----------------------------------------------------------
    # 1. Generate Synthetic Historical Demand Data (12 bulan)
    # ----------------------------------------------------------
    np.random.seed(42)
    months = pd.date_range(datetime.today() - timedelta(days=365), periods=12, freq='M')

    # Musiman: Ramadhan, Lebaran, Akhir Tahun, Imlek
    seasonal_factor = np.array([1.05, 1.10, 1.15, 1.20, 1.25, 1.10, 
                                1.00, 0.95, 1.05, 1.15, 1.30, 1.40])

    base_demand = 9000  # baseline demand LM per bulan (grams)
    noise = np.random.normal(0, 800, 12)  # variasi random

    demand = (base_demand * seasonal_factor) + noise

    df = pd.DataFrame({
        "Month": months,
        "Demand": demand.astype(int)
    })

    # ----------------------------------------------------------
    # 2. Simple Forecast (Next 6 Months)
    # ----------------------------------------------------------
    future_months = pd.date_range(months[-1] + timedelta(days=30), periods=6, freq='M')

    trend = (df["Demand"].pct_change().mean())  # rata-rata growth historis
    forecast = []

    current_value = df["Demand"].iloc[-1]

    for _ in range(6):
        current_value = current_value * (1 + trend + np.random.normal(0, 0.03))
        forecast.append(current_value)

    df_forecast = pd.DataFrame({
        "Month": future_months,
        "Forecast": np.array(forecast).astype(int)
    })

    # ----------------------------------------------------------
    # 3. Visualisasi
    # ----------------------------------------------------------
    st.write("### 📈 Grafik Permintaan & Forecast")

    chart_df = pd.DataFrame({
        "Month": pd.concat([df["Month"], df_forecast["Month"]]),
        "Value": pd.concat([df["Demand"], df_forecast["Forecast"]]),
        "Type": ["Historical"] * len(df) + ["Forecast"] * len(df_forecast)
    })

    st.line_chart(chart_df, x="Month", y="Value", color="Type", height=350)

    # ----------------------------------------------------------
    # 4. Insight Otomatis
    # ----------------------------------------------------------
    st.write("### 🔍 Insight Otomatis")

    growth = df_forecast["Forecast"].iloc[-1] - df["Demand"].iloc[-1]
    growth_pct = (growth / df["Demand"].iloc[-1]) * 100

    if growth_pct > 10:
        msg = "Permintaan diprediksi **naik signifikan**. Perlu meningkatkan stok & produksi."
    elif growth_pct > 0:
        msg = "Permintaan diprediksi **stabil naik**. Produksi dapat disesuaikan secara bertahap."
    else:
        msg = "Permintaan diprediksi **menurun**. Prioritaskan efisiensi produksi."

    st.success(f"Prediksi menunjukkan perubahan permintaan sebesar **{growth_pct:.2f}%**. {msg}")

    # ----------------------------------------------------------
    # 5. Rekomendasi Produksi
    # ----------------------------------------------------------
    st.write("### 🛠 Rekomendasi Produksi & Stok")

    st.markdown("""
    - Tambah buffer stok **10–15%** menjelang hari besar (Imlek, Ramadhan, Lebaran).  
    - Perkuat campaign edukasi investasi emas saat volatilitas global meningkat.  
    - Prioritaskan produk 1g, 5g, dan 10g pada musim permintaan tinggi.  
    - Gunakan forecast bulan-ke-bulan untuk mengelola kapasitas produksi.
    """)

