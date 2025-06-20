import pandas as pd
from pathlib import Path

PROCESSED_FEEDBACK_FILE = Path("datasets/processed_feedback.csv")
PROCESSED_SAVED_PREDICTIONS_FILE = Path("datasets/processed_saved_predictions.csv")


def load_feedback(df: pd.DataFrame):
    PROCESSED_FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_FEEDBACK_FILE, index=False)


def load_saved_predictions(df: pd.DataFrame):
    PROCESSED_SAVED_PREDICTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_SAVED_PREDICTIONS_FILE, index=False)
