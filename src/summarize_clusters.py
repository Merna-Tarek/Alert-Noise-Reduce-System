import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load clustered logs
logs_df = pd.read_csv("data/logs_clustered.csv")

# Group descriptions by cluster
cluster_texts = logs_df.groupby("cluster_id")["description"].apply(lambda texts: " ".join(texts))

# Use TF-IDF to extract key terms per cluster
vectorizer = TfidfVectorizer(stop_words="english", max_features=10)
tfidf_matrix = vectorizer.fit_transform(cluster_texts)

feature_names = vectorizer.get_feature_names_out()

print("\nTop Terms per Cluster:")
print("-" * 40)

for cluster_idx, row in enumerate(tfidf_matrix.toarray()):
    top_indices = row.argsort()[::-1][:5]
    top_terms = [feature_names[i] for i in top_indices]
    print(f"Cluster {cluster_idx}: {', '.join(top_terms)}")
