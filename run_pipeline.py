import numpy as np
import json
from sklearn.decomposition import PCA
from utils import load_csv, train_val_test_split, standardize_features, save_json
from clustering import run_kmeans, run_dbscan, run_autoencoder_clustering
from classification import train_random_forest, train_xgboost, build_dnn, evaluate_model
from predictor import vulnerability_score_from_confidence


def run(
    input_csv="data/optimized.csv",
    label_col="label",
    feature_cols=None,
    outdir="output",
    sample_size=50000,
    pca_components=20,
    max_dbscan=20000
):
    # -------------------------
    # Load data
    # -------------------------
    df = load_csv(input_csv)

    if feature_cols is None:
        feature_cols = [c.strip().lower() for c in df.columns if c != label_col]

    # -------------------------
    # Split sets
    # -------------------------
    train_df, val_df, test_df = train_val_test_split(
        df, target_col=label_col, test_size=0.2, val_size=0.1
    )

    # -------------------------
    # Standardize
    # -------------------------
    X_train, scaler, train_medians = standardize_features(train_df, feature_cols)
    X_val = scaler.transform(val_df[feature_cols].values)
    X_test = scaler.transform(test_df[feature_cols].values)

    y_train = train_df[label_col].values
    y_val = val_df[label_col].values
    y_test = test_df[label_col].values

    # -------------------------
    # Downsample train for clustering
    # -------------------------
    if len(X_train) > sample_size:
        idx = np.random.choice(len(X_train), sample_size, replace=False)
        X_train_small = X_train[idx]
        y_train_small = y_train[idx]
    else:
        X_train_small = X_train
        y_train_small = y_train

    # -------------------------
    # Dimensionality Reduction
    # -------------------------
    pca = PCA(n_components=pca_components, random_state=42)
    X_train_small_pca = pca.fit_transform(X_train_small)

    results = {}

    # -------------------------
    # Clustering (on reduced data)
    # -------------------------
    kres = run_kmeans(X_train_small_pca, n_clusters=6)
    dres = run_dbscan(X_train_small_pca, eps=0.8, min_samples=5)
    aeres = run_autoencoder_clustering(
        X_train_small, encoding_dim=8, n_clusters=6, epochs=10, batch_size=32, verbose=0
    )

    results["clustering"] = {
        "kmeans_silhouette": kres["silhouette"],
        "dbscan_silhouette": dres["silhouette"],
        "ae_kmeans_silhouette": aeres["silhouette"],
    }

    # -------------------------
    # Classification
    # -------------------------
    rf = train_random_forest(X_train, y_train, n_estimators=50)
    xgb = train_xgboost(X_train, y_train, n_estimators=50)

    dnn = build_dnn(X_train.shape[1], n_classes=len(set(y_train)))
    dnn.fit(X_train, y_train, epochs=8, batch_size=32, verbose=0)

    results["classification"] = {
        "rf": evaluate_model(rf, X_test, y_test),
        "xgb": evaluate_model(xgb, X_test, y_test),
        "dnn": evaluate_model(dnn, X_test, y_test, is_keras=True),
    }

    # -------------------------
    # Vulnerability Score (safe DBSCAN)
    # -------------------------
    probs = xgb.predict_proba(X_test)

    # Subsample test set for DBSCAN
    if len(X_test) > max_dbscan:
        idx = np.random.choice(len(X_test), max_dbscan, replace=False)
        X_test_small = X_test[idx]
        probs_small = probs[idx]
    else:
        X_test_small = X_test
        probs_small = probs

    X_test_small_pca = pca.transform(X_test_small)
    dres_test = run_dbscan(X_test_small_pca, eps=0.8, min_samples=5)

    vuln_scores = vulnerability_score_from_confidence(
        probs_small, cluster_labels=dres_test["labels"]
    )

    results["vulnerability"] = {
        "mean_score": float(vuln_scores.mean()),
        "top_5": vuln_scores[:5].tolist(),
        "n_samples": len(X_test_small),
    }

    # -------------------------
    # Save + Print
    # -------------------------
    save_json(results, f"{outdir}/results_summary.json")
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    run()
