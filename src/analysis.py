import pandas as pd
import numpy as np


def profile_by_group(df: pd.DataFrame, group_col: str,
                      value_col: str) -> pd.DataFrame:
    grouped = df.groupby(group_col)[value_col].agg(
        count="count",
        missing=lambda s: s.isna().sum(),
        total=lambda s: len(s))
    grouped["missing_rate"] = (
        grouped["missing"] / grouped["total"] * 100)
    return grouped.reset_index()

def compare_runs(current: pd.DataFrame,
                  previous: pd.DataFrame) -> pd.DataFrame:
    merged = current.merge(
        previous, on="name", how="outer",
        suffixes=("_now", "_before"), indicator=True)

    merged["missing_delta"] = (
        merged["missing_now"] - merged["missing_before"])

    conditions = [
        merged["_merge"] == "left_only",
        merged["_merge"] == "right_only",
        merged["missing_delta"] > 0,
    ]
    choices = ["NEW COLUMN", "COLUMN DISAPPEARED", "MORE MISSING"]
    merged["status"] = np.select(
        conditions, choices, default="stable")

    return merged