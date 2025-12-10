import google.generativeai as genai
from google.oauth2 import service_account
import base64
import json
import streamlit as st

# ============================================================
# 1. LOAD & DECODE SERVICE ACCOUNT FROM STREAMLIT SECRETS
# ============================================================

def load_gcp_credentials():
    """Load and decode GCP service account from Streamlit secrets."""

    try:
        # Decode Base64 private key
        private_key_decoded = base64.b64decode(
            st.secrets["GCP_PRIVATE_KEY_BASE64"]
        ).decode("utf-8")

        # Reconstruct full service account JSON
        service_account_info = {
            "type": "service_account",
            "project_id": st.secrets["GCP_PROJECT_ID"],
            "private_key_id": st.secrets["GCP_PRIVATE_KEY_ID"],
            "private_key": private_key_decoded,
            "client_email": st.secrets["GCP_SERVICE_ACCOUNT_EMAIL"],
            "token_uri": "https://oauth2.googleapis.com/token"
        }

        # Convert into actual credential object
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )

        # Configure Gemini
        genai.configure(credentials=credentials)
        return True, None

    except Exception as e:
        return False, str(e)


# Try load credentials on import
loaded, error_msg = load_gcp_credentials()
if not loaded:
    st.error(f"[GCP Credential Error] {error_msg}")


# ============================================================
# 2. GEMINI PRICE RECOMMENDATION FUNCTION
# ============================================================

def gemini_price_recommendation(spot, indo, harta, g24, my_price):
    """
    Generate AI-based pricing recommendation using Gemini 1.5 Flash.
    """

    model_name = "models/gemini-1.5-flash"

    prompt = f"""
Anda adalah AI Pricing Analyst Logam Mulia.

Gunakan data berikut untuk analisis:

Spot Gold (IDR/gram): {spot}

Harga Kompetitor:
- IndoGold : {indo}
- Hartadinata : {harta}
- Galeri 24 : {g24}

Harga Jual ANTAM saat ini: {my_price}

Tugas:
1. Hitung premium masing-masing kompetitor.
2. Jelaskan apakah harga ANTAM saat ini masih kompetitif atau tidak.
3. Berikan SATU harga rekomendasi terbaik versi AI.
4. Format jawaban sebagai berikut:

REKOMENDASI: Rp <angka>
ALASAN:
- <point 1>
- <point 2>
- <point 3>
"""

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"ERROR saat memanggil Gemini AI: {e}"



