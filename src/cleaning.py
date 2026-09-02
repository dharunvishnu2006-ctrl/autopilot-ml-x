import re
import pandas as pd


def detect_date_columns(df: pd.DataFrame) -> list[str]:
    date_cols = []
    for col in df.select_dtypes(include=["object","str"]).columns:
        sample = df[col].dropna().head(20)
        if sample.empty:
            continue
        has_separator = sample.astype(str).str.contains(
            r"[-/]").all()           
        if not has_separator:
            continue
        parsed = pd.to_datetime(sample, errors="coerce",
                                 format="mixed")
        hit_rate = parsed.notna().mean()
        if hit_rate >= 0.9:
            date_cols.append(col)
    return date_cols


def parse_date_columns(df: pd.DataFrame,
                        date_cols: list[str]) -> pd.DataFrame:
    df = df.copy()
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce",
                                  format="mixed")
    return df


EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


def clean_text_column(series: pd.Series) -> dict:
    cleaned = series.astype(str).str.strip()
    cleaned = cleaned.str.replace(r"\s+", " ", regex=True)
    matches = cleaned.str.match(EMAIL_RE)
    fail_count = int((~matches.fillna(False)).sum())
    return {"cleaned": cleaned, "pattern_failures": fail_count}