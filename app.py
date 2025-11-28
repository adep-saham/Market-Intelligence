import streamlit as st
import pandas as pd

st.set_page_config(page_title="MI Logam Mulia", layout="wide")

st.title("📊 Market Intelligence – Step 2")
st.write("Tahap ini memuat data CSV dari folder data/.")

# === Load CSV ===
try:
    global_price = pd.read_csv("data/harga_global.csv")
    competitor = pd.read_csv("data/kompetitor.csv")
    sales = pd.read_csv("data/penjualan_lm.csv")
    traffic = pd.read_csv("data/traffic_website.csv")

    st.success("CSV berhasil dimuat.")
except Exception as e:
    st.error(f"Error loading CSV: {e}")
    st.stop()

st.subheader("📈 Harga Global")
st.dataframe(global_price)

st.subheader("📊 Kompetitor")
st.dataframe(competitor)

st.subheader("🛒 Penjualan LM")
st.dataframe(sales)

st.subheader("🌐 Traffic Website")
st.dataframe(traffic)
