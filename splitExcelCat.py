# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 23:11:38 2026

@author: User
"""

import os
import re
import pandas as pd

INPUT_FILE = "student_data.xlsx"       # <-- change
SHEET_NAME = 0                  # 0 = first sheet, or use "Sheet1"
CATEGORY_COL = "Category"       # <-- change to your exact column name
OUTPUT_DIR = "split_output"

def safe_filename(name: str) -> str:
    name = str(name).strip()
    name = re.sub(r'[\\/*?:"<>|]+', "_", name)  # remove illegal filename chars
    name = re.sub(r"\s+", " ", name)
    return name[:150] if name else "EMPTY"

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_excel(INPUT_FILE, sheet_name=SHEET_NAME)

    # Make sure column exists (case-insensitive fallback)
    cols_lower = {c.lower(): c for c in df.columns}
    if CATEGORY_COL not in df.columns:
        if CATEGORY_COL.lower() in cols_lower:
            CATEGORY_COL_REAL = cols_lower[CATEGORY_COL.lower()]
        else:
            raise ValueError(f"Column '{CATEGORY_COL}' not found. Available: {list(df.columns)}")
    else:
        CATEGORY_COL_REAL = CATEGORY_COL

    # Split & write
    for cat_value, group in df.groupby(CATEGORY_COL_REAL, dropna=False):
        fname = safe_filename(cat_value)
        out_path = os.path.join(OUTPUT_DIR, f"{fname}.xlsx")
        group.to_excel(out_path, index=False)

    print(f"Done. Created files in: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()