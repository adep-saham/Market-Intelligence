import streamlit as st
import requests
import json

HF_URL = "https://router.huggingface.co/v1/chat/completions"


def gpt_price_recommendation(spot, indo, harta, g24, my_price):

    prompt = f"""
Anda adalah AI Pricing Analyst Senior Logam Mulia.

Gunakan data berikut:

Spot Gold (IDR/gram): {spot}

Harga Kompetitor:
- IndoGold: {indo}
- Hartadinata: {harta}
- Galeri 24: {g24}

Harga ANTAM saat ini: {my_price}

Tugas:
1. Hitung premium kompetitor dibandingkan spot.
2. Tentukan apakah harga ANTAM overpriced / fair / underpriced.
3. Berikan SATU rekomendasi harga jual terbaik hari ini.
4. Format jawaban:

REKOMENDASI: Rp <angka>
ALASAN:
- <alasan 1>
- <alasan 2>
- <alasan 3>
"""

    payload = {
        "model": "meta-llama/Llama-3.2-3B-Instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300,
        "temperature": 0.3
    }

    try:
        response = requests.post(HF_URL, json=payload)
        data = response.json()

        # Debug
        # st.write("HF RAW RESPONSE:", data)

        if "error" in data:
            return f"❌ HF Error: {data['error']}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ ERROR memanggil HF Router API:\n{e}"
