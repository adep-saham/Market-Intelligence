# pricing_ai.py
from openai import AzureOpenAI
import os

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-05-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def copilot_price_recommendation(spot, indo, harta, g24, my_price):
    prompt = f"""
Anda adalah AI Pricing Analyst Logam Mulia.

Gunakan data berikut:

Spot Gold (IDR/gram): {spot}
Harga Kompetitor:
- IndoGold: {indo}
- Hartadinata: {harta}
- Galeri 24: {g24}

Harga ANTAM saat ini: {my_price}

Tugas Anda:
1. Hitung premium masing-masing kompetitor.
2. Analisis tren harga kompetitor (apakah agresif/defensif).
3. Berikan *satu angka rekomendasi harga* (dalam Rupiah).
4. Sertakan alasan bisnis secara ringkas.

Format output:
REKOMENDASI: <angka dalam Rupiah>
ANALISIS: <penjelasan ringkas>
"""

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "Anda adalah engine AI pricing ANTAM Logam Mulia."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message["content"]
