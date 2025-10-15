import numpy as np
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score
from tensorflow.keras import layers, models

def train_random_forest(X_train, y_train, n_estimators=100, random_state=42):
    clf = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
    clf.fit(X_train, y_train)
    return clf

def train_xgboost(X_train, y_train, n_estimators=100, random_state=42):
    clf = XGBClassifier(n_estimators=n_estimators, use_label_encoder=False, eval_metric="logloss", random_state=random_state)
    clf.fit(X_train, y_train)
    return clf

def build_dnn(input_dim, n_classes, hidden_units=[64,32]):
    inp = layers.Input(shape=(input_dim,))
    x = inp
    for u in hidden_units:
        x = layers.Dense(u, activation="relu")(x)
    out = layers.Dense(n_classes, activation="softmax")(x)
    m = models.Model(inp, out)
    m.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return m

def evaluate_model(clf, X, y, is_keras=False):
    if is_keras:
        y_pred_prob = clf.predict(X)
        y_pred = y_pred_prob.argmax(axis=1)
    else:
        y_pred = clf.predict(X)
    return {"accuracy": float(accuracy_score(y, y_pred)), "report": classification_report(y, y_pred, output_dict=True)}
