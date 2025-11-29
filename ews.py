def ews_check(global_df, competitor_df, traffic_df):
    alerts = []

    # -----------------------------
    # Auto-detect kolom traffic
    # -----------------------------
    possible_cols = ["visits", "traffic", "visitor", "count", "value", "jumlah"]
    traffic_col = None

    for c in possible_cols:
        if c in traffic_df.columns:
            traffic_col = c
            break

    # Jika tidak ada kolom valid
    if traffic_col is None:
        return [("Kolom traffic tidak ditemukan. Periksa load_traffic().", "danger")]

    # Traffic Drop Logic
    if len(traffic_df) >= 7:
        today = traffic_df[traffic_col].iloc[-1]
        week_avg = traffic_df[traffic_col].iloc[-7:].mean()

        if today < week_avg * 0.75:
            alerts.append(("Penurunan traffic lebih dari 25%", "danger"))
        elif today < week_avg * 0.90:
            alerts.append(("Traffic menurun minggu ini", "warning"))

    # -----------------------------
    # Check harga emas dunia
    # -----------------------------
    if len(global_df) >= 2:
        last = global_df["price"].iloc[-1]
        prev = global_df["price"].iloc[-2]
        change = (last - prev) / prev * 100

        if change > 1.5:
            alerts.append((f"Harga emas dunia melonjak {change:.2f}%", "danger"))
        elif change < -1.5:
            alerts.append((f"Harga emas dunia turun tajam {change:.2f}%", "danger"))
        elif abs(change) > 0.5:
            alerts.append((f"Harga emas dunia bergerak signifikan {change:.2f}%", "warning"))

    # -----------------------------
    # Price war
    # -----------------------------
    if "gap" in competitor_df.columns:
        worst_gap = competitor_df["gap"].min()
        if worst_gap < -1500:
            alerts.append(("Gap kompetitor sangat negatif (indikasi price war)", "danger"))
        elif worst_gap < -500:
            alerts.append(("Gap kompetitor menurun", "warning"))

    return alerts
