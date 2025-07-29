import argparse
import pandas as pd
import joblib
import os

# Load vectorizer and trained classifier once
vectorizer = joblib.load("models/vectorizer.pkl")
classifier = joblib.load("models/noise_classifier.pkl")

def predict_alerts(alerts):
    X = vectorizer.transform(alerts)
    predictions = classifier.predict(X)
    return predictions

def predict_from_file(input_path):
    """
    Predicts alert noise from a file and returns the DataFrame.
    Supports .txt or .csv input.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")

    if input_path.endswith(".txt"):
        with open(input_path, "r", encoding="utf-8") as f:
            alerts = [line.strip() for line in f if line.strip()]
        df = pd.DataFrame(alerts, columns=["alert"])
    elif input_path.endswith(".csv"):
        df = pd.read_csv(input_path)
        if "alert" not in df.columns:
            raise ValueError("CSV must contain a column named 'alert'")
    else:
        raise ValueError("Unsupported file type. Use .txt or .csv")

    # Run prediction
    predictions = predict_alerts(df["alert"])
    df["prediction"] = predictions
    df["label"] = df["prediction"].apply(lambda x: "NOISY ALERT" if x == 1 else "VALID ALERT")
    return df

def main():
    parser = argparse.ArgumentParser(description="Batch alert noise prediction CLI")
    parser.add_argument("--input", required=True, help="Path to input file (.txt or .csv)")
    parser.add_argument("--output", default=None, help="Optional path to save output CSV")

    args = parser.parse_args()

    # Predict and display
    df = predict_from_file(args.input)

    print("\nBatch Prediction Results:")
    print(df[["alert", "label"]].to_string(index=False))

    # Save if requested
    if args.output:
        df.to_csv(args.output, index=False)
        print(f"\nResults saved to {args.output}")

if __name__ == "__main__":
    main()
