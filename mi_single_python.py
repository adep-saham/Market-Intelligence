import streamlit as st
import pandas as pd

st.set_page_config(page_title="MI Logam Mulia", layout="wide")

st.title("📊 Market Intelligence – Step 1")
st.write("Tahap ini menampilkan data dummy terlebih dahulu.")

# === Dummy Data ===
global_price = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=7),
    "price": [1000000, 1002000, 1001500, 1003000, 1002500, 1004000, 1003500]
})

st.subheader("📈 Harga Emas Global (Dummy)")
st.line_chart(global_price.set_index("date")["price"])

st.success("Step 1 berhasil. Data dummy tampil normal.")
