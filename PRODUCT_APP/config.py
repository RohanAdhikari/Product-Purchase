# config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Calculate project root directory (two levels up from this file)
project_root = Path(__file__).resolve().parents[1]  # PRODUCT_APP -> PythonProject

# Load .env file from project root
load_dotenv(dotenv_path=project_root / '.env')

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

# --- Secrets and Config from Environment Variables ---
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

username_input = os.getenv('username_input')
password_input = os.getenv('password_input')

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')

# Sentry Configuration
SENTRY_DSN = os.getenv('SENTRY_DSN')

# Database Configuration
DB_NAME = os.getenv('DB_NAME', "predictions.db")

# Admin tools URLs
MLFLOW_UI_URL = os.getenv('MLFLOW_UI_URL', "http://localhost:5000")
SENTRY_DASHBOARD_URL = os.getenv('SENTRY_DASHBOARD_URL', "https://sentry.io/organizations/your-org/projects/your-project/")
PROMETHEUS_METRICS_URL = os.getenv('PROMETHEUS_METRICS_URL', "http://localhost:8000")
