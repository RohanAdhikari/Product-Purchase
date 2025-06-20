# email_service.py
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime
import logging
import sentry_sdk
from config import SENDGRID_API_KEY, EMAIL_SENDER, EMAIL_RECEIVER

def send_prediction_email(user, input_data, prediction, confidence):
    """Send email notification about prediction."""
    if not SENDGRID_API_KEY:
        logging.warning("SendGrid API key not set. Email will not be sent.")
        return

    if not EMAIL_SENDER or not EMAIL_RECEIVER:
        logging.warning("Email sender or receiver not set. Email will not be sent.")
        return

    subject = f"New Product Purchase Prediction by {user}"
    body = f"""
Hello,

A new product purchase prediction was made.

User: {user}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Product Details:
Category: {input_data['category']}
Price (NPR): {input_data['price_npr']}
Rating: {input_data['rating']}
Review Count: {input_data['review_count']}
Brand Reputation: {input_data['brand_reputation']}
Discount (%): {input_data['discount_percent']}
Availability: {input_data['availability']}
Warranty (months): {input_data['warranty_months']}
Return Policy: {input_data['return_policy']}

Prediction: {"Recommended to Buy ✅" if prediction == 1 else "Not Recommended to Buy ❌"}
Confidence: {confidence:.2%}

Best regards,
Product Approval System
"""

    try:
        message = Mail(
            from_email=EMAIL_SENDER,
            to_emails=EMAIL_RECEIVER,
            subject=subject,
            plain_text_content=body
        )
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logging.info(f"SendGrid email sent, status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Failed to send SendGrid email: {e}")
        sentry_sdk.capture_exception(e)
