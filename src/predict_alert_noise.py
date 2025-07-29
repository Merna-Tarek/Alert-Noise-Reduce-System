import argparse
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the saved model and vectorizer
model = joblib.load("models/noise_classifier.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

def classify_alert(alert_text):
    # Transform alert into TF-IDF vector
    X_input = vectorizer.transform([alert_text])
    # Predict using the trained model
    prediction = model.predict(X_input)[0]
    label = "NOISY ALERT (Suppress)" if prediction == 1 else "VALID ALERT (Investigate)"
    return label

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify alert as noisy or valid")
    parser.add_argument("--alert", type=str, required=True, help="Alert text to classify")
    args = parser.parse_args()

    result = classify_alert(args.alert)
    print(f"\nPrediction: {result}")
