import streamlit as st
import requests

AIML_API_KEY = st.secrets["AIML_API_KEY"]  # ← WAJIB ADA

def aiml_price_ai(spot, indo, harta, g24, my_price):

    url = "https://api.aimlapi.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {AIML_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",   # MODEL GRATIS
        "messages": [
            {
                "role": "user",
                "content": f"""
Spot: {spot}
IndoGold: {indo}
Hartadinata: {harta}
Galeri24: {g24}
Harga Antam: {my_price}

Buat rekomendasi harga final dan alasannya.
"""
            }
        ]
    }

    res = requests.post(url, json=payload, headers=headers)

    data = res.json()

    # Debug kalau error
    if "choices" not in data:
        return f"❌ AIML API Error:\n\n{data}"

    return data["choices"][0]["message"]["content"]
