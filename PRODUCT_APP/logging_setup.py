# Logging and Sentry setup
import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from config import SENTRY_DSN


def setup_logging():
    """Configure logging and Sentry integration."""
    # Sentry Setup (Logging Integration Only)
    sentry_logging = LoggingIntegration(
        level=logging.INFO,  # Capture info and above as breadcrumbs
        event_level=logging.ERROR  # Send errors as events
    )

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[sentry_logging],
        traces_sample_rate=1.0,  # Adjust sampling rate as needed
        send_default_pii=True
    )

    # Logging Setup
    logger = logging.getLogger("product_app_logger")
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(console_handler)

    return logger