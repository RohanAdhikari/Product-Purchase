
# Database operations
import sqlite3
from datetime import datetime
import pandas as pd
from config import DB_NAME

def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        username TEXT,
        category TEXT,
        price_npr REAL,
        rating REAL,
        review_count INTEGER,
        brand_reputation TEXT,
        discount_percent INTEGER,
        availability TEXT,
        warranty_months INTEGER,
        return_policy TEXT,
        log_price REAL,
        prediction INTEGER,
        confidence REAL
    )
    """)
    conn.commit()
    return conn

def save_prediction(conn, prediction_data):
    """Save prediction to the database."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions (
            timestamp, username, category, price_npr, rating, review_count, brand_reputation,
            discount_percent, availability, warranty_months, return_policy, log_price, prediction, confidence
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        prediction_data["username"],
        prediction_data["category"],
        prediction_data["price_npr"],
        prediction_data["rating"],
        prediction_data["review_count"],
        prediction_data["brand_reputation"],
        prediction_data["discount_percent"],
        prediction_data["availability"],
        prediction_data["warranty_months"],
        prediction_data["return_policy"],
        prediction_data["log_price"],
        int(prediction_data["prediction"]),
        prediction_data["confidence"]
    ))
    conn.commit()

def get_predictions(conn):
    """Retrieve all predictions from the database."""
    return pd.read_sql_query("SELECT * FROM predictions ORDER BY timestamp DESC", conn)

def delete_predictions(conn, ids_to_delete):
    """Delete predictions by their IDs."""
    cursor = conn.cursor()
    placeholders = ','.join(['?'] * len(ids_to_delete))
    cursor.execute(f"DELETE FROM predictions WHERE id IN ({placeholders})", ids_to_delete)
    conn.commit()
