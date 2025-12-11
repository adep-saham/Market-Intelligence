import requests
import os
import json

AIML_API_KEY = os.getenv("AIML_API_KEY")

def aiml_price_ai(spot, indo, harta, g24, my_price):

    prompt = f"""
Anda adalah analis harga emas profesional...

(isi prompt terserah, bukan ini masalahnya)
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
        "max_tokens": 300
    }

    r = requests.post(url, json=payload, headers=headers)

    # LANGSUNG TAMPILKAN RESPONSE RAW DULU
    try:
        data = r.json()
    except:
        return f"❌ RESPONSE BUKAN JSON:\n\n{r.text}"

    # TAMPILKAN RESPONS PENUH
    return f"🔎 RAW RESPONSE:\n\n{json.dumps(data, indent=2)}"
