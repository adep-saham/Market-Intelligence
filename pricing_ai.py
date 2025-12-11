import os
import requests
import json

AIML_API_KEY = os.getenv("AIML_API_KEY")

def aiml_price_ai(spot, indo, harta, g24, my_price):

    prompt = f"""
Anda adalah analis harga emas profesional.

Data pasar:
- Spot: {spot}
- IndoGold: {indo}
- Hartadinata: {harta}
- Galeri 24: {g24}
- Harga ANTAM: {my_price}

Tugas:
1. Hitung premium kompetitor.
2. Analisis tekanan pasar.
3. Tentukan overpriced / underpriced.
4. Berikan SATU harga rekomendasi final.
5. Jelaskan dalam format:

REKOMENDASI: Rp <angka>
ALASAN:
- <point>
- <point>
- <point>
"""

    url = "https://api.aimlapi.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {AIML_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.4
    }

    r = requests.post(url, headers=headers, json=payload)

    try:
        data = r.json()
    except:
        return f"❌ Response bukan JSON:\n{r.text}"

    # Jika ada error → return error JSON
    if "error" in data or "meta" in data and "fieldErrors" in data["meta"]:
        return f"❌ AIML API Error:\n\n{json.dumps(data, indent=2)}"

    # Format sukses OpenAI style
    return data["choices"][0]["message"]["content"]
