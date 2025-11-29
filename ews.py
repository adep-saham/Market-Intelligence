import streamlit as st
import pandas as pd

# ==========================================
# CARI KOLOM TRAFFIC SECARA OTOMATIS
# ==========================================
def detect_traffic_column(df):
    possible_cols = ["visits", "visit", "traffic", "pengunjung", "count", "value"]
    for col in possible_cols:
        if col in df.columns:
            return col
    return None


# ==========================================
# LOGIC UTAMA EWS
# ==========================================
def ews_check(global_df, competitor_df, traffic_df):
    alerts = []

    # -------- TRAFFIC CHECK ----------
    traffic_col = detect_traffic_column(traffic_df)

    if traffic_col:
        if len(traffic_df) >= 7:
            today = traffic_df[traffic_col].iloc[-1]
            last_week_avg = traffic_df[traffic_col].iloc[-7:].mean()

            if today < last_week_avg * 0.75:
                alerts.append(("Traffic turun >25% dibanding minggu lalu", "danger"))
            elif today < last_week_avg * 0.90:
                alerts.append(("Traffic menurun minggu ini", "warning"))
    else:
        alerts.append(("Kolom traffic tidak ditemukan", "warning"))

    # -------- WORLD GOLD PRICE --------
    if len(global_df) >= 2:
        last = global_df["price"].iloc[-1]
        prev = global_df["price"].iloc[-2]
        change = (last - prev) / prev * 100

        if change > 1.5:
            alerts.append((f"Harga emas dunia naik tajam {change:.2f}%", "danger"))
        elif change < -1.5:
            alerts.append((f"Harga emas dunia turun tajam {change:.2f}%", "danger"))
        elif abs(change) > 0.6:
            alerts.append((f"Harga emas bergerak signifikan {change:.2f}%", "warning"))

    # -------- COMPETITOR PRICE GAP --------
    if "gap" in competitor_df.columns:
        min_gap = competitor_df["gap"].min()

        if min_gap < -1500:
            alerts.append(("Gap kompetitor sangat negatif (indikasi price war)", "danger"))
        elif min_gap < -500:
            alerts.append(("Gap kompetitor menurun (potensi price pressure)", "warning"))

    return alerts


# ==========================================
# HALAMAN UTAMA
# ==========================================
def ews_page(global_df, competitor_df, traffic_df):
    st.header("🔍 Hasil Analisis EWS")

    alerts = ews_check(global_df, competitor_df, traffic_df)

    if not alerts:
        st.success("Semua indikator stabil — tidak ada Early Warning.")
        return

    for msg, level in alerts:
        if level == "danger":
            st.error(msg)
        elif level == "warning":
            st.warning(msg)
        else:
            st.info(msg)
