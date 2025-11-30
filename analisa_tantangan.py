import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go  # <--- WAJIB ADA
import matplotlib.pyplot as plt

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

    df_trans["Tanggal"] = pd.to_datetime(df_trans["Tanggal"], errors="coerce")
    df_trans["Total_Nilai"] = df_trans["Total_Harga"]

    # ============================
    # NORMALISASI DATA PELANGGAN
    # ============================
    df_pelanggan = df_pelanggan.rename(columns={
        "ID Customer": "Customer_ID",
        "Tanggal Lahir": "Tanggal_Lahir"
    })

    # =============================
    # TURBO 1: OPTIMASI TIPE DATA (SETELAH RENAME) ← LETAK YANG BENAR
    # =============================
    df_trans["Customer_ID"] = df_trans["Customer_ID"].astype("category")
    df_pelanggan["Customer_ID"] = df_pelanggan["Customer_ID"].astype("category")


    # ============================
    # 1️⃣ Trend Harga & Volume (Matplotlib Dual Axis - Clean)
    # ============================
    
    st.header("1️⃣ Trend Harga & Volume (Dual Axis – Matplotlib Version)")
    
    import matplotlib.pyplot as plt
    
    # Pastikan tanggal valid
    df_trans["Tanggal"] = pd.to_datetime(df_trans["Tanggal"], errors="coerce")
    df_harga["Tanggal"] = pd.to_datetime(df_harga["Tanggal"], errors="coerce")
    
    # Cari kolom Qty
    qty_candidates = ["Qty", "qty", "Jumlah", "jumlah", "Quantity", "quantity",
                      "Jumlah dalam pcs", "QTY", "PCS", "Pcs"]
    kolom_qty = next((c for c in df_trans.columns if c.strip() in qty_candidates), None)
    
    # Agregasi harian
    df_daily = df_trans.groupby("Tanggal").agg(
        Total_Qty=(kolom_qty, "sum"),
        Total_Jual=("Total_Nilai", "sum")
    ).reset_index()
    
    # Merge harga harian
    harga_candidates = ["Harga_Jual_Antam", "Harga Jual Antam", "Harga_Jual", "Harga Jual"]
    kolom_harga = next((c for c in df_harga.columns if c.strip() in harga_candidates), None)
    
    df_merge = df_daily.merge(df_harga, on="Tanggal", how="left")
    df_merge = df_merge.dropna(subset=["Total_Qty", kolom_harga])
    df_merge = df_merge.sort_values("Tanggal")
    
    # ============================
    # Matplotlib Dual Axis
    # ============================
    
    fig, ax = plt.subplots(figsize=(15, 5))
    ax2 = ax.twinx()
    
    # Plot harga emas (kiri)
    ax.plot(df_merge["Tanggal"], df_merge[kolom_harga], color="blue", linewidth=2, label="Harga Emas")
    
    # Plot qty (kanan)
    ax2.plot(df_merge["Tanggal"], df_merge["Total_Qty"], color="orange", linewidth=2, label="Total Qty")
    
    # Label axis
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Harga Emas (Rp)", color="blue")
    ax2.set_ylabel("Total Qty", color="orange")
    
    ax.tick_params(axis='y', labelcolor="blue")
    ax2.tick_params(axis='y', labelcolor="orange")
    
    # Judul
    plt.title("Harga Emas vs Volume Penjualan (Dual Axis – Matplotlib)")
    
    # Improve layout
    fig.tight_layout()
    
    # Tampilkan di Streamlit
    st.pyplot(fig)
    
    # ============================
    # 🧍 DEMOGRAFI PELANGGAN (Per Kolom Data Valid)
    # ============================
    
    st.header("🧍 Demografi Pelanggan")
    
    pel = df_pelanggan.copy()
    
    # Fungsi untuk membersihkan data “data kosong”
    def clean_col(col):
        return (
            col.fillna("")                   # Hilangkan NaN
               .replace(["data kosong", "Data Kosong", "DATA KOSONG", ""], None)
        )
    
    # Membersihkan kolom yang digunakan
    kolom_demografi = ["Provinsi", "Kota", "Lokasi Pendaftaran", "Tempat Lahir", "Tanggal_Lahir"]
    
    for k in kolom_demografi:
        if k in pel.columns:
            pel[k] = clean_col(pel[k])
    
    # ============================
    # 🗺️ DISTRIBUSI PROVINSI (Metode Anti Error — Matplotlib)
    # ============================
    if "Provinsi" in pel.columns:
        st.subheader("🗺️ Distribusi Provinsi (Valid per Customer)")

        # Filter data valid
        prov = pel[["Customer_ID", "Provinsi"]].copy()
        prov["Provinsi"] = prov["Provinsi"].replace(
            ["data kosong", "", "0", 0], pd.NA
        )
        prov = prov.dropna(subset=["Provinsi"])

        prov_count = prov["Provinsi"].value_counts()

        if len(prov_count) > 0:
            import matplotlib.pyplot as plt

            fig, ax = plt.subplots(figsize=(8, 4))
            prov_count.plot(kind="bar", ax=ax, color="skyblue")

            ax.set_title("Distribusi Provinsi Berdasarkan Data Valid")
            ax.set_xlabel("Provinsi")
            ax.set_ylabel("Jumlah")
            ax.grid(axis="y", linestyle="--", alpha=0.5)

            st.pyplot(fig)

        else:
            st.info("Tidak ada data Provinsi valid.")


    
    
    # ============================
    # 🏙️ KOTA
    # ============================
    if "Kota" in pel.columns:
        st.subheader("🏙️ Distribusi Kota (Valid per Customer)")
    
        kota = pel[["Customer_ID", "Kota"]].dropna(subset=["Kota"])
        kota_count = kota["Kota"].value_counts().reset_index()
        kota_count.columns = ["Kota", "Jumlah"]
    
        if len(kota_count) > 0:
            fig = px.bar(
                kota_count, x="Kota", y="Jumlah",
                title="Distribusi Kota Berdasarkan Data Valid",
                text="Jumlah", color="Jumlah"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Tidak ada data Kota valid.")
    
    
    # ============================
    # 📝 LOKASI PENDAFTARAN
    # ============================
    if "Lokasi Pendaftaran" in pel.columns:
        st.subheader("📝 Distribusi Lokasi Pendaftaran (Valid per Customer)")

        lok = pel[["Customer_ID", "Lokasi Pendaftaran"]].dropna(subset=["Lokasi Pendaftaran"])
        lok_count = lok["Lokasi Pendaftaran"].value_counts().reset_index()
        lok_count.columns = ["Lokasi Pendaftaran", "Jumlah"]

        if len(lok_count) > 0:
            fig = px.bar(
                lok_count, x="Lokasi Pendaftaran", y="Jumlah",
                title="Distribusi Lokasi Pendaftaran Berdasarkan Data Valid",
                text="Jumlah", color="Jumlah"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Tidak ada data Lokasi Pendaftaran valid.")





    # ============================
    # 3️⃣ RFM (PERCENTILE SCORING 0–100)
    # ============================
    
    st.header("3️⃣ RFM (Recency, Frequency, Monetary) — Percentile 0–100")
    
    # Hitung dasar RFM
    rfm = df_trans.groupby("Customer_ID").agg(
        Frequency=("Tanggal", "count"),
        Monetary=("Total_Nilai", "sum"),
        Last_Tanggal=("Tanggal", "max")
    ).reset_index()
    
    # Recency
    rfm["Recency"] = (pd.Timestamp("2024-12-31") - rfm["Last_Tanggal"]).dt.days
    
    # ============================
    # Percentile Scoring 0–100
    # ============================
    
    # Recency → lebih kecil lebih baik → score terbalik
    rfm["R_pct"] = 100 - rfm["Recency"].rank(pct=True) * 100
    
    # Frequency → lebih besar lebih baik
    rfm["F_pct"] = rfm["Frequency"].rank(pct=True) * 100
    
    # Monetary → lebih besar lebih baik
    rfm["M_pct"] = rfm["Monetary"].rank(pct=True) * 100
    
    # Total RFM Weighted (bobot bisa diubah)
    rfm["RFM_Score"] = (rfm["R_pct"] * 0.4) + (rfm["F_pct"] * 0.3) + (rfm["M_pct"] * 0.3)
    
    # Ambil top 10
    top10 = rfm.sort_values("RFM_Score", ascending=False).head(10)
    
    # Tampilkan tabel
    st.subheader("🏆 Top 10 Customer Terbaik (Percentile Mode 0–100)")
    st.dataframe(top10)


    # Ambil top 100 strict RFM
    top100 = rfm_strict.head(100).copy()

    # ================================
    # SCATTER PLOT — TOP 100 STRICT RFM
    # ================================
    
    st.subheader("📈 Scatter Plot — Frequency vs Monetary (Top 100 Strict RFM)")
    
    # Ambil top 100
    df_scatter = top100.copy()
    
    # Pastikan data numeric
    df_scatter["Frequency"] = pd.to_numeric(df_scatter["Frequency"], errors="coerce")
    df_scatter["Monetary"] = pd.to_numeric(df_scatter["Monetary"], errors="coerce")
    
    # Buang baris bermasalah
    df_scatter = df_scatter.dropna(subset=["Frequency", "Monetary"])
    df_scatter = df_scatter[df_scatter["Frequency"] > 0]
    df_scatter = df_scatter[df_scatter["Monetary"] > 0]
    
    # Scatter plot simple (anti error)
    import plotly.express as px
    
    fig_scatter = px.scatter(
        df_scatter,
        x="Frequency",
        y="Monetary",
        hover_data=["Customer_ID", "R_Score", "F_Score", "M_Score", "RFM_Weighted"],
        title="Scatter Plot — Frequency vs Monetary (Top 100 Strict RFM)",
    )
    
    # Log agar titik tidak numpuk
    fig_scatter.update_layout(
        xaxis=dict(type="log", title="Frequency (log)"),
        yaxis=dict(type="log", title="Monetary (log)"),
        template="plotly_white"
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)



    
    # ============================
    # 4️⃣ PRODUK TERLARIS
    # ============================
    st.header("4️⃣ Produk / Jasa Terlaris")

    if "Produk" in df_trans.columns:
        prod = df_trans.groupby("Produk")["Total_Nilai"].sum().reset_index()
        fig5 = px.bar(prod, x="Produk", y="Total_Nilai",
                      title="Omzet per Produk/Jasa")
        st.plotly_chart(fig5, use_container_width=True)

    st.success("Analisa selesai ✔ (Turbo Mode)")













































