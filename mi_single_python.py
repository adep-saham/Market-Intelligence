# ============================================================
#  Market Intelligence System - UBPP Logam Mulia
#  Full single-file version WITHOUT sklearn (safe for Streamlit)
# ============================================================

import pandas as pd

# ------------------------------------------------------------
# 1. DATA LOADER
# ------------------------------------------------------------
def load_global_price(path="data/harga_global.csv"):
    return pd.read_csv(path)

def load_competitor(path="data/kompetitor.csv"):
    return pd.read_csv(path)

def load_sales(path="data/penjualan_lm.csv"):
    return pd.read_csv(path)

def load_traffic(path="data/traffic_website.csv"):
    return pd.read_csv(path)

# ------------------------------------------------------------
# 2. COMPETITOR MONITORING
# ------------------------------------------------------------
def detect_price_gap(lm_price, competitor_df):
    competitor_df["gap"] = competitor_df["price"] - lm_price
    competitor_df["status"] = competitor_df["gap"].apply(
        lambda x: "lebih murah" if x < 0 else "lebih mahal"
    )
    return competitor_df

def near_price_war(competitor_df, threshold=-500):
    return competitor_df[competitor_df["gap"] < threshold]

# ------------------------------------------------------------
# 3. EARLY WARNING SYSTEM (EWS)
# ------------------------------------------------------------
def check_global_price_spike(global_price_df, threshold=1.0):
    global_price_df["pct_change"] = global_price_df["price"].pct_change() * 100
    return global_price_df[global_price_df["pct_change"].abs() > threshold]

def check_traffic_drop(traffic_df, threshold=-30):
    traffic_df["pct_change"] = traffic_df["traffic"].pct_change() * 100
    return traffic_df[traffic_df["pct_change"] < threshold]

def generate_alerts(global_spike, competitor_war, traffic_drop):
    alerts = []
    if not global_spike.empty:
        alerts.append("⚠ Harga emas global bergerak ekstrem!")
    if not competitor_war.empty:
        alerts.append("⚠ Kompetitor memulai perang harga!")
    if not traffic_drop.empty:
        alerts.append("⚠ Traffic website turun signifikan!")
    return alerts

# ------------------------------------------------------------
# 4. FORECASTING (PURE PYTHON LINEAR REGRESSION)
# ------------------------------------------------------------
def forecast_demand(sales_df, days_forward=7):
    sales_df = sales_df.dropna()

    sales_df["t"] = range(len(sales_df))
    x = sales_df["t"].values
    y = sales_df["qty"].values

    # manual regression
    n = len(x)
    slope = (n * (x*y).sum() - x.sum()*y.sum()) / (n*(x**2).sum() - (x.sum()**2))
    intercept = (y.sum() - slope * x.sum()) / n

    # predict future
    future_t = range(len(sales_df), len(sales_df) + days_forward)
    forecasts = [slope * t + intercept for t in future_t]

    return pd.DataFrame({
        "t": list(future_t),
        "forecast_qty": forecasts
    })

# ------------------------------------------------------------
# 5. PRICING RECOMMENDATION ENGINE
# ------------------------------------------------------------
def recommend_price(global_price, competitor_df, elasticity=-0.8):
    avg_competitor = competitor_df["price"].mean()
    recommended = (global_price * 0.8) + (avg_competitor * 0.2)

    # sensitivity adjustment
    if elasticity < -0.5:
        recommended *= 1.01

    return round(recommended, 0)

# ------------------------------------------------------------
# 6. MAIN RUNNER
# ------------------------------------------------------------
def run_mi_system():
    global_price = load_global_price()
    competitor = load_competitor()
    sales = load_sales()
    traffic = load_traffic()

    lm_price = global_price["price"].iloc[-1]
    gap = detect_price_gap(lm_price, competitor.copy())

    forecast = forecast_demand(sales)

    alerts = generate_alerts(
        check_global_price_spike(global_price.copy()),
        near_price_war(gap.copy()),
        check_traffic_drop(traffic.copy())
    )

    rec_price = recommend_price(lm_price, competitor)

    return {
        "price_gap": gap,
        "forecast": forecast,
        "alerts": alerts,
        "recommended_price": rec_price
    }

# ------------------------------------------------------------
# Uncomment to test locally
# result = run_mi_system()
# print(result)
