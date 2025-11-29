import streamlit as st
import pandas as pd
import numpy as np


# =================================================================
# 🔥 Fungsi Pembantu
# =================================================================
def make_alert(message, level="warning"):
    if level == "danger":
        st.error(f"⚠️ {message}")
    elif level == "success":
        st.success(f"✅ {message}")
    else:
        st.warning(f"🟡 {message}")


# =================================================================
# 🚨 Fungsi EWS Utama
# =================================================================
def ews_check(global_df, competitor_df, traffic_df):
    alerts = []

    # 1. Trend Harga Emas Dunia
    if len(global_df) >= 2:
        last = global_df["price"].iloc[-1]
        prev = global_df["price"].iloc[-2]
        change = (last - prev) / prev * 100

        if change > 1.5:
            alerts.append(("Harga emas dunia melonjak {:.2f}%".format(change), "danger"))
        elif change < -1.5:
            alerts.append(("Harga emas dunia turun tajam {:.2f}%".format(change), "danger"))
        elif abs(change) > 0.5:
            alerts.append(("Harga emas dunia bergerak signifikan {:.2f}%".format(change), "warning"))

    # 2. Price War (Gap Kompetitor)
    if "gap" in competitor_df.columns:
        worst_gap = competitor_df["gap"].min()
        if worst_gap < -1500:
            alerts.append(("Gap kompetitor terlalu negatif, indikasi price war!", "danger"))
        elif worst_gap < -500:
            alerts.append(("Gap kompetitor menurun, perhatikan kompetitor!", "warning"))

    # 3. Harga Competitor Anomali
    try:
        comp_avg = competitor_df["jual"].mean()
        comp_std = competitor_df["jual"].std()

        for idx, row in competitor_df.iterrows():
            if abs(row["jual"] - comp_avg) > comp_std * 1.8:
                alerts.append((f"Harga {row['source']} tampak tidak normal.", "warning"))
    except:
        pass

    # 4. Traffic Drop
    if len(traffic_df) >= 7:
        today = traffic_df["visits"].iloc[-1]
        week_avg = traffic_df["visits"].iloc[-7:].mean()

        if today < week_avg * 0.75:
            alerts.append(("Penurunan traffic lebih dari 25%", "danger"))
        elif today < week_avg * 0.90:
            alerts.append(("Traffic menurun minggu ini", "warning"))

    return alerts


# =================================================================
# 🖥️ Halaman EWS (dipanggil dari app.py)
# =================================================================
def ews_page(global_df, competitor_df, traffic_df):
    st.subheader("🛡 Governance & Early Warning System (EWS)")
    st.caption("Sistem peringatan dini otomatis berdasarkan harga dunia, kompetitor, dan traffic.")

    st.write("---")
    st.write("### 🔍 Hasil Analisis EWS")

    alerts = ews_check(global_df, competitor_df, traffic_df)

    if not alerts:
        st.success("Semua stabil. Tidak ada alert.")
    else:
        for message, level in alerts:
            make_alert(message, level)

    # ============================================================
    # 📌 Rekomendasi Aksi
    # ============================================================
    st.write("---")
    st.write("### 📝 Rekomendasi Aksi Otomatis")

    if not alerts:
        st.info("Tidak ada rekomendasi. Situasi stabil.")
    else:
        for message, level in alerts:
            if level == "danger":
                st.error(f"➡ **Aksi Prioritas**: {message}. Segera evaluasi harga LM & update MI Daily Brief.")
            elif level == "warning":
                st.warning(f"➡ **Aksi**: {message}. Pantau perkembangan 24 jam ke depan.")

    # ============================================================
    # 📊 Ringkasan Dashboard Mini
    # ============================================================
    st.write("---")
    st.write("### 📈 Ringkasan Indikator Utama")

    col1, col2, col3 = st.columns(3)
    col1.metric("Harga Emas Dunia (USD)", f"${global_df['price'].iloc[-1]:,.2f}")
    col2.metric("Harga Kompetitor Rata²", f"Rp {competitor_df['jual'].mean():,.0f}")
    col3.metric("Traffic hari ini", f"{traffic_df['visits'].iloc[-1]:,}")

    st.caption("Sumber: MI Internal Analytics Engine")

