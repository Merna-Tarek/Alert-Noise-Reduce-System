# src/filter_alerts.py
import pandas as pd
import json

logs_df = pd.read_csv("data/logs_clustered.csv")
with open("data/noise_suppression_rules.json") as f:
    rules = json.load(f)

noisy_clusters = [r["cluster_id"] for r in rules]
filtered_df = logs_df[~logs_df["cluster_id"].isin(noisy_clusters)]
filtered_df.to_csv("data/cleaned_logs.csv", index=False)
print(f"Cleaned alerts saved to data/cleaned_logs.csv ({len(filtered_df)} rows)")
