import streamlit as st
import pandas as pd
import plotly.express as px

def run_analisa(df_harga, df_trans, df_pelanggan):

    # ============================
    # NORMALISASI K0L0M HARGA EMAS
    # ============================
    df_harga = df_harga.rename(columns={
        "Date": "Tanggal",
        "Harga Jual Antam": "Harga_Jual_Antam",
        "Harga Buyback": "Harga_Buyback"
    })

    # ============================
    # NORMALISASI DATA TRANSAKSI
    # ============================
    df_trans = df_trans.rename(columns={
        "ID Customer": "Customer_ID",
        "Jumlah dalam pcs": "Qty",
        "Keterangan Barang atau Jasa": "Produk",
        "Berat dalam Kg": "Berat",
        "Total Harga dalam Rupiah": "Total_Harga",
        "Tanggal": "Tanggal"
    })

    # Pastikan kolom tanggal valid
    df_trans["Tanggal"] = pd.to_datetime(df_trans["Tanggal"], errors="coerce")

    # Nilai transaksi = Total Harga dalam Rupiah
    df_trans["Total_Nilai"] = df_trans["Total_Harga"]

    # ============================
    # NORMALISASI DATA PELANGGAN
    # ============================
    df_pelanggan = df_pelanggan.rename(columns={
        "ID Customer": "Customer_ID",
        "Tanggal Lahir": "Tanggal_Lahir"
    })

    if "Tanggal_Lahir" in df_pelanggan.columns:
        df_pelanggan["Tanggal_Lahir"] = pd.to_datetime(df_pelanggan["Tanggal_Lahir"], errors="coerce")
        df_pelanggan["Umur"] = (
            pd.Timestamp("2024-12-31") - df_pelanggan["Tanggal_Lahir"]
        ).dt.days // 365

    # Merge transaksi + pelanggan
    df_trans = df_trans.merge(df_pelanggan, on="Customer_ID", how="left")

    # ============================
    # 1. TREND HARGA VS PENJUALAN
    # ============================
    st.header("1️⃣ Trend Harga vs Volume Penjualan")

    df_daily = df_trans.groupby("Tanggal").agg(
        Total_Jual=("Total_Nilai", "sum"),
        Total_Qty=("Qty", "sum")
    ).reset_index()

    df_merge = df_daily.merge(df_harga, on="Tanggal", how="left")

    fig = px.line(
        df_merge,
        x="Tanggal",
        y=["Harga_Jual_Antam", "Total_Qty"],
        title="Harga Emas vs Volume Penjualan"
    )
    st.plotly_chart(fig, use_container_width=True)

    # ============================
    # 2. DEMOGRAFI PELANGGAN
    # ============================
    st.header("2️⃣ Demografi Pelanggan")

    if "Umur" in df_trans.columns:
        fig2 = px.histogram(df_trans, x="Umur", nbins=20, title="Distribusi Umur Pelanggan")
        st.plotly_chart(fig2, use_container_width=True)

    if "Provinsi" in df_trans.columns:
        omzet = df_trans.groupby("Provinsi")["Total_Nilai"].sum().reset_index()
        fig3 = px.bar(omzet, x="Provinsi", y="Total_Nilai", title="Omzet per Provinsi")
        st.plotly_chart(fig3, use_container_width=True)

    # ============================
    # 3. RFM ANALYTICS
    # ============================
    st.header("3️⃣ RFM (Recency, Frequency, Monetary)")

    rfm = df_trans.groupby("Customer_ID").agg(
        Frequency=("Tanggal", "count"),
        Monetary=("Total_Nilai", "sum"),
        Last_Tanggal=("Tanggal", "max")
    ).reset_index()

    rfm["Recency"] = (pd.Timestamp("2024-12-31") - rfm["Last_Tanggal"]).dt.days

    st.dataframe(rfm.head())

    fig4 = px.scatter(rfm, x="Frequency", y="Monetary", size="Monetary",
                      title="Scatter Frequency vs Monetary")
    st.plotly_chart(fig4, use_container_width=True)

    # ============================
    # 4. PRODUK TERLARIS
    # ============================
    st.header("4️⃣ Produk / Jasa Terlaris")

    if "Produk" in df_trans.columns:
        prod = df_trans.groupby("Produk")["Total_Nilai"].sum().reset_index()
        fig5 = px.bar(prod, x="Produk", y="Total_Nilai", title="Omzet per Produk/Jasa")
        st.plotly_chart(fig5, use_container_width=True)

    st.success("Analisa selesai ✔")




