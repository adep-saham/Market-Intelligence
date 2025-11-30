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
    # 3️⃣ RFM (Strict Quantile + Weighted + Tie-Break)
    # ============================
    
    st.header("3️⃣ RFM (Recency, Frequency, Monetary) — Strict Mode")
    
    # --- Hitung dasar RFM ---
    rfm = df_trans.groupby("Customer_ID").agg(
        Frequency=("Tanggal", "count"),            # hitung semua transaksi (termasuk duplikat)
        Monetary=("Total_Nilai", "sum"),           # total nilai transaksi
        Last_Tanggal=("Tanggal", "max")            # transaksi terakhir
    ).reset_index()
    
    # Recency dihitung dari tanggal terakhir transaksi
    rfm["Recency"] = (pd.Timestamp("2024-12-31") - rfm["Last_Tanggal"]).dt.days
    
    # ============================
    # STRICT SCORING MENGGUNAKAN QCUT (Distribusi rata & adil)
    # ============================
    
    rfm["R_Score"] = pd.qcut(rfm["Recency"], 5, labels=[5,4,3,2,1]).astype(int)
    rfm["F_Score"] = pd.qcut(rfm["Frequency"], 5, labels=[1,2,3,4,5]).astype(int)
    rfm["M_Score"] = pd.qcut(rfm["Monetary"], 5, labels=[1,2,3,4,5]).astype(int)
    
    # ============================
    # WEIGHTED RFM SCORE (Lebih Ketat)
    # Recency = 40% | Frequency = 30% | Monetary = 30%
    # ============================
    
    rfm["RFM_Weighted"] = (
        rfm["R_Score"]*0.4 +
        rfm["F_Score"]*0.3 +
        rfm["M_Score"]*0.3
    )
    
    # ============================
    # FINAL RANKING DENGAN TIE-BREAKER
    # urutan: Weighted → Monetary → Frequency → Recency
    # ============================
    
    top10 = rfm.sort_values(
        ["RFM_Weighted", "Monetary", "Frequency", "Recency"],
        ascending=[False, False, False, True]
    ).head(10)
    
    st.subheader("🏆 Top 10 Customer Terbaik (Strict RFM + Weighted + Tie-Break)")
    st.dataframe(top10)
    
    # ============================
    # Scatter (Frequency vs Monetary)
    # ============================
    
    fig_scatter = px.scatter(
        rfm.sample(min(5000, len(rfm))),   # sampel agar cepat
        x="Frequency",
        y="Monetary",
        size="Monetary",
        color="RFM_Weighted",
        title="Scatter Plot — Frequency vs Monetary (Strict RFM)",
        labels={"Frequency": "Jumlah Transaksi", "Monetary": "Total Nilai (Rp)"}
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






















