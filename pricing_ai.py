import requests
import os

AIML_API_KEY = os.getenv("AIML_API_KEY")

def aiml_price_ai(spot, indo, harta, g24, my_price):

    prompt = f"""
Anda adalah analis harga emas profesional.

Data pasar:
- Spot emas: {spot}
- IndoGold: {indo}
- Hartadinata: {harta}
- Galeri 24: {g24}
- Harga ANTAM saat ini: {my_price}

Tugas AI:
1. Hitung premium masing-masing kompetitor.
2. Analisis kondisi pasar (spread, deviasi ANTAM, tekanan harga).
3. Tentukan apakah harga ANTAM overpriced, fair, atau underpriced.
4. Berikan SATU harga rekomendasi final.
5. Gunakan Bahasa Indonesia profesional dan rapi.

FORMAT WAJIB:
REKOMENDASI: Rp <angka>
ALASAN:
- <point 1>
- <point 2>
- <point 3>
"""

    url = "https://api.aimlapi.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {AIML_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-70b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.4
    }

    response = requests.post(url, json=payload, headers=headers)
    result = response.json()

    # Return output text
    return result["choices"][0]["message"]["content"]
