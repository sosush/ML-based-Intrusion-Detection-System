import glob
import os
import pandas as pd
from data_prep import basic_preprocess

def detect_label_column(df):
    """
    Try to detect the label column automatically.
    Looks for common names: label, attack, class (case-insensitive).
    """
    # normalize column names: strip spaces and lowercase
    df.columns = [c.strip() for c in df.columns]
    candidates = [c for c in df.columns if c.lower() in ["label", "attack", "class"]]

    if not candidates:
        raise ValueError(f"No label column found! Columns = {df.columns.tolist()}")
    if len(candidates) > 1:
        print(f"⚠️ Multiple possible label columns found: {candidates}, using {candidates[0]}")
    return candidates[0]

# Collect all raw CSVs from IDSdata
raw_files = glob.glob("IDSdata/*.csv")
print(f"Found {len(raw_files)} raw CSVs")

processed_files = []

for i, f in enumerate(raw_files, 1):
    print(f"[{i}/{len(raw_files)}] Inspecting {f}")
    # peek header
    df_head = pd.read_csv(f, nrows=5)
    df_head.columns = [c.strip() for c in df_head.columns]  # strip spaces
    label_col = detect_label_column(df_head).lower().strip()

    out = f"data/processed_{i}.csv"
    print(f"    Using label column: '{label_col}' -> {out}")
    processed_csv, meta = basic_preprocess(f, out, label_col=label_col)
    processed_files.append(out)

# Merge all processed outputs
dfs = [pd.read_csv(f) for f in processed_files]
df = pd.concat(dfs, ignore_index=True)

# Strip spaces from all column names in final merged file
df.columns = [c.strip() for c in df.columns]

df.to_csv("data/processed.csv", index=False)
print("✅ Final merged processed.csv shape:", df.shape)
