def aiml_price_ai(spot, indo, harta, g24, my_price):
    url = "https://api.aimlapi.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {AIML_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",   # MODEL GRATIS
        "messages": [
            {
                "role": "user",
                "content": f"""
Anda adalah AI analis harga emas...
Spot: {spot}
IndoGold: {indo}
Harta: {harta}
Galeri 24: {g24}
Harga Antam: {my_price}
Buat rekomendasi harga dan alasan.
"""
            }
        ],
        "temperature": 0.5
    }
