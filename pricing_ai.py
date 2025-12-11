import streamlit as st
import requests
import json

# ==========================================
# LOAD API
# ==========================================
API_KEY = st.secrets.get("DEEPSEEK_API_KEY", None)

if not API_KEY:
    st.error("❌ DEEPSEEK_API_KEY belum diset di Streamlit Secrets.")

API_URL = "https://api.deepseek.com/v1/chat/completions"


# ==========================================
# PRICE RECOMMENDATION FUNCTION
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

Tugas:
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
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        data = response.json()

        # Debugging block (sementara)
        # st.write("RAW RESPONSE:", data)

        # Handle API error
        if "error" in data:
            return f"❌ DeepSeek Error: {data['error']}"

        # Extract result
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ ERROR memanggil DeepSeek API:\n{e}"
