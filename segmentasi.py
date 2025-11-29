import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==========================================================
# ADVANCED SEGMENTASI PELANGGAN LM (NO CSV)
# ==========================================================

def segmentasi_pelanggan_lm():

    st.title("Segmentasi Pelanggan LM")

    st.subheader("Advanced Customer Segmentation (RFM Model)")

    # ----------------------------------------------------------
    # 1. Generate Dummy Customer Transaction Data (Auto)
    # ----------------------------------------------------------
    np.random.seed(42)
    n_customers = 150

    data = pd.DataFrame({
        "Customer_ID": [f"CUST-{i:03d}" for i in range(n_customers)],
        "Recency": np.random.randint(1, 365, n_customers),             # hari sejak pembelian terakhir
        "Frequency": np.random.randint(1, 15, n_customers),            # frekuensi pembelian
        "Monetary": np.random.randint(1_000_000, 150_000_000, n_customers) # nilai total pembelian IDR
    })

    # ----------------------------------------------------------
    # 2. Hitung skor RFM (1–5)
    # ----------------------------------------------------------
    data["R_Score"] = pd.qcut(data["Recency"], 5, labels=[5,4,3,2,1]).astype(int)
    data["F_Score"] = pd.qcut(data["Frequency"], 5, labels=[1,2,3,4,5]).astype(int)
    data["M_Score"] = pd.qcut(data["Monetary"], 5, labels=[1,2,3,4,5]).astype(int)

    data["RFM_Score"] = data["R_Score"] + data["F_Score"] + data["M_Score"]

    # ----------------------------------------------------------
    # 3. Segment Classification Rules
    # ----------------------------------------------------------
    def classify(rfm):
        if rfm >= 13:
            return "Champion"
        elif rfm >= 10:
            return "Loyal Customer"
        elif rfm >= 7:
            return "Potential Loyalist"
        elif rfm >= 5:
            return "At Risk"
        else:
            return "Lost Customer"

    data["Segment"] = data["RFM_Score"].apply(classify)

    # ----------------------------------------------------------
    # 4. Visualisasi Komposisi Segmen
    # ----------------------------------------------------------
    st.write("### 🧩 Komposisi Segmentasi Pelanggan")

    seg_count = data["Segment"].value_counts().reset_index()
    seg_count.columns = ["Segment", "Jumlah"]

    fig = px.pie(
        seg_count,
        values="Jumlah",
        names="Segment",
        title="Distribusi Segment Pelanggan",
        color="Segment",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    st.plotly_chart(fig, use_container_width=True)

    # ----------------------------------------------------------
    # 5. Tabel Detail Pelanggan
    # ----------------------------------------------------------
    st.write("### 📋 Detail Segmentasi Pelanggan")
    st.dataframe(data, use_container_width=True)

    # ----------------------------------------------------------
    # 6. Insight Otomatis
    # ----------------------------------------------------------
    st.write("### 🔍 Insight Otomatis")

    insight_text = {
        "Champion": "Pelanggan terbaik dengan nilai belanja besar & aktif. Prioritas layanan premium & personal assistance.",
        "Loyal Customer": "Pelanggan setia yang sering bertransaksi. Cocok diberi program loyalitas & early access produk.",
        "Potential Loyalist": "Mulai terlihat pola beli yang bagus. Butuh nurture dengan edukasi & promo kecil.",
        "At Risk": "Mulai jarang transaksi. Perlu kampanye reaktivasi & penawaran khusus.",
        "Lost Customer": "Tidak membeli dalam waktu lama. Perlu strategi win-back intensif."
    }

    for seg in seg_count["Segment"]:
        st.markdown(f"**{seg}**: {insight_text[seg]}")
