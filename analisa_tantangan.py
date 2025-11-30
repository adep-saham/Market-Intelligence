import streamlit as st
import pandas as pd
import plotly.express as px

def run_analisa(df_harga, df_trans, df_pelanggan):

    # ============================
    # NORMALISASI KOLOM
    # ============================

    # Harga emas
    df_harga = df_harga.rename(columns={
        "Date": "Tanggal",
        "Harga Jual Antam": "Harga_Jual_Antam",
        "Harga Buyback": "Harga_Buyback"
    })

    # Transaksi: normalisasi kolom umum
    df_trans = df_trans.rename(columns={
        "ID Customer": "Customer_ID",
        "Jumlah (pcs)": "Qty",
        "Tanggal": "Tanggal",
        "Keterangan Barang/Jasa": "Produk",
        "Berat (kg)": "Berat"
    })

    # Pelanggan
    df_pelanggan = df_pelanggan.rename(columns={
        "ID Customer": "Customer_ID",
        "Tanggal Lahir": "Tanggal_Lahir"
    })

    # ============================
    # DETEKSI K0LOM HARGA OTOMATIS
    # ============================

    harga_candidates = [
        "Harga_Jual",
        "Total Harga (Rupiah)",
        "Total_Harga",
        "TotalHarga",
        "harga_jual",
        "harga",
    ]

    kolom_harga = None
    for c in df_trans.columns:
        if c.strip() in harga_candidates:
            kolom_harga = c
            break

    # Jika tetap tidak ketemu → error yang rapi
    if kolom_harga is None:
        st.error(f"❌ Tidak menemukan kolom harga di data transaksi. Kolom tersedia: {df_trans.columns.tolist()}")
        st.stop()

    # Standardisasi
    df_trans.rename(columns={kolom_harga: "Harga_Jual"}, inplace=True)

    # ============================
    # CLEANING
    # ============================

    df_harga["Tanggal"] = pd.to_datetime(df_harga["Tanggal"], errors="coerce")
    df_trans["Tanggal"] = pd.to_datetime(df_trans["Tanggal"], errors="coerce")

    df_trans["Total_Nilai"] = df_trans["Harga_Jual"]

    if "Tanggal_Lahir" in df_pelanggan.columns:
        df_pelanggan["Tanggal_Lahir"] = pd.to_datetime(df_pelanggan["Tanggal_Lahir"], errors="coerce")
        df_pelanggan["Umur"] = (pd.Timestamp("2024-12-31") - df_pelanggan["Tanggal_Lahir"]).dt.days // 365

    df_trans = df_trans.merge(df_pelanggan, on="Customer_ID", how="left")

    # ============================
    # TREND PENJUALAN
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
    # DEMOGRAFI
    # ============================
    st.header("2️⃣ Demografi Pelanggan")

    if "Umur" in df_trans.columns:
        fig2 = px.histogram(df_trans, x="Umur", nbins=20)
        st.plotly_chart(fig2, use_container_width=True)

    if "Provinsi" in df_trans.columns:
        fig3 = px.bar(
            df_trans.groupby("Provinsi")["Total_Nilai"].sum().reset_index(),
            x="Provinsi", y="Total_Nilai"
        )
        st.plotly_chart(fig3, use_container_width=True)

    # ============================
    # RFM
    # ============================
    st.header("3️⃣ RFM")

    rfm = df_trans.groupby("Customer_ID").agg(
        Frequency=("Tanggal", "count"),
        Monetary=("Total_Nilai", "sum"),
        Last_Tanggal=("Tanggal", "max")
    ).reset_index()

    rfm["Recency"] = (pd.Timestamp("2024-12-31") - rfm["Last_Tanggal"]).dt.days

    st.dataframe(rfm.head())

    # ============================
    # PRODUK TERLARIS
    # ============================
    st.header("4️⃣ Produk Terlaris")

    if "Produk" in df_trans.columns:
        df_prod = df_trans.groupby("Produk")["Total_Nilai"].sum().reset_index()
        fig5 = px.bar(df_prod, x="Produk", y="Total_Nilai")
        st.plotly_chart(fig5, use_container_width=True)

    st.success("Analisa selesai ✔")


