"""
 This file converts the raw SARS export files (.xls) into .csv files.

Why: I downloaded the SARS data as .xls, but I prefer working with 
CSV files because they're easier to open and check in a text editor.

When to run this: only once, after downloading new SARS files. 
This script is NOT part of the main pipeline - main.py doesn't call it.
"""

import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def convert_all():
    xls_files = list(RAW_DIR.glob("*.xls")) + list(RAW_DIR.glob("*.xlsx"))
    if not xls_files:
        print(f"No .xls/.xlsx files found in {RAW_DIR}")
        return

    for f in xls_files:
        df = pd.read_excel(f)
        out_path = f.with_suffix(".csv")
        df.to_csv(out_path, index=False)
        print(f"Converted {f.name} -> {out_path.name} ({len(df)} rows)")


if __name__ == "__main__":
    convert_all()