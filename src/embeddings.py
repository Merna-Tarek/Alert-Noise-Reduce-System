# embeddings.py

import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import os


def embed_alert_descriptions(csv_path='data/generated_siem_logs.csv',
                            model_name='all-MiniLM-L6-v2',
                            output_embeddings='data/alert_embeddings.npy',
                            output_df='data/logs_with_embeddings.csv'):
    # Load the CSV with alert descriptions
    df = pd.read_csv(csv_path)
    if 'alert_description' not in df.columns:
        raise ValueError("CSV file must contain an 'alert_description' column.")

    print(f" Loaded {len(df)} alerts from {csv_path}")

    # Load the sentence transformer model
    print(f" Loading embedding model: {model_name}")
    model = SentenceTransformer(model_name)

    # Compute sentence embeddings
    print("Generating embeddings...")
    embeddings = model.encode(df['alert_description'].tolist(), show_progress_bar=True)

    # Save embeddings as .npy
    os.makedirs(os.path.dirname(output_embeddings), exist_ok=True)
    np.save(output_embeddings, embeddings)
    print(f"Saved embeddings to {output_embeddings}")

    # (Optional) Save DataFrame with embedding index
    df['embedding_index'] = range(len(df))
    df.to_csv(output_df, index=False)
    print(f" Saved logs with index to {output_df}")

    return df, embeddings


if __name__ == "__main__":
    embed_alert_descriptions()
