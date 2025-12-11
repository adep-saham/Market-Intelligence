import streamlit as st
import requests
import json

HF_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct"


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
1. Hitung premium kompetitor dibanding spot.
2. Tentukan apakah harga ANTAM overpriced / fair / underpriced.
3. Berikan SATU rekomendasi harga terbaik hari ini.
4. Format WAJIB:

REKOMENDASI: Rp <angka>
ALASAN:
- <point1>
- <point2>
- <point3>
"""

    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0.3, "max_new_tokens": 300}
    }

    try:
        response = requests.post(HF_URL, json=payload)
        data = response.json()

        # Jika error dari HF
        if "error" in data:
            return f"❌ HF Error: {data['error']}"

        # Model output berada pada index 0
        return data[0]["generated_text"]

    except Exception as e:
        return f"❌ ERROR memanggil HF API:\n{e}"
