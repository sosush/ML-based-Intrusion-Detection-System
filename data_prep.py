import pandas as pd
import numpy as np
from utils import save_csv, load_csv, standardize_features
from sklearn.preprocessing import LabelEncoder

DEFAULT_FEATURES = None  # None means infer from CSV (all numeric except label)

def basic_preprocess(input_csv="data/raw.csv", output_csv="data/processed.csv", label_col="label"):
    df = load_csv(input_csv)

    # 🔑 Normalize column names: strip spaces
    df.columns = [c.strip().lower() for c in df.columns]

    # Drop columns with too many missing values and fill remaining
    df = df.dropna(axis=1, thresh=int(len(df)*0.5))
    df = df.fillna(0)

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.fillna(0)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    numeric_cols = [c for c in numeric_cols if c != label_col]
    df[numeric_cols] = df[numeric_cols].clip(lower=-1e10, upper=1e10)

    # Ensure label exists
    if label_col not in df.columns:
        raise ValueError(f"label column '{label_col}' not found. Available columns: {df.columns.tolist()}")

    # Label encode
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    df[label_col] = le.fit_transform(df[label_col].astype(str))

    # Choose numeric features
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols = [c for c in numeric_cols if c != label_col]

    # Store metadata
    meta = {"label_encoder_classes": le.classes_.tolist(), "feature_cols": numeric_cols}
    save_csv(df[[*numeric_cols, label_col]], output_csv)
    return output_csv, meta
