# pricing_ai.py
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gpt_price_recommendation(spot, indo, harta, g24, my_price):
    prompt = f"""
Anda adalah AI Pricing Analyst Emas Logam Mulia.

Gunakan data berikut untuk memberikan harga rekomendasi dan analisis:

Spot Gold (IDR/gram): {spot}

Harga Kompetitor:
- IndoGold: {indo}
- Hartadinata: {harta}
- Galeri 24: {g24}

Harga Jual ANTAM saat ini: {my_price}

Tugas:
1. Hitung premium masing-masing kompetitor.
2. Berikan analisis pasar (ringkas).
3. Berikan *SATU ANGKA rekomendasi harga jual* dalam Rupiah.
4. Format output TEKS saja, contoh:

REKOMENDASI: Rp x.xxx.xxx
ALASAN: <analisis ringkas>
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Anda adalah engine AI pricing ANTAM Logam Mulia."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message["content"]
