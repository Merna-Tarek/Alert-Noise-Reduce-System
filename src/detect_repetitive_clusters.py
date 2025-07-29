# src/detect_repetitive_clusters.py
import pandas as pd
import json

# Load clustered logs
logs_df = pd.read_csv("data/logs_clustered.csv")

# Count alerts per cluster
cluster_counts = logs_df["cluster_id"].value_counts()

# Threshold: clusters with too many alerts are considered noisy
NOISE_THRESHOLD = 50

# Collect noisy clusters
noisy_clusters = cluster_counts[cluster_counts > NOISE_THRESHOLD]

# Print results
print("Noisy Clusters Detected:\n------------------------------")
rules = []
for cluster_id, count in noisy_clusters.items():
    print(f"Cluster {cluster_id} → {count} alerts → Candidate for noise suppression")
    rules.append({
        "cluster_id": int(cluster_id),
        "action": "suppress",
        "reason": f"{count} repetitive alerts"
    })

# Save suppression rules
output_path = "data/noise_suppression_rules.json"
with open(output_path, "w") as f:
    json.dump(rules, f, indent=2)

print(f"\nSuppression rules saved to {output_path}")
