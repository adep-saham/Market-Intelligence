from openai import OpenAI
import streamlit as st

# ==========================================
# 1. Load OpenAI API KEY
# ==========================================
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OPENAI_API_KEY belum diset di Streamlit Secrets.")
else:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# ==========================================
# 2. GPT Pricing Recommendation
# ==========================================
def gpt_price_recommendation(spot, indo, harta, g24, my_price):

    prompt = f"""
Anda adalah AI Pricing Analyst Logam Mulia.

Gunakan data berikut untuk membuat analisis harga emas ANTAM:

Spot Gold (IDR/gram): {spot}

Harga Kompetitor:
- IndoGold : {indo}
- Hartadinata : {harta}
- Galeri 24 : {g24}

Harga Jual ANTAM: {my_price}

Tugas:
1. Hitung premium kompetitor terhadap spot.
2. Evaluasi apakah harga ANTAM masih kompetitif.
3. Berikan SATU rekomendasi harga jual terbaik.
4. Format jawaban seperti berikut:

REKOMENDASI: Rp <angka>
ALASAN:
- <point 1>
- <point 2>
- <point 3>
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        return response.choices[0].message["content"]

    except Exception as e:
        return f"❌ ERROR memanggil GPT API:\n{e}"
