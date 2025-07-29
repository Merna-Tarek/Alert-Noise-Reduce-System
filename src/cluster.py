import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# -------- Step 1: Load embeddings and original logs --------
embeddings = np.load("data/alert_embeddings.npy")
raw_logs = pd.read_csv("data/logs_with_embeddings.csv")

# -------- Step 2: Run KMeans clustering --------
n_clusters = 6  # You can adjust this number based on your needs
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
clusters = kmeans.fit_predict(embeddings)

# -------- Step 3: Add cluster ID and restore descriptions --------
logs_df = pd.DataFrame(embeddings)
logs_df["cluster_id"] = clusters
logs_df["description"] = raw_logs["alert_description"]

# -------- Step 4: Save clustered logs --------
logs_df.to_csv("data/logs_clustered.csv", index=False)
print("Clustered alerts saved to data/logs_clustered.csv")

# -------- Step 5: Plot cluster distribution --------
cluster_counts = logs_df["cluster_id"].value_counts().sort_index()

plt.figure(figsize=(10, 6))
sns.barplot(x=cluster_counts.index, y=cluster_counts.values, hue=cluster_counts.index, palette="mako", legend=False)
plt.title("Number of Alerts per Cluster", fontsize=14)
plt.xlabel("Cluster ID")
plt.ylabel("Alert Count")
plt.tight_layout()
plt.savefig("data/cluster_distribution.png")
plt.show()

# -------- Step 6: Print sample alerts from each cluster --------
print("\nSample Alerts from Each Cluster:")
print("-" * 40)
for cluster_id in sorted(logs_df['cluster_id'].unique()):
    samples = logs_df[logs_df['cluster_id'] == cluster_id]['description'].head(1).values
    if samples:
        print(f"Cluster {cluster_id}: Sample Alert -> {samples[0]}")
