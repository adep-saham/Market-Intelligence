import pandas as pd

# ======================================================
# 1. DATA LOADER
# ======================================================

def load_global_price(path="data/harga_global.csv"):
    return pd.read_csv(path)

def load_competitor(path="data/kompetitor.csv"):
    return pd.read_csv(path)

def load_sales(path="data/penjualan_lm.csv"):
    return pd.read_csv(path)

def load_traffic(path="data/traffic_website.csv"):
    return pd.read_csv(path)


# ======================================================
# 2. COMPETITOR MONITORING
# ======================================================

def detect_price_gap(lm_price, competitor_df):
    competitor_df = competitor_df.copy()
    competitor_df["gap"] = competitor_df["price"] - lm_price
    competitor_df["status"] = competitor_df["gap"].apply(
        lambda x: "lebih murah" if x < 0 else "lebih mahal"
    )
    return competitor_df

def near_price_war(competitor_df, threshold=-500):
    # perang harga jika gap < threshold
    return competitor_df[competitor_df["gap"] < threshold]


# ======================================================
# 3. EARLY WARNING SYSTEM (EWS)
# ======================================================

def check_global_price_spike(global_price_df, threshold=1.0):
    df = global_price_df.copy()
    df["pct_change"] = df["price"].pct_change() * 100
    return df[df["pct_change"].abs() > threshold]

def check_traffic_drop(traffic_df, threshold=-30):
    df = traffic_df.copy()
    df["pct_change"] = df["traffic"].pct_change() * 100
    return df[df["pct_change"] < threshold]

def generate_alerts(global_spike, competitor_war, traffic_drop):
    alerts = []

    if not global_spike.empty:
        alerts.append("⚠ Harga emas global bergerak ekstrem!")

    if not competitor_war.empty:
        alerts.append("⚠ Kompetitor memulai perang harga!")

    if not traffic_drop.empty:
        alerts.append("⚠ Traffic website turun signifikan!")

    return alerts


# ======================================================
# 4. FORECAST DEMAND (NO SKLEARN – MANUAL LR)
# ======================================================

def forecast_demand(sales_df, days_forward=7):
    df = sales_df.copy().dropna()
    df["t"] = range(len(df))

    x = df["t"].values
    y = df["qty"].values

    n = len(x)

    # manual slope & intercept
    slope = (n * (x*y).sum() - x.sum()*y.sum()) / (n*(x**2).sum() - (x.sum()**2))
    intercept = (y.sum() - slope * x.sum()) / n

    future_t = range(len(df), len(df) + days_forward)
    forecasts = [slope * t + intercept for t in future_t]

    return pd.DataFrame({
        "t": list(future_t),
        "forecast_qty": forecasts
    })


# ======================================================
# 5. PRICING ENGINE
# ======================================================

def recommend_price(global_price, competitor_df, elasticity=-0.8):
    avg_competitor = competitor_df["price"].mean()
    recommended = (global_price * 0.8) + (avg_competitor * 0.2)

    if elasticity < -0.5:
        recommended *= 1.01

    return round(recommended, 0)
