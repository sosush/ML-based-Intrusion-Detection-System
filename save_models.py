import os
import joblib
import numpy as np
from classification import train_random_forest, train_xgboost
import pandas as pd

MODELS_DIR = "models"
os.makedirs(MODELS_DIR, exist_ok=True)

# Load preprocessed dataset
df = pd.read_csv("data/processed.csv")  # your merged CSV
X = df.drop(columns=["label"]).values
y = df["label"].values

# Optional: split data (here just using all data for fast saving)
X_train, y_train = X, y

# Train Random Forest
print("Training Random Forest...")
rf_model = train_random_forest(X_train, y_train)
joblib.dump(rf_model, os.path.join(MODELS_DIR, "rf_model.joblib"))
print("✅ rf_model saved")

# Train XGBoost
print("Training XGBoost...")
xgb_model = train_xgboost(X_train, y_train)
joblib.dump(xgb_model, os.path.join(MODELS_DIR, "xgb_model.joblib"))
print("✅ xgb_model saved")

# Optional: if you have a scaler, create and save it
# from sklearn.preprocessing import StandardScaler
# scaler = StandardScaler().fit(X_train)
# joblib.dump(scaler, os.path.join(MODELS_DIR, "scaler.joblib"))
# print("✅ scaler saved")
