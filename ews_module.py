import pandas as pd

# ================================
# EWS PRO — Analytic Rules
# ================================
def analyze_global_price(global_df):
    """Analisis pergerakan harga global (gold price)."""
    try:
        today = global_df["Close"].iloc[-1]
        yesterday = global_df["Close"].iloc[-2]
        change_pct = ((today - yesterday) / yesterday) * 100

        if change_pct > 1.5:
            return {
                "indicator": "Gold Price Global",
                "severity": "high",
                "change": change_pct,
                "reason": f"Harga emas global naik signifikan {change_pct:.2f}%.",
                "recommendation": "Pantau dampak ke harga jual LM hari ini."
            }
        elif change_pct < -1.2:
            return {
                "indicator": "Gold Price Global",
                "severity": "moderate",
                "change": change_pct,
                "reason": f"Harga emas global turun {change_pct:.2f}%.",
                "recommendation": "Evaluasi strategi harga jika penurunan berlanjut."
            }
        else:
            return {
                "indicator": "Gold Price Global",
                "severity": "stable",
                "change": change_pct,
                "reason": "Pergerakan harga global stabil.",
                "recommendation": "-"
            }
    except:
        return None


def analyze_competitor_price(comp_df):
    """Analisis perubahan harga kompetitor."""
    try:
        comp_df["avg_price"] = comp_df.mean(axis=1)
        today = comp_df["avg_price"].iloc[-1]
        yesterday = comp_df["avg_price"].iloc[-2]
        change_pct = ((today - yesterday) / yesterday) * 100

        if change_pct <= -2:
            return {
                "indicator": "Harga Kompetitor",
                "severity": "high",
                "change": change_pct,
                "reason": f"Kompetitor menurunkan harga {change_pct:.2f}%. Indikasi price war.",
                "recommendation": "Pertimbangkan penyesuaian harga atau bundling promo."
            }
        elif change_pct <= -1:
            return {
                "indicator": "Harga Kompetitor",
                "severity": "moderate",
                "change": change_pct,
                "reason": f"Harga kompetitor turun {change_pct:.2f}%.",
                "recommendation": "Pantau apakah ada tren penurunan lanjutan."
            }
        else:
            return {
                "indicator": "Harga Kompetitor",
                "severity": "stable",
                "change": change_pct,
                "reason": "Harga kompetitor stabil.",
                "recommendation": "-"
            }
    except:
        return None


def analyze_traffic(traffic_df):
    """Analisis penurunan traffic website/apps."""
    try:
        today = traffic_df["Visits"].iloc[-1]
        avg_week = traffic_df["Visits"].tail(7).mean()
        change_pct = ((today - avg_week) / avg_week) * 100

        if change_pct <= -20:
            return {
                "indicator": "Traffic",
                "severity": "high",
                "change": change_pct,
                "reason": f"Traffic turun tajam {change_pct:.2f}%.",
                "recommendation": "Aktifkan push notif / promo digital."
            }
        elif change_pct <= -10:
            return {
                "indicator": "Traffic",
                "severity": "moderate",
                "change": change_pct,
                "reason": f"Traffic turun {change_pct:.2f}%.",
                "recommendation": "Pertimbangkan aktivitas marketing ringan."
            }
        else:
            return {
                "indicator": "Traffic",
                "severity": "stable",
                "change": change_pct,
                "reason": "Traffic stabil.",
                "recommendation": "-"
            }
    except:
        return None


# ================================
# MAIN FUNCTION (untuk app.py)
# ================================
def ews_pro(global_df, competitor_df, traffic_df):
    alerts = []

    a = analyze_global_price(global_df)
    if a: alerts.append(a)

    b = analyze_competitor_price(competitor_df)
    if b: alerts.append(b)

    c = analyze_traffic(traffic_df)
    if c: alerts.append(c)

    return alerts
