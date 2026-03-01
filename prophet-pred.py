import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("expenses.csv")

# Prophet expects ds and y
df['ds'] = pd.to_datetime(df['ds'])
df = df[['ds', 'y']]

# -----------------------------
# Train model
# -----------------------------
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False
)

model.fit(df)

# -----------------------------
# Create future dates
# -----------------------------
future = model.make_future_dataframe(periods=12, freq='W')

# -----------------------------
# Predict
# -----------------------------
forecast = model.predict(future)

# -----------------------------
# Plot
# -----------------------------
model.plot(forecast)
plt.show()

print(forecast[['ds','yhat','yhat_lower','yhat_upper']].tail())
