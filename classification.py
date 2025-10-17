import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# --------------------------
# Load merged processed dataset
# --------------------------
df = pd.read_csv("data/processed.csv")  # replace with your merged CSV path
label_col = "label"  # change if your label column has another name
X = df.drop(columns=[label_col]).values
y = df[label_col].values

# --------------------------
# Train/test split
# --------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --------------------------
# Scale features
# --------------------------
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Save scaler for later use
joblib.dump(scaler, "models/scaler.joblib")

# --------------------------
# Train Random Forest
# --------------------------
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
joblib.dump(rf_model, "models/rf_model.joblib")

# Evaluate RF
y_pred_rf = rf_model.predict(X_test)
print("Random Forest Accuracy:", accuracy_score(y_test, y_pred_rf))
print(classification_report(y_test, y_pred_rf))

# --------------------------
# Train XGBoost
# --------------------------
xgb_model = XGBClassifier(
    n_estimators=100,
    use_label_encoder=False,
    eval_metric="logloss",
    random_state=42
)
xgb_model.fit(X_train, y_train)
joblib.dump(xgb_model, "models/xgb_model.joblib")

# Evaluate XGB
y_pred_xgb = xgb_model.predict(X_test)
print("XGBoost Accuracy:", accuracy_score(y_test, y_pred_xgb))
print(classification_report(y_test, y_pred_xgb))
