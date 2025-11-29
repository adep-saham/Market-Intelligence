import google.generativeai as genai
import os

# Configure API key
genai.configure(api_key=os.getenv("AIzaSyDU1rL7phIjZ83Joh7xn-6HE1HZ4PDvkvE"))

def gemini_price_recommendation(spot, indo, harta, g24, my_price):
    prompt = f"""
Anda adalah AI Pricing Analyst Emas Logam Mulia.

Gunakan data berikut:

Spot Gold (IDR per gram): {spot}

Harga Kompetitor:
- IndoGold: {indo}
- Hartadinata: {harta}
- Galeri 24: {g24}

Harga Jual ANTAM saat ini: {my_price}

Tugas Anda:
1. Hitung premium masing-masing kompetitor.
2. Analisis tren pasar (ringkas).
3. Berikan *SATU harga rekomendasi AI* (angka bulat Rupiah tanpa desimal).
4. Sertakan alasan bisnis (maks 3 poin).
5. Format WAJIB seperti berikut:

REKOMENDASI: Rp <angka>
ALASAN:
- <alasan1>
- <alasan2>
- <alasan3>
"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text

