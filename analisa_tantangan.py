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
    # 2️⃣ DEMOGRAFI PELANGGAN (FIX: UMUR + PROVINSI)
    # ============================
    
    st.header("2️⃣ Demografi Pelanggan")
    
    # =====================================================
    # 2A. UMUR PELANGGAN
    # =====================================================
    
    # --- pastikan Tanggal_Lahir selalu datetime ---
    if "Tanggal_Lahir" in df_pelanggan.columns:
        df_pelanggan["Tanggal_Lahir"] = pd.to_datetime(df_pelanggan["Tanggal_Lahir"], errors="coerce")
        
        # hitung umur
        today = pd.Timestamp("2024-12-31")
        df_pelanggan["Umur"] = ((today - df_pelanggan["Tanggal_Lahir"]).dt.days // 365)
    
        # merge umur ke df_trans
        df_trans = df_trans.merge(
            df_pelanggan[["Customer_ID", "Umur"]],
            on="Customer_ID",
            how="left"
        )
    
    # --- histogram umur ---
    if "Umur" in df_trans.columns:
        df_plot_age = df_trans.dropna(subset=["Umur"])
    
        if len(df_plot_age) > 0:
            fig2 = px.histogram(
                df_plot_age.sample(min(5000, len(df_plot_age))),
                x="Umur",
                nbins=20,
                title="Distribusi Umur Pelanggan"
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Tidak ada data umur valid untuk ditampilkan.")
    else:
        st.info("Data tanggal lahir / umur tidak tersedia.")
    
    # =====================================================
    # 2B. DEMOGRAFI PROVINSI
    # =====================================================
    
    # --- deteksi kolom provinsi di df_pelanggan ---
    prov_cols = ["Provinsi", "provinsi", "Province", "PROVINSI"]
    
    kolom_provinsi = None
    for c in df_pelanggan.columns:
        if c.strip() in prov_cols:
            kolom_provinsi = c
            break
    
    # --- merge provinsi ke df_trans ---
    if kolom_provinsi is not None:
        df_trans = df_trans.merge(
            df_pelanggan[["Customer_ID", kolom_provinsi]],
            on="Customer_ID",
            how="left"
        )
    
        # --- grafik jumlah pelanggan per provinsi ---
        prov_count = df_pelanggan[kolom_provinsi].value_counts().reset_index()
        prov_count.columns = ["Provinsi", "Jumlah_Pelanggan"]
    
        fig_prov1 = px.bar(
            prov_count,
            x="Provinsi",
            y="Jumlah_Pelanggan",
            title="Jumlah Pelanggan per Provinsi"
        )
        st.plotly_chart(fig_prov1, use_container_width=True)
    
        # --- grafik omzet total per provinsi ---
        omzet = df_trans.groupby(kolom_provinsi)["Total_Nilai"].sum().reset_index()
        omzet.columns = ["Provinsi", "Total_Omzet"]
    
        fig_prov2 = px.bar(
            omzet,
            x="Provinsi",
            y="Total_Omzet",
            title="Omzet Penjualan per Provinsi"
        )
        st.plotly_chart(fig_prov2, use_container_width=True)
    
    else:
        st.info("Kolom Provinsi tidak ditemukan dalam data pelanggan.")

    # ============================
    # 3️⃣ RFM (Recency, Frequency, Monetary) — STRICT & CLEAN
    # ============================
    
    st.header("3️⃣ RFM (Recency, Frequency, Monetary)")
    
    # 1️⃣ Buang duplikasi supaya Frequency tidak over-count
    df_trans_clean = df_trans.drop_duplicates(subset=["Customer_ID", "Tanggal", "Total_Nilai"])
    
    # 2️⃣ Hitung RFM
    rfm = df_trans_clean.groupby("Customer_ID").agg(
        Frequency=("Tanggal", "count"),
        Monetary=("Total_Nilai", "sum"),
        Last_Tanggal=("Tanggal", "max")
    ).reset_index()
    
    # 3️⃣ Hitung Recency dari end-of-year 2024
    today = pd.Timestamp("2024-12-31")
    rfm["Recency"] = (today - rfm["Last_Tanggal"]).dt.days
    
    # ============================
    # STRICT RFM SCORING — SAFE (NO ERROR)
    # ============================
    
    # 1️⃣ Pastikan Recency selalu angka (isi NaT → Recency 999)
    rfm["Recency"] = rfm["Recency"].fillna(9999)
    
    # 2️⃣ Pastikan Frequency dan Monetary tidak kosong
    rfm["Frequency"] = rfm["Frequency"].fillna(0)
    rfm["Monetary"] = rfm["Monetary"].fillna(0)
    
    # 3️⃣ BINS YANG MENUTUP SEMUA NILAI (SAFE)
    # Recency: semakin kecil semakin bagus
    rfm["R_Score"] = pd.cut(
        rfm["Recency"],
        bins=[-1, 7, 30, 90, 180, 999999999],     # semua nilai tercakup
        labels=[5, 4, 3, 2, 1],
        include_lowest=True
    ).astype(int)
    
    # Frequency
    rfm["F_Score"] = pd.cut(
        rfm["Frequency"],
        bins=[-1, 4, 10, 20, 50, 999999999],       # batas atas sangat besar
        labels=[1, 2, 3, 4, 5],
        include_lowest=True
    ).astype(int)
    
    # Monetary
    rfm["M_Score"] = pd.cut(
        rfm["Monetary"],
        bins=[-1, 100_000_000, 250_000_000, 500_000_000, 1_000_000_000, 999999999999999],
        labels=[1, 2, 3, 4, 5],
        include_lowest=True
    ).astype(int)
    
    rfm["RFM_Score"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]

    
    # ============================
    # 3B. TOP 10 CUSTOMER TERBAIK
    # ============================
    
    top10 = rfm.sort_values("RFM_Score", ascending=False).head(10)
    
    st.subheader("🏆 Top 10 Customer Terbaik (Strict RFM)")
    st.dataframe(top10)
    
    # ============================
    # 3C. SCATTER PLOT — FIXED & CLEAN
    # ============================
    
    st.subheader("Scatter Frequency vs Monetary (Fixed & Clean)")
    
    fig_scatter = px.scatter(
        rfm,
        x="Frequency",
        y="Monetary",
        size="Monetary",
        color="RFM_Score",
        color_continuous_scale="Viridis",
        hover_data=["Customer_ID", "Frequency", "Monetary", "RFM_Score"],
        title="Scatter Plot: Frequency vs Monetary per Customer"
    )
    
    fig_scatter.update_layout(
        xaxis_title="Frequency (Jumlah Transaksi)",
        yaxis_title="Monetary (Total Belanja)",
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



















