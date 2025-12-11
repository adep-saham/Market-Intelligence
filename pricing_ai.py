import streamlit as st
import requests
import json

# ==========================================
# 1. LOAD DEEPSEEK API KEY
# ==========================================
if "DEEPSEEK_API_KEY" not in st.secrets:
    st.error("❌ DEEPSEEK_API_KEY belum diset di Streamlit Secrets.")
else:
    API_KEY = st.secrets["DEEPSEEK_API_KEY"]

API_URL = "https://api.deepseek.com/chat/completions"


# ==========================================
# 2. PRICE RECOMMENDATION FUNCTION
# ==========================================
def gpt_price_recommendation(spot, indo, harta, g24, my_price):

    prompt = f"""
Anda adalah AI Pricing Analyst Senior Logam Mulia.

Gunakan data berikut untuk memberikan rekomendasi harga jual ANTAM:

Spot Gold (IDR/gram): {spot}

Harga Kompetitor:
- IndoGold: {indo}
- Hartadinata: {harta}
- Galeri 24: {g24}

Harga ANTAM saat ini: {my_price}

Tugas Anda:
1. Hitung premium kompetitor dibandingkan spot.
2. Analisis apakah harga ANTAM kompetitif atau tidak.
3. Rekomendasikan SATU harga jual terbaik hari ini.
4. Format WAJIB sebagai:

REKOMENDASI: Rp <angka>
ALASAN:
- <alasan 1>
- <alasan 2>
- <alasan 3>
"""

    payload = {
        "model": "deepseek-chat",  
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ ERROR memanggil DeepSeek API:\n{e}"
