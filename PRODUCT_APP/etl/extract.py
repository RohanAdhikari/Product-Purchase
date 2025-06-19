import pandas as pd
from pathlib import Path

FEEDBACK_FILE = Path("datasets/feedback.csv")
SAVED_PREDICTIONS_FILE = Path("datasets/saved_predictions.csv")


def extract_feedback():
    if FEEDBACK_FILE.exists():
        return pd.read_csv(FEEDBACK_FILE)
    else:
        return pd.DataFrame(columns=["username", "rating", "comments", "timestamp"])


def extract_saved_predictions():
    if SAVED_PREDICTIONS_FILE.exists():
        return pd.read_csv(SAVED_PREDICTIONS_FILE)
    else:
        return pd.DataFrame(columns=[
            "username", "category", "price_npr", "rating", "review_count", "brand_reputation",
            "discount_percent", "availability", "warranty_months", "return_policy",
            "log_price", "prediction_result", "timestamp"
        ])
