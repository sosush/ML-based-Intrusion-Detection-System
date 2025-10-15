import os
import numpy as np
import pandas as pd
from utils import save_csv, ensure_dir
from data_prep import basic_preprocess
from run_pipeline import run

def create_synthetic_dataset(path="data/raw.csv", n_samples=500, n_features=12, attack_ratio=0.3, seed=42):
    np.random.seed(seed)
    n_attack = int(n_samples * attack_ratio)
    n_benign = n_samples - n_attack
    ben = np.random.normal(loc=0.0, scale=1.0, size=(n_benign, n_features))
    att = np.random.normal(loc=2.0, scale=1.5, size=(n_attack, n_features))
    X = np.vstack([ben, att])
    labels = ["BENIGN"] * n_benign + ["ATTACK"] * n_attack
    cols = [f"f{i}" for i in range(n_features)]
    df = pd.DataFrame(X, columns=cols)
    df["label"] = labels
    ensure_dir(os.path.dirname(path) or ".")
    df.to_csv(path, index=False)
    return path

def test_end_to_end(tmp_path):
    data_dir = os.path.join(tmp_path, "data")
    os.makedirs(data_dir, exist_ok=True)
    raw_csv = os.path.join(data_dir, "raw.csv")
    create_synthetic_dataset(path=raw_csv, n_samples=300, n_features=10, attack_ratio=0.3)
    processed_csv, meta = basic_preprocess(input_csv=raw_csv, output_csv=os.path.join(data_dir, "processed.csv"), label_col="label")
    res = run(input_csv=processed_csv, label_col="label", feature_cols=meta["feature_cols"], outdir=str(tmp_path / "output"))
    assert "clustering" in res
    assert "classification" in res
    assert res["vulnerability"]["mean_score"] >= 0.0 and res["vulnerability"]["mean_score"] <= 1.0
