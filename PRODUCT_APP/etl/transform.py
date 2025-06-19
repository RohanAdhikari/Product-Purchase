import pandas as pd


def transform_feedback(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.drop_duplicates()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0).astype(int)
    df["comments"] = df["comments"].fillna("").str.strip()
    return df


def transform_saved_predictions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.drop_duplicates()

    # Ensure proper types
    numeric_cols = [
        "price_npr", "rating", "review_count", "brand_reputation",
        "discount_percent", "warranty_months", "log_price", "prediction_result"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["availability"] = df["availability"].fillna("").astype(str).str.strip()
    df["return_policy"] = df["return_policy"].fillna("").astype(str).str.strip()
    df["username"] = df["username"].fillna("Anonymous").astype(str).str.strip()

    return df
