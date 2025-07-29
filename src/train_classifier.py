# src/train_classifier.py

import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load logs with cluster labels
logs_df = pd.read_csv("data/logs_clustered.csv")

# Load suppression rules (list of dicts)
with open("data/noise_suppression_rules.json") as f:
    suppression_rules = json.load(f)

# Extract noisy cluster IDs
noisy_clusters = {rule["cluster_id"] for rule in suppression_rules}

# Label data: 1 = noisy, 0 = not noisy
logs_df["label"] = logs_df["cluster_id"].apply(lambda cid: 1 if cid in noisy_clusters else 0)

# Vectorize the alert descriptions
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(logs_df["description"])
y = logs_df["label"]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the classifier
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print("\nClassification Report:\n----------------------------")
print(classification_report(y_test, y_pred))

# Save model and vectorizer
joblib.dump(model, "models/noise_classifier.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("\nClassifier and vectorizer saved to models/")
