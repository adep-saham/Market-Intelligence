import google.generativeai as genai
from google.oauth2 import service_account
import json
import streamlit as st

# --- Load Service Account dari Streamlit Secrets ---
if "GCP_SERVICE_ACCOUNT" not in st.secrets:
    raise RuntimeError("Secret GCP_SERVICE_ACCOUNT belum diset di Streamlit Secrets.")

service_account_info = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])

credentials = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

genai.configure(credentials=credentials)


def gemini_price_recommendation(spot, indo, harta, g24, my_price):
    model_name = "models/gemini-1.5-flash"

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
