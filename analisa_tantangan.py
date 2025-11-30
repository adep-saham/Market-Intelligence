import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go  # <--- WAJIB ADA


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
    # 1️⃣ TREND HARGA & VOLUME (DUAL AXIS SIMPLE & CLEAN)
    # ============================
    
    st.header("1️⃣ Trend Harga & Volume (Dual Axis – Simple)")
    
    # -----------------------------
    # Step 1: Pastikan tanggal valid
    # -----------------------------
    df_trans["Tanggal"] = pd.to_datetime(df_trans["Tanggal"], errors="coerce")
    df_harga["Tanggal"] = pd.to_datetime(df_harga["Tanggal"], errors="coerce")
    
    # -----------------------------
    # Step 2: Deteksi kolom Qty
    # -----------------------------
    qty_candidates = ["Qty", "qty", "Jumlah", "jumlah", "Quantity", "quantity",
                      "Jumlah dalam pcs", "QTY", "PCS", "Pcs"]
    
    kolom_qty = next((c for c in df_trans.columns if c.strip() in qty_candidates), None)
    
    if kolom_qty is None:
        st.error("❌ Tidak menemukan kolom Qty di data transaksi.")
        st.stop()
    
    # -----------------------------
    # Step 3: Buat agregasi HARlAN
    # -----------------------------
    df_daily = df_trans.groupby("Tanggal").agg(
        Total_Qty=(kolom_qty, "sum"),
        Total_Jual=("Total_Nilai", "sum")
    ).reset_index()
    
    # -----------------------------
    # Step 4: Merge dengan harga emas
    # -----------------------------
    df_merge = df_daily.merge(df_harga, on="Tanggal", how="left")
    
    # -----------------------------
    # Step 5: Deteksi kolom Harga Emas
    # -----------------------------
    harga_candidates = [
        "Harga_Jual_Antam", "Harga Jual Antam", "Harga Jual",
        "Harga Jual (Rp)", "Harga_Jual", "HargaJualAntam"
    ]
    
    kolom_harga = next((c for c in df_merge.columns if c.strip() in harga_candidates), None)
    
    if kolom_harga is None:
        st.error(f"❌ Tidak menemukan kolom harga emas. Kolom tersedia: {df_merge.columns.tolist()}")
        st.stop()
    
    # -----------------------------
    # Step 6: Bersihkan & urutkan
    # -----------------------------
    df_merge = df_merge.dropna(subset=["Total_Qty", kolom_harga])
    df_merge = df_merge.sort_values("Tanggal")
    
    # -----------------------------
    # Step 7: Buat Dual Axis Chart Simple
    # -----------------------------
    fig = go.Figure()
    
    # --- Garis Harga (Left Axis)
    fig.add_trace(go.Scatter(
        x=df_merge["Tanggal"],
        y=df_merge[kolom_harga],
        name="Harga Emas Antam (Rp)",
        line=dict(color="#1f77b4", width=3)
    ))
    
    # --- Garis Qty (Right Axis)
    fig.add_trace(go.Scatter(
        x=df_merge["Tanggal"],
        y=df_merge["Total_Qty"],
        name="Total Qty",
        yaxis="y2",
        line=dict(color="#ff7f0e", width=3)
    ))
    
    fig.update_layout(
        title="Harga Emas vs Volume Penjualan (Dual Axis – Simple)",
        xaxis=dict(title="Tanggal"),
    
        # Axis kiri
        yaxis=dict(
            title="Harga Emas (Rp)",
            titlefont=dict(color="#1f77b4"),
            tickfont=dict(color="#1f77b4")
        ),
    
        # Axis kanan
        yaxis2=dict(
            title="Volume Penjualan (Qty)",
            overlaying="y",
            side="right",
            titlefont=dict(color="#ff7f0e"),
            tickfont=dict(color="#ff7f0e")
        ),
    
        template="simple_white",
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)



    # ============================
    # 2️⃣ DEMOGRAFI PELANGGAN
    # ============================
    st.header("2️⃣ Demografi Pelanggan")

    if "Umur" in df_trans.columns:
        fig2 = px.histogram(df_trans.sample(min(5000, len(df_trans))), x="Umur",
                            nbins=20, title="Distribusi Umur Pelanggan (Turbo)")
        st.plotly_chart(fig2, use_container_width=True)

    if "Provinsi" in df_trans.columns:
        omzet = df_trans.groupby("Provinsi")["Total_Nilai"].sum().reset_index()
        fig3 = px.bar(omzet, x="Provinsi", y="Total_Nilai", title="Omzet per Provinsi")
        st.plotly_chart(fig3, use_container_width=True)

    # ============================
    # 3️⃣ RFM (OPTIMIZED)
    # ============================

    # TURBO 3: Groupby cepat
    rfm = df_trans.groupby("Customer_ID").agg(
        Frequency=("Tanggal", "count"),
        Monetary=("Total_Nilai", "sum"),
        Last_Tanggal=("Tanggal", "max")
    ).reset_index()

    rfm["Recency"] = (pd.Timestamp("2024-12-31") - rfm["Last_Tanggal"]).dt.days

    # TURBO 4: scoring cepat (cut, bukan qcut)
    rfm["R_Score"] = pd.cut(rfm["Recency"], bins=5, labels=[5,4,3,2,1]).astype(int)
    rfm["F_Score"] = pd.cut(rfm["Frequency"], bins=5, labels=[1,2,3,4,5]).astype(int)
    rfm["M_Score"] = pd.cut(rfm["Monetary"], bins=5, labels=[1,2,3,4,5]).astype(int)

    rfm["RFM_Score"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]

    st.header("3️⃣ RFM (Recency, Frequency, Monetary)")

    top10 = rfm.sort_values("RFM_Score", ascending=False).head(10)

    st.subheader("🏆 Top 10 Customer Terbaik (Turbo Mode)")
    st.dataframe(top10)

    # Scatter cepat (sampel)
    fig_scatter = px.scatter(
        rfm.sample(min(5000, len(rfm))),
        x="Frequency",
        y="Monetary",
        size="Monetary",
        title="Scatter Frequency vs Monetary (Turbo)"
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











