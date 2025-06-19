# Configuration and constants
import os

# --- Constants for fixed lists ---
CATEGORY_DICT = {
    "mobile accessories": "Mobile Accessories",
    "beauty": "Beauty",
    "home appliances": "Home Appliances",
    "fashion": "Fashion",
    "electronics": "Electronics"
}

RETURN_POLICY_DICT = {
    "30 days": "30 Days",
    "7 days": "7 Days",
    "15 days": "15 Days",
    "no return": "No Return"
}

# Email Configuration
SENDGRID_API_KEY = "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"
EMAIL_SENDER = "maiyaadhikari2017@gmail.com"
EMAIL_RECEIVER = "kiritootirik578@gmail.com"

# Sentry Configuration
SENTRY_DSN = "https://7f301bd2375c0c0c32955923cd0eb371@o4509506735177728.ingest.us.sentry.io/4509506823913472"

# Database Configuration
DB_NAME = "predictions.db"

# config.py additions for admin tools URLs

MLFLOW_UI_URL = "http://localhost:5000"  # Change to your MLflow UI URL
SENTRY_DASHBOARD_URL = "https://sentry.io/organizations/your-org/projects/your-project/"  # Your Sentry dashboard URL
PROMETHEUS_METRICS_URL = "http://localhost:8000"  # Metrics server URL
