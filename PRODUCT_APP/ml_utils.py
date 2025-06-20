
# ML model and data loading
import os
import pickle
import numpy as np
import mlflow
import pandas as pd
import streamlit as st
from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory (PythonProject/)"""
    return Path(__file__).parent.parent


@st.cache_resource
def load_model():
    """Load the trained model."""
    model_path = get_project_root() / "models" / "best_svm_model_pipeline.pkl"
    dvc_pull(model_path)
    with open(model_path, "rb") as f:
        return pickle.load(f)


@st.cache_data
def load_dataset():
    """Load the sample dataset."""
    dataset_path = get_project_root() / "datasets" / "products_dataset.pkl"
    dvc_pull(dataset_path)
    with open(dataset_path, "rb") as f:
        return pickle.load(f)


def dvc_pull(file_path: Path):
    """Pull file from DVC if it doesn't exist.
    Args:
        file_path: Absolute path to the file
    """
    # Convert to relative path for DVC command (from project root)
    rel_path = file_path.relative_to(get_project_root())

    if not file_path.exists():
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Execute DVC pull with relative path
        ret = os.system(f'cd {get_project_root()} && dvc pull {rel_path}')

        if ret != 0:
            raise RuntimeError(f"DVC pull failed for {rel_path}")

        if not file_path.exists():
            raise FileNotFoundError(
                f"File {file_path} not found after DVC pull. "
                f"Check if {rel_path} is tracked in DVC."
            )


def make_prediction(model, input_data):
    """Make prediction using the model."""
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)[0]
    confidence = model.predict_proba(input_df)[0][1]
    return prediction, confidence


def log_to_mlflow(username, input_data, prediction, confidence):
    """Log prediction to MLflow."""
    with mlflow.start_run():
        mlflow.set_tag("user", username)
        for k, v in input_data.items():
            mlflow.log_param(k, str(v))
        mlflow.log_metric("prediction", int(prediction))
        mlflow.log_metric("confidence", float(confidence))