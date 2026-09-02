from src.pipeline import pipeline
from src.cleaning import detect_date_columns, parse_date_columns


@pipeline
def profile(df) -> dict:
    """Return a dict report for any dataset."""
    date_cols = detect_date_columns(df)     
    df = parse_date_columns(df, date_cols)   

    report = {
        "rows": df.shape[0],
        "cols": df.shape[1],
        "column_names": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "numeric_summary": df.describe().to_dict(),
        "date_columns_detected": date_cols,
    }

    return report