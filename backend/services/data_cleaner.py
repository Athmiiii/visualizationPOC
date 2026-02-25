"""
data_cleaner.py — Cleans a raw DataFrame and produces a human-readable report.
"""

import pandas as pd
from typing import Tuple


def clean_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
    """
    Inspect and auto-fix common data quality issues in a DataFrame.

    Checks performed:
      - Duplicate rows  → dropped
      - Null / NaN values → filled with median (numeric) or mode (categorical)
      - Inconsistent string casing → normalised to title case
      - Object columns that look numeric → coerced to numeric dtype

    Returns:
      - cleaned DataFrame
      - cleaning_report dict listing every change that was made
    """
    report: dict = {
        "duplicates_removed": 0,
        "nulls_filled": {},
        "type_conversions": [],
        "casing_normalised": [],
    }

    original_len = len(df)

    # --- 1. Drop duplicate rows ---
    df = df.drop_duplicates()
    report["duplicates_removed"] = original_len - len(df)

    # --- 2. Fill null values ---
    for col in df.columns:
        null_count = df[col].isna().sum()
        if null_count == 0:
            continue

        if pd.api.types.is_numeric_dtype(df[col]):
            fill_value = df[col].median()
            df[col] = df[col].fillna(fill_value)
            report["nulls_filled"][col] = {
                "count": int(null_count),
                "strategy": "median",
                "value": fill_value,
            }
        else:
            mode_series = df[col].mode()
            fill_value = mode_series[0] if not mode_series.empty else ""
            df[col] = df[col].fillna(fill_value)
            report["nulls_filled"][col] = {
                "count": int(null_count),
                "strategy": "mode",
                "value": fill_value,
            }

    # --- 3. Coerce object columns that are actually numeric ---
    for col in df.select_dtypes(include=["object"]).columns:
        coerced = pd.to_numeric(df[col], errors="coerce")
        if coerced.notna().sum() / len(df) > 0.8:  # >80 % successfully parsed
            df[col] = coerced
            report["type_conversions"].append(
                {"column": col, "from": "object", "to": "numeric"}
            )

    # --- 4. Normalise string casing to title case ---
    for col in df.select_dtypes(include=["object"]).columns:
        if df[col].str.strip().str.istitle().mean() < 0.8:
            df[col] = df[col].str.strip().str.title()
            report["casing_normalised"].append(col)

    return df, report
