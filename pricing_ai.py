# ============================================
#  AI Lokal Pintar – MI GOLD (Tanpa API)
# ============================================

import numpy as np

def local_intelligence_recommendation(spot, indo, harta, g24, my_price):
    """
    AI lokal berbasis rule-engine + natural language generator.
    Tidak membutuhkan API.
    """

    # ================
    # 1. HITUNG PREMIUM
    # ================
    def premium(harga):
        return (harga - spot) / spot * 100

    prem_indo = premium(indo)
    prem_harta = premium(harta)
    prem_g24 = premium(g24)
    prem_my = premium(my_price)

    # rata2 premium pasar
    avg_prem = np.mean([prem_indo, prem_harta, prem_g24])
    deviasi = prem_my - avg_prem

    # tingkat tekanan pasar ("market pressure index")
    spread = max([indo, harta, g24]) - min([indo, harta, g24])
    mpi = spread / spot * 100  # %

    # ================
    # 2. TENTUKAN REKOMENDASI HARGA
    # ================

    # aturan AI lokal
    if deviasi > 1.2:  # terlalu mahal dibanding pasar
        rekom = my_price - (my_price * 0.008)  # turunkan 0.8%
        kondisi = "Harga ANTAM berada di atas pasar."
        arah = "Penurunan disarankan agar tetap kompetitif."
    elif deviasi < -1.2:  # terlalu murah
        rekom = my_price + (my_price * 0.008)  # naikkan 0.8%
        kondisi = "Harga ANTAM berada di bawah pasar."
        arah = "Kenaikan harga masih dapat diterima pasar."
    else:
        rekom = my_price
        kondisi = "Harga ANTAM sejajar dengan pasar."
        arah = "Tidak perlu penyesuaian signifikan."

    rekom = round(rekom, -2)

    # ================
    # 3. NATURAL LANGUAGE GENERATOR
    # ================

    alasan = [
        f"Premium IndoGold tercatat {prem_indo:.2f}%",
        f"Hartadinata berada pada {prem_harta:.2f}%",
        f"Galeri 24 berada pada {prem_g24:.2f}%",
        f"Rata-rata premium pasar: {avg_prem:.2f}%",
        f"Deviasi harga ANTAM terhadap pasar: {deviasi:.2f}%",
        f"Market Pressure Index (MPI): {mpi:.2f}%",
        kondisi,
        arah
    ]

    # Bangun paragraf alasan seperti LLM
    alasan_text = "\n".join([f"- {a}" for a in alasan])

    # ================
    # 4. FINAL OUTPUT COMO AI
    # ================

    output = f"""
REKOMENDASI: Rp {rekom:,}

ALASAN:
{alasan_text}

Catatan AI Lokal:
- Model ini menggunakan rule-engine dinamis yang meniru pola penalaran AI.
- Nilai rekomendasi menyesuaikan premium pasar, tekanan harga, dan spread kompetitor.
"""

    return output
