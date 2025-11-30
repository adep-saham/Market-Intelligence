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
    
    # ==========================================================
    # DEMOGRAFI – FIXED VERSION (NO ERROR, NO KEYERROR)
    # ==========================================================
    
    # Pastikan nama kolom konsisten
    rename_map = {col: col.strip().title() for col in df_pelanggan.columns}
    df_pelanggan = df_pelanggan.rename(columns=rename_map)
    
    df_valid = df_pelanggan.copy()
    
    # Bersihkan isinya (bukan kolom)
    for col in df_valid.columns:
        df_valid[col] = df_valid[col].astype(str).str.strip().str.upper()
    
    # Replace nilai kosong
    df_valid = df_valid.replace(
        {"NAN": None, "NONE": None, "NULL": None, "DATA KOSONG": None, "": None}
    )
    
    # Tahun Lahir
    df_valid["Tahun_Lahir"] = pd.to_datetime(
        df_valid["Tanggal_Lahir"], errors="coerce"
    ).dt.year
    
    
    # ====================== DISTRIBUSI PROVINSI ======================
    if "Provinsi" in df_valid.columns:
        prov_series = (
            df_valid.dropna(subset=["Provinsi"])
            .groupby("Provinsi")["Customer_Id"]
            .count()
            .sort_values(ascending=False)
            .head(50)
        )
    
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.bar(prov_series.index, prov_series.values, color="skyblue")
        ax.set_title("Top 50 Provinsi Customer")
        ax.set_ylabel("Jumlah")
        plt.xticks(rotation=90, fontsize=6)
        st.pyplot(fig)
    
    
    # ======================== DISTRIBUSI KOTA ========================
    if "Kota" in df_valid.columns:
        kota_series = (
            df_valid.dropna(subset=["Kota"])
            .groupby("Kota")["Customer_Id"]
            .count()
            .sort_values(ascending=False)
            .head(50)
        )
    
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.bar(kota_series.index, kota_series.values, color="teal")
        ax.set_title("Top 50 Kota Customer")
        ax.set_ylabel("Jumlah")
        plt.xticks(rotation=90, fontsize=6)
        st.pyplot(fig)
    
    
    # ===================== DISTRIBUSI TAHUN LAHIR =====================
    
    if "Tahun_Lahir" in df_valid.columns:
        tahun_series = (
            df_valid.dropna(subset=["Tahun_Lahir"])
            .groupby("Tahun_Lahir")["Customer_Id"]
            .count()
            .sort_index()
        )
    
        fig, ax = plt.subplots(figsize=(10, 3))
    
        ax.bar(tahun_series.index.astype(int), tahun_series.values, color="orange")
        ax.set_title("Distribusi Tahun Lahir Customer")
        ax.set_ylabel("Jumlah")
    
        # Atur xtick setiap 5 tahun
        tahun_list = tahun_series.index.astype(int).tolist()
        xticks = [t for t in tahun_list if t % 5 == 0]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticks, rotation=45, fontsize=6)
    
        st.pyplot(fig)

    
  
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

    # ================================
    # TOP 100 STRICT RFM
    # ================================
    if "RFM_Weighted" in rfm_strict.columns:
        rfm_strict = rfm_strict.sort_values("RFM_Weighted", ascending=False)
        top100 = rfm_strict.head(100).copy()
    else:
        st.warning("⚠️ RFM_Weighted tidak ditemukan. Scatter plot dilewati.")
        top100 = pd.DataFrame()  # fallback aman
    
    # ================================
    # SCATTER PLOT MATPLOTLIB
    # ================================
    st.subheader("📈 Scatter Plot (Matplotlib) — Frequency vs Monetary (Top 100 Strict RFM)")
    
    if not top100.empty:
    
        df_scatter = top100.copy()
    
        # Pastikan numeric
        df_scatter["Frequency"] = pd.to_numeric(df_scatter["Frequency"], errors="coerce")
        df_scatter["Monetary"] = pd.to_numeric(df_scatter["Monetary"], errors="coerce")
    
        # Bersihkan data invalid
        df_scatter = df_scatter.dropna(subset=["Frequency", "Monetary"])
        df_scatter = df_scatter[(df_scatter["Frequency"] > 0) & (df_scatter["Monetary"] > 0)]
    
        import matplotlib.pyplot as plt
    
        # Ukuran figur 1/3 layar
        fig, ax = plt.subplots(figsize=(7, 4))
    
        # Scatter
        ax.scatter(
            df_scatter["Frequency"],
            df_scatter["Monetary"],
            alpha=0.7,
            s=60,
            edgecolor="black",
            linewidth=0.5,
            color="#1f77b4"
        )
    
        # Log scale agar tidak menumpuk
        ax.set_xscale("log")
        ax.set_yscale("log")
    
        ax.set_title("Scatter Plot — Frequency vs Monetary (Top 100 Strict RFM)")
        ax.set_xlabel("Frequency (log)")
        ax.set_ylabel("Monetary (log)")
    
        ax.grid(True, alpha=0.3, linestyle="--")
    
        st.pyplot(fig)
    
    else:
        st.info("Tidak tersedia data Top 100 untuk scatter plot.")



    
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

























































