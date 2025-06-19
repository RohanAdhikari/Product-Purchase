import streamlit as st
import pandas as pd
import plotly.express as px
from config import MLFLOW_UI_URL, SENTRY_DASHBOARD_URL, PROMETHEUS_METRICS_URL
from database import get_predictions, delete_predictions

# ✅ Import ETL pipeline trigger
from etl.run_pipeline import run_etl_pipeline


def admin_login():
    st.header("🔐 Admin Login to View Prediction History")
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    username_input = st.text_input("Admin Username", help="Enter admin username to access history")
    password_input = st.text_input("Admin Password", type="password", help="Enter admin password")
    if st.button("Login", help="Click to login as admin"):
        if username_input == "kirito" and password_input == "otirik":
            st.session_state.admin_logged_in = True
            st.success("✅ Admin logged in successfully!")
        else:
            st.error("❌ Invalid admin credentials")


def admin_logout_button():
    st.header("🔒 Admin Logout")
    if st.button("Logout Admin", help="Click to log out of admin view"):
        st.session_state.admin_logged_in = False
        st.session_state.view_history = False
        try:
            st.experimental_rerun()
        except AttributeError:
            st.stop()


def show_admin_tools():
    st.header("🛠️ Admin Tools")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Open MLflow UI", help="Monitor ML model runs"):
            st.markdown(f"[Open MLflow UI]({MLFLOW_UI_URL})", unsafe_allow_html=True)

    with col2:
        if st.button("Open Sentry Dashboard", help="Track errors and exceptions"):
            st.markdown(f"[Open Sentry Dashboard]({SENTRY_DASHBOARD_URL})", unsafe_allow_html=True)

    with col3:
        if st.button("Open Metrics Server", help="View performance metrics"):
            st.markdown(f"[Open Metrics Server]({PROMETHEUS_METRICS_URL})", unsafe_allow_html=True)

    st.markdown("---")

    # ✅ ETL Trigger Section
    st.subheader("🧼 Run ETL Data Pipeline")
    st.markdown("Process raw data from prediction & feedback logs into clean datasets.")

    if st.button("🚀 Run ETL Pipeline Now"):
        try:
            run_etl_pipeline()
            st.success("✅ ETL pipeline executed successfully! Cleaned files saved.")
        except Exception as e:
            st.error(f"❌ Failed to run ETL pipeline: {e}")


def show_total_predictions(conn):
    df = get_predictions(conn)
    st.markdown(f"### Total Predictions Made: **{len(df)}**")


def show_prediction_insights(df_history):
    df_history["timestamp"] = pd.to_datetime(df_history["timestamp"])

    st.subheader("📦 Predictions by Category")
    category_counts = df_history["category"].value_counts()
    fig_bar = px.bar(
        x=category_counts.index,
        y=category_counts.values,
        labels={"x": "Category", "y": "Number of Predictions"},
        color=category_counts.index,
        title="Predictions Count by Category",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("🧭 Buy vs Not Buy Distribution")
    pie_df = df_history["prediction"].map({1: "Buy", 0: "Don't Buy"}).value_counts()
    fig_pie = px.pie(
        names=pie_df.index,
        values=pie_df.values,
        title="Prediction Outcome Distribution",
        color_discrete_sequence=px.colors.sequential.Plasma_r
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("📅 Predictions Over Time")
    daily_counts = df_history.set_index("timestamp").resample("D").size()
    fig_line = px.line(
        x=daily_counts.index,
        y=daily_counts.values,
        labels={"x": "Date", "y": "Number of Predictions"},
        title="Daily Prediction Counts",
        markers=True
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.subheader("📌 Average Confidence by Category")
    confidence_by_cat = df_history.groupby("category")["confidence"].mean()
    fig_conf = px.bar(
        x=confidence_by_cat.index,
        y=confidence_by_cat.values,
        labels={"x": "Category", "y": "Average Confidence"},
        title="Average Prediction Confidence per Category",
        color=confidence_by_cat.index,
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(fig_conf, use_container_width=True)


def show_prediction_history(conn):
    if "view_history" not in st.session_state:
        st.session_state.view_history = False

    # Show login only if not logged in
    if not st.session_state.admin_logged_in:
        admin_login()
        return

    # Admin is logged in, show the history UI
    st.header("📊 Prediction History")
    df_history = get_predictions(conn)

    show_total_predictions(conn)

    if df_history.empty:
        st.info("No predictions found.")
        return

    st.markdown("✅ **Select rows to delete** and click the button below.")
    selected_rows = st.data_editor(
        df_history,
        use_container_width=True,
        num_rows="dynamic",
        disabled=["id"],
        key="editable_history",
        hide_index=True
    )
    to_delete = df_history.loc[~df_history.index.isin(selected_rows.index)]

    if not to_delete.empty:
        if st.button("🗑️ Delete Selected", help="Delete selected prediction records from database"):
            try:
                ids_to_delete = tuple(to_delete["id"].tolist())
                delete_predictions(conn, ids_to_delete)
                st.success("Selected rows deleted successfully.")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to delete rows: {e}")

    if "show_graphs" not in st.session_state:
        st.session_state.show_graphs = False

    def toggle_graphs():
        st.session_state.show_graphs = not st.session_state.show_graphs

    st.markdown("### 📊 Prediction Insights")
    st.button("Toggle Prediction Graphs", on_click=toggle_graphs, help="Show or hide visual insights from prediction data")

    if st.session_state.show_graphs:
        show_prediction_insights(df_history)

    # ✅ Admin Tools and ETL shown only when logged in
    show_admin_tools()
    admin_logout_button()


# New wrapper function to be imported in main.py
def show_admin_page(conn):
    """
    This function controls the entire admin section UI including login,
    prediction history, insights, admin tools, and logout.
    Call this from your main.py with DB connection.
    """
    if "view_history" not in st.session_state:
        st.session_state.view_history = False



    if st.session_state.view_history:
        show_prediction_history(conn)
