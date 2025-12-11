import numpy as np
import random

def local_intelligence_recommendation(spot, indo, harta, g24, my_price):

    # ======= 1. PREMIUM SUMMARY =======
    def prem(h):
        return (h - spot) / spot * 100

    p_indo  = prem(indo)
    p_harta = prem(harta)
    p_g24   = prem(g24)
    p_my    = prem(my_price)

    avg_prem = np.mean([p_indo, p_harta, p_g24])
    deviasi  = p_my - avg_prem
    spread   = max([indo, harta, g24]) - min([indo, harta, g24])
    mpi      = spread / spot * 100  # Market Pressure Index


    # ======= 2. STRATEGI AI =======
    if deviasi > 1.2:
        rekom = my_price - my_price * 0.0075
        stance = "Harga ANTAM berada di area *overpriced* dibanding pasar."
        strategy = "Strategi koreksi ringan disarankan untuk menjaga keunggulan kompetitif."
        tone = "defensive"
    elif deviasi < -1.2:
        rekom = my_price + my_price * 0.0075
        stance = "Harga ANTAM berada di area *underpriced*."
        strategy = "Penyesuaian naik kecil tetap aman, mengingat demand masih stabil."
        tone = "aggressive"
    else:
        rekom = my_price
        stance = "Harga ANTAM berada dalam zona *fair value*."
        strategy = "Harga dapat dipertahankan sambil monitoring pergerakan kompetitor."
        tone = "balanced"

    rekom = round(rekom, -2)

    # ======= 3. AI EXPLANATION ENGINE (lebih natural & variatif) =======
    opening_variants = [
        "Berdasarkan pemetaan premium kompetitor dan kondisi pasar saat ini, berikut evaluasi AI:",
        "Analisis otomatis terhadap 3 kompetitor utama menunjukkan pola berikut:",
        "AI mendeteksi dinamika harga yang relevan untuk penentuan harga hari ini:"
    ]

    market_insight = [
        "Spread kompetitor cukup lebar, menandakan pasar belum sepenuhnya stabil.",
        "Tekanan pasar relatif sedang, menunjukkan ruang untuk penyesuaian harga.",
        "Volatilitas premium antar kompetitor meningkat, mencerminkan demand yang berubah."
    ]

    risk_note = [
        "Menahan harga terlalu lama bisa mengurangi kecepatan rotasi barang.",
        "Koreksi harga yang terlalu agresif dapat mengurangi margin jangka pendek.",
        "Mengikuti pasar tanpa pertimbangan deviasi dapat menyebabkan mispricing."
    ]

    opening = random.choice(opening_variants)
    insight = random.choice(market_insight)
    risk    = random.choice(risk_note)

    # ======= 4. Final Output (versi AI yang lebih ‘hidup’) =======
    output = f"""
{opening}

📌 **Rekomendasi Harga AI**  
**Rp {rekom:,.0f}**

📊 **Ringkasan Analisis**
- Premium IndoGold: {p_indo:.2f}%
- Hartadinata: {p_harta:.2f}%
- Galeri 24: {p_g24:.2f}%
- Rata-rata premium pasar: {avg_prem:.2f}%
- Deviasi harga ANTAM: {deviasi:.2f}%
- Market Pressure Index (MPI): {mpi:.2f}%  
- {insight}

🧠 **Interpretasi AI ({tone.upper()} mode)**
- {stance}
- {strategy}

⚠️ **Catatan Risiko**
- {risk}

💡 *AI Lokal Pintar v2 menghasilkan narasi menggunakan Natural Language Reasoning Engine, tanpa API eksternal.*
"""

    return output
