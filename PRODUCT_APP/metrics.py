# Prometheus metrics
import streamlit as st
from prometheus_client import start_http_server, Counter, REGISTRY
import threading
import logging

# Set up logging
logger = logging.getLogger(__name__)


def start_metrics_server():
    """Start Prometheus metrics server."""
    try:
        start_http_server(8000)
        logger.info("Prometheus metrics server started on port 8000")
    except OSError as e:
        if "Address already in use" in str(e):
            logger.info("Metrics server already running")
        else:
            logger.error(f"Failed to start metrics server: {e}")
            raise


def get_or_create_counter(name, description):
    """Get existing counter or create new one."""
    try:
        counter = REGISTRY._names_to_collectors.get(name)
        if counter is None:
            counter = Counter(name, description)
            logger.info(f"Created new counter: {name}")
        else:
            logger.debug(f"Using existing counter: {name}")
        return counter
    except Exception as e:
        logger.error(f"Error getting/creating counter: {e}")
        raise


def setup_metrics():
    """Initialize metrics and start server."""
    try:
        # Initialize session state if not exists
        if not hasattr(st, 'session_state'):
            raise RuntimeError("Streamlit session state not available")

        if "metrics_started" not in st.session_state:
            logger.info("Starting metrics server thread")
            metrics_thread = threading.Thread(
                target=start_metrics_server,
                daemon=True,
                name="prometheus_metrics_thread"
            )
            metrics_thread.start()
            st.session_state.metrics_started = True
            logger.info("Metrics server thread started")

        prediction_counter = get_or_create_counter(
            'product_predictions_total',
            'Total product predictions made'
        )
        return prediction_counter

    except Exception as e:
        logger.error(f"Metrics setup failed: {e}")
        raise