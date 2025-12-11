import google.generativeai as genai
import streamlit as st

# ==========================================
# Load API Key
# ==========================================
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ GEMINI_API_KEY belum diset di Streamlit Secrets.")
else:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])


# ==========================================
# Gemini Price Recommendation
# ==========================================
def gemini_price_recommendation(spot, indo, harta, g24, my_price):
    model_name = "models/gemini-1.5-flash"

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
4. Format jawaban sebagai berikut:

REKOMENDASI: Rp <angka>
ALASAN:
- <point 1>
- <point 2>
- <point 3>
"""

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"❌ ERROR saat memanggil Gemini API: {e}"
