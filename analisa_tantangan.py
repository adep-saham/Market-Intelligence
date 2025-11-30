import streamlit as st
import pandas as pd
import plotly.express as px

def run_analisa(df_harga, df_trans, df_pelanggan):

    # ============================
    # 1. CLEANING
    # ============================
    df_harga["Tanggal"] = pd.to_datetime(df_harga["Tanggal"])
    df_trans["Tanggal"] = pd.to_datetime(df_trans["Tanggal"])
    
    # Buat kolom Total Nilai Transaksi
    df_trans["Total_Nilai"] = df_trans["Qty"] * df_trans["Harga_Jual"]

    # Hitung umur
    if "Tanggal_Lahir" in df_pelanggan.columns:
        df_pelanggan["Tanggal_Lahir"] = pd.to_datetime(df_pelanggan["Tanggal_Lahir"])
        df_pelanggan["Umur"] = (pd.Timestamp("2024-12-31") - df_pelanggan["Tanggal_Lahir"]).dt.days // 365

    # Merge data transaksi & pelanggan
    df_trans = df_trans.merge(df_pelanggan, on="Customer_ID", how="left")

    st.header("1️⃣ Trend Harga vs Volume Penjualan")
    df_daily = df_trans.groupby("Tanggal").agg(
        Total_Jual=("Total_Nilai", "sum"),
        Total_Qty=("Qty", "sum")
    ).reset_index()

    df_merge = df_daily.merge(df_harga, on="Tanggal", how="left")

    fig = px.line(df_merge, x="Tanggal", y=["Harga_Jual_Antam", "Total_Qty"],
                  labels={"value": "Harga / Qty"}, title="Harga Emas vs Volume Penjualan")
    st.plotly_chart(fig, use_container_width=True)

    # ============================
    # 2. DEMOGRAFI
    # ============================
    st.header("2️⃣ Demografi Pelanggan")

    if "Umur" in df_trans.columns:
        fig2 = px.histogram(df_trans, x="Umur", nbins=20, title="Distribusi Umur Pelanggan")
        st.plotly_chart(fig2, use_container_width=True)

    if "Provinsi" in df_trans.columns:
        fig3 = px.bar(df_trans.groupby("Provinsi")["Total_Nilai"].sum().reset_index(),
                      x="Provinsi", y="Total_Nilai", title="Omzet per Provinsi")
        st.plotly_chart(fig3, use_container_width=True)

    # ============================
    # 3. PERILAKU PEMBELIAN (RFM)
    # ============================
    st.header("3️⃣ Perilaku Pembelian (RFM)")

    rfm = df_trans.groupby("Customer_ID").agg(
        Frequency=("Tanggal", "count"),
        Monetary=("Total_Nilai", "sum"),
        Last_Tanggal=("Tanggal", "max")
    ).reset_index()

    rfm["Recency"] = (pd.Timestamp("2024-12-31") - rfm["Last_Tanggal"]).dt.days

    st.write("Tabel RFM (ringkasan):")
    st.dataframe(rfm.head())

    fig4 = px.scatter(rfm, x="Frequency", y="Monetary",
                      size="Monetary", title="Scatter: Frequency vs Monetary")
    st.plotly_chart(fig4, use_container_width=True)

    # ============================
    # 4. PRODUK TERLARIS
    # ============================
    st.header("4️⃣ Produk / Denominasi Terlaris")

    if "Denom" in df_trans.columns:
        df_denom = df_trans.groupby("Denom")["Total_Nilai"].sum().reset_index()
        fig5 = px.bar(df_denom, x="Denom", y="Total_Nilai", title="Kontribusi Omzet per Denom")
        st.plotly_chart(fig5, use_container_width=True)

    st.success("Analisa selesai ✔")
