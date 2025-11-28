import streamlit as st
import pandas as pd

from mi_single_python import detect_price_gap

st.set_page_config(page_title="MI Logam Mulia", layout="wide")

st.title("📊 Market Intelligence – Step 3")
st.write("Tahap ini mengaktifkan analisis gap kompetitor.")

# Load CSV
global_price = pd.read_csv("data/harga_global.csv")
competitor = pd.read_csv("data/kompetitor.csv")

# Ambil harga terakhir LM
lm_price = global_price["price"].iloc[-1]

# Hitung gap
gap_df = detect_price_gap(lm_price, competitor)

st.subheader("📉 Analisis Gap Kompetitor")
st.dataframe(gap_df)

st.success("Step 3 MI berhasil!")
