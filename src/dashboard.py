import streamlit as st
import pandas as pd
import joblib
import os

# Load model and vectorizer once
MODEL_PATH = "models/noise_classifier.pkl"
VECTORIZER_PATH = "models/vectorizer.pkl"
DEFAULT_LOG_PATH = "data/generated_siem_logs.csv"

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH), joblib.load(VECTORIZER_PATH)

@st.cache_data
def load_logs(file_path):
    try:
        df = pd.read_csv(file_path)
        if "alert" not in df.columns:
            st.warning("CSV file must contain a column named 'alert'")
            return pd.DataFrame()
        return df
    except Exception as e:
        st.error(f"Failed to load file: {e}")
        return pd.DataFrame()

def predict_alerts(df, model, vectorizer):
    X = vectorizer.transform(df["alert"])
    predictions = model.predict(X)
    df["prediction"] = predictions
    df["label"] = df["prediction"].apply(lambda x: "NOISY ALERT" if x == 1 else "VALID ALERT")
    return df

# Load model and data
model, vectorizer = load_model()
df_logs = load_logs(DEFAULT_LOG_PATH)
if not df_logs.empty:
    df_logs = predict_alerts(df_logs, model, vectorizer)

# GUI layout
st.set_page_config(page_title="Alert Noise Dashboard", layout="wide")
st.title("🔍 Alert Noise Classifier Dashboard")

tabs = st.tabs(["📊 Dashboard", "📁 Upload New Alerts", "🧠 Classify Single Alert", "📤 Export Results"])

# --- Dashboard ---
with tabs[0]:
    st.subheader("Dataset Overview")
    if df_logs.empty:
        st.info("No alerts loaded.")
    else:
        st.success(f"{len(df_logs)} alerts loaded from `{DEFAULT_LOG_PATH}`.")
        st.metric("🟢 Valid Alerts", df_logs["label"].value_counts().get("VALID ALERT", 0))
        st.metric("🔴 Noisy Alerts", df_logs["label"].value_counts().get("NOISY ALERT", 0))
        st.dataframe(df_logs.head(20))

# --- Upload New Alerts ---
with tabs[1]:
    uploaded_file = st.file_uploader("Upload CSV file with alert column", type=["csv"])
    if uploaded_file:
        new_df = pd.read_csv(uploaded_file)
        if "alert" in new_df.columns:
            new_df = predict_alerts(new_df, model, vectorizer)
            st.dataframe(new_df)
            st.download_button("Download with Predictions", new_df.to_csv(index=False), file_name="predicted_alerts.csv")
        else:
            st.error("Uploaded CSV must contain 'alert' column.")

# --- Classify Single Alert ---
with tabs[2]:
    st.subheader("Single Alert Classification")
    user_input = st.text_area("Enter alert text here:")
    if st.button("Classify"):
        if user_input.strip():
            result = predict_alerts(pd.DataFrame({"alert": [user_input]}), model, vectorizer)
            st.info(f"Prediction: {result['label'].iloc[0]}")
        else:
            st.warning("Please enter alert text.")

# --- Export Tab ---
with tabs[3]:
    if not df_logs.empty:
        col1, col2 = st.columns(2)
        with col1:
            valid_df = df_logs[df_logs["label"] == "VALID ALERT"]
            st.download_button("⬇ Download VALID Alerts", valid_df.to_csv(index=False), "valid_alerts.csv")

        with col2:
            noisy_df = df_logs[df_logs["label"] == "NOISY ALERT"]
            st.download_button("⬇ Download NOISY Alerts", noisy_df.to_csv(index=False), "noisy_alerts.csv")
    else:
        st.info("Load alerts to export results.")
