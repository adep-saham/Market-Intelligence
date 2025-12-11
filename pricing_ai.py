import requests
import os
import json

AIML_API_KEY = os.getenv("AIML_API_KEY")

def aiml_price_ai(spot, indo, harta, g24, my_price):

    prompt = f"""
Anda adalah analis harga emas profesional.

Data:
Spot: {spot}
IndoGold: {indo}
Hartadinata: {harta}
Galeri 24: {g24}
Harga ANTAM: {my_price}

Tugas:
1. Hitung premium kompetitor.
2. Analisis tekanan pasar.
3. Tentukan apakah harga ANTAM overpriced atau underpriced.
4. Berikan rekomendasi harga final dalam 1 angka.
5. Jelaskan secara singkat dan profesional.

Format:
REKOMENDASI: Rp <angka>
ALASAN:
- <poin1>
- <poin2>
- <poin3>
"""

    url = "https://api.aimlapi.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {AIML_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-70b-instruct",   # model gratis & paling pintar
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.4
    }

    response = requests.post(url, json=payload, headers=headers)

    # DEBUG: tampilkan respons mentah jika error
    try:
        data = response.json()
    except:
        return f"❌ Response bukan JSON:\n{response.text}"

    # Jika response mengandung error
    if "error" in data:
        return f"❌ AIMLAPI Error:\n{json.dumps(data, indent=2)}"

    # Format benar (OpenAI style)
    return data["choices"][0]["message"]["content"]
