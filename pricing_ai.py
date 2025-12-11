import onnxruntime as ort
import numpy as np

# Load model Phi-3 Mini ONNX sekali saja
session = ort.InferenceSession("phi-3-mini.onnx")

def run_local_llm(prompt):
    inputs = {
        "input_text": np.array([prompt])
    }
    output = session.run(None, inputs)
    return output[0][0]


def local_price_recommendation(spot, indo, harta, g24, my_price):

    prompt = f"""
Anda adalah analis harga emas.

Data:
Spot emas per gram: {spot}
IndoGold: {indo}
Hartadinata: {harta}
Galeri 24: {g24}
Harga jual ANTAM: {my_price}

Tugas:
1. Hitung premium 3 kompetitor.
2. Berikan evaluasi ringkas.
3. Berikan rekomendasi harga final.

Format:
REKOMENDASI: Rp <angka>
ALASAN:
- <point1>
- <point2>
- <point3>
"""

    return run_local_llm(prompt)
