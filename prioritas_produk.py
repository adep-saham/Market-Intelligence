import streamlit as st
import pandas as pd

def prioritas_produk_page():

    st.subheader("🏅 Ranking Prioritas Produk")

    # Contoh data dummy
    data = {
        "Produk": ["1g", "2g", "5g", "10g", "25g", "50g", "100g"],
        "Volume": [20795, 5860, 43158, 49732, 16284, 11265, 21850],
        "Margin": ["3.00%", "6.59%", "5.34%", "3.43%", "8.51%", "2.56%", "9.22%"],
        "Growth": ["23.16%", "-4.98%", "24.77%", "13.52%", "13.35%", "-4.79%", "-2.31%"],
        "Popularity": [93, 52, 86, 56, 70, 58, 88]
    }

    df = pd.DataFrame(data)

    # Skor prioritas dasar (bisa dikembangkan)
    df["PPS"] = (df["Popularity"] / df["Popularity"].max()) * 0.4 + \
                (df["Volume"] / df["Volume"].max()) * 0.4 + \
                (df.index / len(df)) * 0.2

    st.dataframe(
        df.sort_values("PPS", ascending=False),
        use_container_width=True
    )
