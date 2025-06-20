
# ui_components.py
import streamlit as st
import numpy as np
import pandas as pd

from config import CATEGORY_DICT, RETURN_POLICY_DICT


def display_prediction_result(prediction, confidence):
    st.subheader("🔍 Prediction Result")
    if prediction == 1:
        st.success(f"✅ Recommended to Buy (Confidence: {confidence:.2%})")
    else:
        st.error(f"❌ Not Recommended to Buy (Confidence: {(1 - confidence):.2%})")


def display_input_details(input_df):
    display_df = input_df.drop(columns=["username"])
    display_df.rename(columns={
        "category": "Category",
        "price_npr": "Price (NPR)",
        "rating": "Rating",
        "review_count": "Review Count",
        "brand_reputation": "Brand Reputation",
        "discount_percent": "Discount (%)",
        "availability": "Availability",
        "warranty_months": "Warranty (months)",
        "return_policy": "Return Policy",
        "log_price": "Log Price"
    }, inplace=True)
    st.markdown("### 📋 Input Details")
    st.dataframe(display_df.T, use_container_width=True)


def show_input_form(sample_data):
    if "prediction_made" not in st.session_state:
        st.session_state.prediction_made = False
    if "show_faq" not in st.session_state:
        st.session_state.show_faq = False

    with st.sidebar:
        st.header("👤 Enter Your Name")
        username = st.text_input(
            "Your Name",
            max_chars=30,
            value=st.session_state.get('username', ''),
            help="Enter your name for tracking predictions",
        )

        st.header("📥 Input Product Information")

        category_display = st.selectbox(
            "Product Category",
            list(CATEGORY_DICT.values()),
            index=list(CATEGORY_DICT.values()).index(
                st.session_state.get('category_display', list(CATEGORY_DICT.values())[0])),
            help="Choose the product category"
        )
        category = [k for k, v in CATEGORY_DICT.items() if v == category_display][0]

        price_npr = st.number_input(
            "Price in NPR",
            min_value=0,
            step=100,
            value=st.session_state.get('price_npr', 0),
            help="Enter the product price in NPR currency"
        )

        rating = st.slider(
            "Product Rating",
            0.0, 5.0, step=0.1,
            value=st.session_state.get('rating', 0.0),
            help="Rate the product out of 5"
        )

        review_count = st.number_input(
            "Number of Reviews",
            min_value=0,
            step=1,
            value=st.session_state.get('review_count', 0),
            help="Total number of user reviews for the product"
        )

        brand_reputation = st.selectbox(
            "Brand Reputation",
            sorted(sample_data["brand_reputation"].unique()),
            index=sorted(sample_data["brand_reputation"].unique()).index(
                st.session_state.get('brand_reputation', sorted(sample_data["brand_reputation"].unique())[0])),
            help="Select brand reputation category"
        )

        discount_percent = st.slider(
            "Discount (%)",
            0, 100,
            value=st.session_state.get('discount_percent', 0),
            help="Mention current discount on the product"
        )

        availability = st.selectbox(
            "Availability",
            sorted(sample_data["availability"].unique()),
            index=sorted(sample_data["availability"].unique()).index(
                st.session_state.get('availability', sorted(sample_data["availability"].unique())[0])),
            help="Product availability status"
        )

        warranty_months = st.number_input(
            "Warranty (months)",
            min_value=0,
            step=1,
            value=st.session_state.get('warranty_months', 0),
            help="Enter the warranty period in months"
        )

        return_policy_display = st.selectbox(
            "Return Policy",
            list(RETURN_POLICY_DICT.values()),
            index=list(RETURN_POLICY_DICT.values()).index(
                st.session_state.get('return_policy_display', list(RETURN_POLICY_DICT.values())[0])),
            help="Choose the type of return policy"
        )
        return_policy = [k for k, v in RETURN_POLICY_DICT.items() if v == return_policy_display][0]

        submitted = st.button("Predict", help="Click to predict whether this product is worth buying")

        if submitted:
            st.session_state.update({
                'username': username,
                'category_display': category_display,
                'price_npr': price_npr,
                'rating': rating,
                'review_count': review_count,
                'brand_reputation': brand_reputation,
                'discount_percent': discount_percent,
                'availability': availability,
                'warranty_months': warranty_months,
                'return_policy_display': return_policy_display,
                'prediction_made': True
            })
            return {
                "username": username,
                "category": category,
                "price_npr": price_npr,
                "rating": rating,
                "review_count": review_count,
                "brand_reputation": brand_reputation,
                "discount_percent": discount_percent,
                "availability": availability,
                "warranty_months": warranty_months,
                "return_policy": return_policy,
                "log_price": np.log1p(price_npr)
            }

    if not st.session_state.prediction_made:
        st.markdown("### 📝 Display User Guide & FAQs")

        # Initialize toggle state if not present
        if "show_faq" not in st.session_state:
            st.session_state.show_faq = False

        # A button acts as the toggle trigger
        if st.button("Display User Guide and FAQs"):
            # Flip the boolean value on each button click
            st.session_state.show_faq = not st.session_state.show_faq

        if st.session_state.show_faq:
            st.info(
                """
                **How Does This Application Work?**

                🔹 **Input Product Details:**  
                Provide accurate information such as category, price, rating, discount, brand reputation, 
                availability, warranty, and return policy using the form on the left sidebar.

                🔸 **Machine Learning Prediction:**  
                The application uses a trained machine learning model to analyze the inputs and recommend 
                whether the product is worth buying based on historical data.

                🔹 **Confidence Score:**  
                Alongside the recommendation, a confidence score is displayed, indicating the reliability of the prediction.

                🔸 **Interpretation of Results:**  
                ▸ **Recommended to Buy:** Product meets key criteria for a worthwhile purchase.  
                ▸ **Not Recommended to Buy:** Product may have potential drawbacks or insufficient value.

                🔹 **Usage Tips:**  
                ▹ Ensure inputs are accurate for reliable predictions.  
                ▹ Use the confidence score to assess certainty.  
                ▹ Reconsider inputs if results seem unclear or unexpected.

                🔐 **Admin-Only Access:**  
                  Only Admin can access and manage the prediction history, delete records, and 
                  view detailed analytics with graphs and ML tools .

                 If you have any questions or need support, please reach out via the contact details provided.

                """
            )

    return None
