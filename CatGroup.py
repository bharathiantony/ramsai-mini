# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 23:20:44 2026

@author: Bharathiraja
"""

import pandas as pd

# Load Excel
df = pd.read_excel("Travel.xlsx")

# 🔹 Ensure date is datetime
df['Date'] = pd.to_datetime(df['Date'])

# 🔹 Convert to YYYY-MM
df['Date'] = df['Date'].dt.to_period('M').astype(str)

# 🔹 Group by month and sum amount
monthly_sum = (
    df.groupby('Date', as_index=False)['Amount']
      .sum()
)

print(monthly_sum)

# 🔹 Save to Excel
monthly_sum.to_excel("Travel_Purchase.xlsx", index=False)