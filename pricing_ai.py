import google.generativeai as genai
import os

# Konfigurasi API Key
genai.configure(api_key=os.getenv("AIzaSyBRSGLbIvqV0Tc6njysqI6QxYo95LjKnoM"))

def gemini_price_recommendation(spot, indo, harta, g24, my_price):
    model_name = "models/gemini-2.5-flash"  # MODEL VALID DI PROJECT ANDA

    prompt = f"""
Anda adalah AI Pricing Analyst Emas Logam Mulia.

Gunakan data berikut:

Spot Gold (IDR/gram): {spot}

Harga Kompetitor:
- IndoGold: {indo}
- Hartadinata: {harta}
- Galeri 24: {g24}

Harga Jual ANTAM saat ini: {my_price}

Tugas:
1. Hitung premium masing-masing kompetitor.
2. Analisis tren pasar.
3. Berikan SATU harga rekomendasi AI dalam Rupiah.
4. Format WAJIB seperti ini:

REKOMENDASI: Rp <angka>
ALASAN:
- <point1>
- <point2>
- <point3>
"""

    model = genai.GenerativeModel(model_name)

    response = model.generate_content(prompt)

    return response.text
