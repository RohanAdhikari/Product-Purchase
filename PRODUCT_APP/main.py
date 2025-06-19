# Main Streamlit application
import streamlit as st
import logging
import sentry_sdk
import mlflow
import pandas as pd
from datetime import datetime

from config import CATEGORY_DICT, RETURN_POLICY_DICT
from database import init_db, save_prediction
from email_service import send_prediction_email
from logging_setup import setup_logging
from metrics import setup_metrics
from ml_utils import load_model, load_dataset, make_prediction, log_to_mlflow
from ui_components import (
    display_prediction_result,
    display_input_details,
    show_input_form
)
from utils import show_progress
from feedback import ask_feedback, show_feedback_form
from admin_page import show_admin_page
from chatbot import chatbot_ui
from etl.saved_predictions import save_prediction_full


# --- Setup and Initialization ---
logger = setup_logging()
st.set_page_config(page_title="Product Purchase Approval", layout="centered")

# Initialize session state variables
for key in ["admin_logged_in", "view_history", "prediction_made"]:
    if key not in st.session_state:
        st.session_state[key] = False

# Initialize database and MLflow
conn = init_db()
prediction_counter = setup_metrics()
try:
    mlflow.set_experiment("Product_Purchase_Approval")
    logger.info("MLflow experiment setup complete")
except Exception as e:
    logger.error(f"Failed to setup MLflow experiment: {e}")
    st.warning("MLflow tracking might not be working properly")

# Load model and dataset
try:
    model = load_model()
    sample_data = load_dataset()
    logger.info("Model and dataset loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model or dataset: {e}")
    st.error("❌ Failed to load required resources. Please check the logs.")
    st.stop()

# --- Main UI ---
st.title("🛍️ Product Purchase Approval Predictor")
st.markdown("Use this tool to predict whether a product should be **approved for purchase** based on various features.")

# Sidebar Admin Toggle
st.session_state.view_history = st.sidebar.checkbox(
    "🔎 Admin Only",
    value=st.session_state.view_history,
    key="admin_view_checkbox"  # ✅ Fixes Streamlit duplicate element ID issue
)

# Show Admin Page if toggled
if st.session_state.view_history:
    show_admin_page(conn)
    st.stop()

# Show Input Form & Handle Prediction
input_data = show_input_form(sample_data)

if input_data and input_data["username"].strip():
    show_progress()
    try:
        prediction, confidence = make_prediction(model, input_data)

        st.session_state.prediction_made = True
        st.session_state.prediction_result = (prediction, confidence)
        st.session_state.input_for_display = input_data

        prediction_counter.inc()
        logger.info(f"Prediction counter incremented by user: {input_data['username']}")

        # ✅ Save to MLflow
        try:
            log_to_mlflow(input_data["username"], input_data, prediction, confidence)
        except Exception as e:
            logger.warning(f"MLflow logging failed: {e}")

        # ✅ Save to database
        try:
            save_prediction(conn, {
                **input_data,
                "prediction": prediction,
                "confidence": confidence
            })
        except Exception as e:
            logger.error(f"Database save failed: {e}")
            sentry_sdk.capture_exception(e)

        # ✅ Save to saved_predictions.csv
        try:
            save_prediction_full(
                username=input_data["username"],
                category=input_data["category"],
                price_npr=input_data["price_npr"],
                rating=input_data["rating"],
                review_count=input_data["review_count"],
                brand_reputation=input_data["brand_reputation"],
                discount_percent=input_data["discount_percent"],
                availability=input_data["availability"],
                warranty_months=input_data["warranty_months"],
                return_policy=input_data["return_policy"],
                prediction_result=int(prediction)
            )
        except Exception as e:
            logger.error(f"Saving to saved_predictions.csv failed: {e}")
            sentry_sdk.capture_exception(e)

        # ✅ Send email
        try:
            send_prediction_email(input_data["username"], input_data, prediction, confidence)
        except Exception as e:
            logger.warning(f"Email sending failed: {e}")

    except Exception as e:
        st.error(f"❗ Prediction Error: {e}")
        logger.exception("Prediction error occurred")
        sentry_sdk.capture_exception(e)

elif input_data and not input_data["username"].strip():
    st.warning("Please enter your name before predicting.")

# Display prediction results
if st.session_state.get("prediction_result") and st.session_state.get("input_for_display"):
    prediction, confidence = st.session_state.prediction_result
    display_prediction_result(prediction, confidence)
    display_input_details(pd.DataFrame([st.session_state.input_for_display]))

# Feedback Section
if (
    st.session_state.get("prediction_made", False)
    and not st.session_state.get("view_history", False)
    and st.session_state.get("input_for_display", {}).get("username", "").strip() != ""
):
    ask_feedback()
    show_feedback_form()

# Chatbot Section
st.sidebar.markdown("---")
chatbot_ui()
