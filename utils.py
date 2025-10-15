import os
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

RANDOM_SEED = 42

def ensure_dir(d):
    os.makedirs(d, exist_ok=True)

def save_json(obj, path):
    ensure_dir(os.path.dirname(path) or ".")
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)

def load_csv(path):
    return pd.read_csv(path)

def save_csv(df, path):
    ensure_dir(os.path.dirname(path) or ".")
    df.to_csv(path, index=False)

def train_val_test_split(df, target_col="label", test_size=0.2, val_size=0.1):
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=RANDOM_SEED, stratify=df[target_col])
    train_df, val_df = train_test_split(train_df, test_size=val_size/(1-test_size), random_state=RANDOM_SEED, stratify=train_df[target_col])
    return train_df.reset_index(drop=True), val_df.reset_index(drop=True), test_df.reset_index(drop=True)

def standardize_features(df, feature_cols):
    scaler = StandardScaler()
    df[feature_cols] = df[feature_cols].clip(upper=1e6)

    # Replace inf/-inf with NaN
    df[feature_cols] = df[feature_cols].replace([np.inf, -np.inf], np.nan)
    
    # Fill NaNs with median
    medians = df[feature_cols].median()
    df[feature_cols] = df[feature_cols].fillna(medians)
    
    # Fit and transform
    X = scaler.fit_transform(df[feature_cols].values)
    
    return X, scaler, medians


def apply_scaler(df, feature_cols, scaler, train_medians=None):
    # Replace inf/-inf with NaN
    df[feature_cols] = df[feature_cols].replace([np.inf, -np.inf], np.nan)
    
    # Fill NaNs with median
    if train_medians is not None:
        # Use training set median for consistency
        df[feature_cols] = df[feature_cols].fillna(train_medians)
    else:
        # Use the current df median (less ideal)
        df[feature_cols] = df[feature_cols].fillna(df[feature_cols].median())
    
    # Transform using the scaler
    return scaler.transform(df[feature_cols].values)

