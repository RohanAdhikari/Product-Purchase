from etl.extract import extract_feedback, extract_saved_predictions
from etl.transform import transform_feedback, transform_saved_predictions
from etl.load import load_feedback, load_saved_predictions


def run_etl_pipeline():
    # Process feedback
    raw_feedback = extract_feedback()
    clean_feedback = transform_feedback(raw_feedback)
    load_feedback(clean_feedback)

    # Process saved predictions
    raw_saved_predictions = extract_saved_predictions()
    clean_saved_predictions = transform_saved_predictions(raw_saved_predictions)
    load_saved_predictions(clean_saved_predictions)
