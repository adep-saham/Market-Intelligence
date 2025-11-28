import streamlit as st

st.set_page_config(page_title="MI Logam Mulia", layout="wide")

st.title("✔ Aplikasi Streamlit Berhasil Jalan")
st.write("Ini adalah versi NORMAL tanpa modul MI.")

st.subheader("Tes Komponen UI")
st.write("Jika halaman ini muncul, berarti Streamlit Anda tidak error.")

st.metric("Harga Emas (Dummy)", "Rp 1.234.000", "+0.20%")
st.line_chart([1,2,3,4,5,6])
