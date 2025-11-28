import requests
from datetime import datetime

# ============================
# API ENDPOINTS
# ============================
URL_INDOGOLD = "https://old-river-ece0.best-adeprasetyo.workers.dev/indogold"
URL_HRTA = "https://old-river-ece0.best-adeprasetyo.workers.dev/hartadinata"
URL_GALERI24 = "https://old-river-ece0.best-adeprasetyo.workers.dev/galeri24"
URL_SPOT = "https://data-asli-kamu.com/api/spot"   # ganti sesuai endpoint spot emas kamu


# ============================
# HELPER FUNCTION
# ============================
def fetch_json(url):
    try:
        res = requests.get(url, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}


# ============================
# PRICE MODEL
# ============================
def calculate_premium(price, spot_gram):
    """Premium vs spot price."""
    return (price / spot_gram) - 1


def recommend_price(my_price, competitor_avg, elasticity=0.3):
    """
    elasticity rendah = harga bisa lebih tinggi
    elasticity tinggi = harus menyesuaikan lebih sensitif
    """
    adjustment = (competitor_avg - my_price) * elasticity
    return round(my_price + adjustment)


# ============================
# MAIN APP
# ============================
def main():
    print("\n======================================")
    print("       DAILY PRICE ELASTICITY AI      ")
    print("======================================\n")

    # --- FETCH DATA ---
    indogold = fetch_json(URL_INDOGOLD)
    hrta = fetch_json(URL_HRTA)
    g24 = fetch_json(URL_GALERI24)
    spot = fetch_json(URL_SPOT)

    # --- Spot Validation ---
    if "gram" not in spot:
        print("❌ Tidak dapat mengambil harga spot emas.")
        return

    spot_idr = spot["gram"]
    print(f"Spot Gold (IDR/gram): Rp {spot_idr:,}\n")

    # --- Competitor Data ---
    print("=== Competitor Prices ===")

    def print_competitor(name, data):
        if "jual" in data:
            print(f"{name:<15} Jual: Rp {data['jual']:,}   |   Beli: Rp {data['beli']:,}")
        else:
            print(f"{name:<15} Data tidak tersedia.")

    print_competitor("IndoGold", indogold)
    print_competitor("Hartadinata", hrta)
    print_competitor("Galeri 24", g24)

    # --- AVERAGE COMPETITOR ---
    competitor_sell = [
        c["jual"] for c in [indogold, hrta, g24] if "jual" in c
    ]

    if len(competitor_sell) == 0:
        print("\n❌ Tidak ada data competitor yang valid.")
        return

    avg_competitor = sum(competitor_sell) / len(competitor_sell)
    print(f"\nRata-rata Harga Jual Competitor: Rp {avg_competitor:,.0f}")

    # --- PREMIUM CALC ---
    print("\n=== Premium vs Spot ===")
    competitors = [
        ("IndoGold", indogold),
        ("Hartadinata", hrta),
        ("Galeri 24", g24)
    ]

    for name, data in competitors:
        if "jual" in data:
            premium = calculate_premium(data["jual"], spot_idr)
            print(f"{name:<15} Premium: {premium*100:.2f}%")

    # --- Input Harga Kamu ---
    try:
        my_price = int(input("\nMasukkan harga jual kamu (Rp): "))
    except:
        print("❌ Input tidak valid.")
        return

    # --- Rekomendasi AI ---
    recommended = recommend_price(my_price, avg_competitor)
    gap = my_price - avg_competitor

    print("\n=== AI Price Recommendation ===")
    print(f"Harga Kamu Saat Ini  : Rp {my_price:,}")
    print(f"Rata-rata Competitor : Rp {avg_competitor:,.0f}")
    print(f"Gap Harga            : Rp {gap:,.0f}")
    print(f"Rekomendasi AI       : Rp {recommended:,}")

    # --- Price Elasticity Score ---
    elasticity_score = min(1, max(0, abs(gap) / avg_competitor))

    print("\n=== Price Elasticity Score ===")
    print(f"Skor Elastisitas (0-1) : {elasticity_score:.3f}")
    print("Keterangan:")
    print("  0   = Tidak sensitif (bisa naik harga)")
    print("  1   = Sangat sensitif (harus hati-hati)")

    print("\nSelesai ✔")


if __name__ == "__main__":
    main()
