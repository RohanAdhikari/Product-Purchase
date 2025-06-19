import streamlit as st
import pandas as pd
from pathlib import Path
import time

FEEDBACK_FILE = Path(__file__).parent.parent / "datasets" / "feedback.csv"
MAX_FEEDBACK_PER_USER = 2


def load_feedback():
    if FEEDBACK_FILE.exists():
        return pd.read_csv(FEEDBACK_FILE)
    else:
        return pd.DataFrame(columns=["username", "rating", "comments", "timestamp"])


def save_feedback(username, rating, comments):
    df = load_feedback()
    new_entry = pd.DataFrame([{
        "username": username or "Anonymous",
        "rating": rating,
        "comments": comments.strip(),
        "timestamp": pd.Timestamp.now()
    }])
    FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(FEEDBACK_FILE, index=False)


def ask_feedback():
    """Ask user if they'd like to give feedback – only once after prediction."""

    # Show only if prediction is made and feedback not handled
    if not st.session_state.get("prediction_made", False):
        return

    if st.session_state.get("feedback_handled", False):
        return

    st.markdown("---")
    st.subheader("💭 We'd love to hear from you!")
    st.markdown("Would you like to provide feedback on your experience?")

    choice = st.radio(
        "Your response:",
        ["Yes", "No"],
        index=None,
        horizontal=True,
        key="feedback_choice"
    )

    if choice == "Yes":
        st.session_state.give_feedback = True
    elif choice == "No":
        st.session_state.give_feedback = False
        st.info("Thank you for your time! 🤝")
        st.session_state.feedback_handled = True
        time.sleep(1)
        st.rerun()


def show_feedback_form():
    if not st.session_state.get("prediction_made", False):
        return

    if st.session_state.get("feedback_handled", False):
        return

    # If user said "No", nothing more to do
    if st.session_state.get("give_feedback") is False:
        return

    # If user said "Yes", show form step-by-step
    if st.session_state.get("give_feedback") is True and not st.session_state.get("feedback_previewed"):
        with st.form("feedback_form"):
            st.markdown("### 📝 Feedback Form")
            username = st.text_input("👤 Your Name", value=st.session_state.get("username", ""), key="feedback_username")
            rating = st.slider("⭐ Rate your experience", 1, 5, value=4)
            comments = st.text_area("💬 Comments (optional)", max_chars=300)

            preview = st.form_submit_button("👀 Preview Before Submit")

            if preview:
                user = username.strip() or "Anonymous"
                st.session_state.feedback_data = {
                    "username": user,
                    "rating": rating,
                    "comments": comments.strip()
                }
                st.session_state.feedback_previewed = True
                st.rerun()
        return

    # Preview step before confirmation
    if st.session_state.get("feedback_previewed", False):
        st.markdown("### 📋 Please Confirm Your Feedback")
        data = st.session_state.get("feedback_data", {})
        st.markdown(f"- 👤 **Name:** `{data.get('username')}`")
        st.markdown(f"- ⭐ **Rating:** `{data.get('rating')}/5`")
        if data.get("comments"):
            st.markdown(f"- 💬 **Comments:**\n\n> {data.get('comments')}")

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("✅ Submit Now"):
                save_feedback(data["username"], data["rating"], data["comments"])
                st.success("🎉 Feedback submitted. Thank you!")
                st.session_state.feedback_handled = True
                time.sleep(1)
                st.rerun()
        with col2:
            if st.button("✏️ Edit"):
                st.session_state.feedback_previewed = False
                st.rerun()
