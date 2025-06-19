# Utility functions
import time
import streamlit as st

def show_progress():
    """Display progress spinner and bar."""
    with st.spinner("⏳ Predicting... Please wait"):
        progress = st.progress(0)
        for i in range(0, 101, 10):
            time.sleep(0.05)
            progress.progress(i)

