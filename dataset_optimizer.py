# ids_project/dataset_optimizer.py

import pandas as pd
import numpy as np
from sklearn.feature_selection import VarianceThreshold

def optimize_dataset(input_csv="data/processed.csv", output_csv="data/optimized.csv",
                     benign_ratio=2, variance_threshold=0.0, corr_threshold=0.95,
                     binary_labels=True):
    """
    Optimize IDS dataset for efficiency and training usability.
    - Downsamples benign traffic (class balancing)
    - Optionally collapses to binary labels (BENIGN vs ATTACK)
    - Drops low-variance & highly correlated features
    """

    print(f"📥 Loading dataset from {input_csv} ...")
    df = pd.read_csv(input_csv)
    print("Original shape:", df.shape)

    # ✅ Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    # ✅ Collapse labels (binary)
    if binary_labels:
        df['label'] = df['label'].apply(lambda x: 0 if str(x).lower() == "benign" or str(x) == "0" else 1)

    # ✅ Downsample benign while keeping all attacks
    benign = df[df['label'] == 0]
    attack = df[df['label'] == 1]

    benign_sample = benign.sample(n=min(len(attack)*benign_ratio, len(benign)), random_state=42)
    df_balanced = pd.concat([benign_sample, attack])
    print("Balanced shape:", df_balanced.shape)

    # ✅ Drop low-variance features
    if variance_threshold > 0:
        selector = VarianceThreshold(threshold=variance_threshold)
        numeric_cols = df_balanced.select_dtypes(include=[np.number]).columns.tolist()
        X = df_balanced[numeric_cols]
        selector.fit(X)
        kept = [c for c, keep in zip(numeric_cols, selector.get_support()) if keep]
        df_balanced = df_balanced[kept + ['label']]
        print("After variance filter:", df_balanced.shape)

    # ✅ Drop highly correlated features
    if corr_threshold < 1.0:
        corr = df_balanced.corr(numeric_only=True).abs()
        upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
        to_drop = [column for column in upper.columns if any(upper[column] > corr_threshold)]
        df_balanced = df_balanced.drop(columns=to_drop)
        print("After correlation pruning:", df_balanced.shape)

    # ✅ Shuffle
    df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

    # ✅ Save optimized dataset
    df_balanced.to_csv(output_csv, index=False)
    print(f"✅ Optimized dataset saved to {output_csv} with shape {df_balanced.shape}")

if __name__ == "__main__":
    optimize_dataset()
