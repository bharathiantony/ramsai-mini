# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 23:37:04 2026

@author: Bharathiraja
"""

import pandas as pd
from prophet import Prophet

# -----------------------------
# CONFIG
# -----------------------------
INPUT_FILE = "Food.xlsx"     # <-- your category file
MONTH_COL = "Month"          # <-- column name in your file
AMOUNT_COL = "Amount"        # <-- column name in your file
FORECAST_MONTHS = 12         # <-- how many months ahead

# -----------------------------
# LOAD & PREPARE (Prophet needs ds, y)
# -----------------------------
df = pd.read_excel(INPUT_FILE)

# If Month is like "2024-01" or "2024-01-01"
df[MONTH_COL] = pd.to_datetime(df[MONTH_COL])

prophet_df = df.rename(columns={MONTH_COL: "ds", AMOUNT_COL: "y"})[["ds", "y"]]
prophet_df = prophet_df.sort_values("ds")

# Ensure monthly start frequency (MS = Month Start).
# If your ds already is month start, fine. If not, normalize:
prophet_df["ds"] = prophet_df["ds"].dt.to_period("M").dt.to_timestamp("MS")

# Fill missing months (recommended)
prophet_df = (
    prophet_df.set_index("ds")
              .asfreq("MS")            # monthly start frequency
              .fillna(0)               # or .interpolate() depending on your case
              .reset_index()
)

# -----------------------------
# MOVING HOLIDAYS / CALENDAR DAYS
# -----------------------------
# Example: India-focused "moving" days + fixed-date holidays.
# Adjust list to what matters for your spend pattern.

years = range(prophet_df["ds"].dt.year.min(), prophet_df["ds"].dt.year.max() + 3)

holidays = []

# Fixed-date (same date every year)
for y in years:
    holidays += [
        {"holiday": "new_year", "ds": f"{y}-01-01", "lower_window": 0, "upper_window": 2},
        {"holiday": "independence_day", "ds": f"{y}-08-15", "lower_window": -1, "upper_window": 1},
        {"holiday": "gandhi_jayanti", "ds": f"{y}-10-02", "lower_window": -1, "upper_window": 1},
        {"holiday": "christmas", "ds": f"{y}-12-25", "lower_window": -2, "upper_window": 2},
    ]

# Moving / variable-date holidays (you supply actual dates per year)
# Replace these with the dates you want (Pongal, Diwali, Eid, etc.)
# Example placeholders (EDIT THESE):
moving_dates = {
    2024: {"diwali": "2024-11-01", "eid": "2024-04-10", "pongal": "2024-01-15"},
    2025: {"diwali": "2025-10-20", "eid": "2025-03-31", "pongal": "2025-01-15"},
    2026: {"diwali": "2026-11-08", "eid": "2026-03-20", "pongal": "2026-01-15"},
}

for y, events in moving_dates.items():
    for name, date_str in events.items():
        holidays.append({
            "holiday": name,
            "ds": date_str,
            "lower_window": -3,   # impact starts 3 days before
            "upper_window": 3     # impact lasts 3 days after
        })

holidays_df = pd.DataFrame(holidays)
holidays_df["ds"] = pd.to_datetime(holidays_df["ds"])

# -----------------------------
# TRAIN PROPHET
# -----------------------------
m = Prophet(
    holidays=holidays_df,
    yearly_seasonality=True,
    weekly_seasonality=False,   # monthly data doesn't need weekly
    daily_seasonality=False,
    seasonality_mode="additive" # try "multiplicative" if variance scales with level
)

m.fit(prophet_df)

# -----------------------------
# FORECAST
# -----------------------------
future = m.make_future_dataframe(periods=FORECAST_MONTHS, freq="MS")
forecast = m.predict(future)

# Save outputs
forecast_out = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
forecast_out.to_excel("forecast_output.xlsx", index=False)

print(forecast_out.tail(10))