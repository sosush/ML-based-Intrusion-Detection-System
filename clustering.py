import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from tensorflow.keras import layers, models


def run_kmeans(X, n_clusters=6, sample_size=10000):
    """Run KMeans clustering with optional sampling for silhouette score."""
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)

    # Sample for silhouette to avoid O(n^2) explosion
    if len(set(labels)) > 1:
        if sample_size and len(X) > sample_size:
            idx = np.random.choice(len(X), sample_size, replace=False)
            score = silhouette_score(X[idx], labels[idx])
        else:
            score = silhouette_score(X, labels)
    else:
        score = -1

    return {"labels": labels, "silhouette": score}


def run_dbscan(X, eps=0.5, min_samples=5, sample_size=10000):
    """Run DBSCAN clustering with optional sampling for silhouette score."""
    dbscan = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=-1)
    labels = dbscan.fit_predict(X)

    if len(set(labels)) > 1:
        if sample_size and len(X) > sample_size:
            idx = np.random.choice(len(X), sample_size, replace=False)
            score = silhouette_score(X[idx], labels[idx])
        else:
            score = silhouette_score(X, labels)
    else:
        score = -1

    return {"labels": labels, "silhouette": score}


def build_autoencoder(input_dim, encoding_dim=8):
    """Build a simple feed-forward autoencoder for dimensionality reduction."""
    inp = layers.Input(shape=(input_dim,))
    x = layers.Dense(max(encoding_dim * 4, 32), activation="relu")(inp)
    x = layers.Dense(max(encoding_dim * 2, 16), activation="relu")(x)
    encoded = layers.Dense(encoding_dim, activation="relu", name="encoded")(x)

    x = layers.Dense(max(encoding_dim * 2, 16), activation="relu")(encoded)
    x = layers.Dense(max(encoding_dim * 4, 32), activation="relu")(x)
    decoded = layers.Dense(input_dim, activation="linear")(x)

    ae = models.Model(inp, decoded)
    encoder = models.Model(inp, encoded)
    ae.compile(optimizer="adam", loss="mse")
    return ae, encoder


def run_autoencoder_clustering(X, encoding_dim=8, n_clusters=8, epochs=10, batch_size=32, verbose=0):
    """Train an autoencoder, extract embeddings, and cluster them with KMeans."""
    ae, encoder = build_autoencoder(X.shape[1], encoding_dim)
    ae.fit(X, X, epochs=epochs, batch_size=batch_size, verbose=verbose)
    embeddings = encoder.predict(X)

    kres = run_kmeans(embeddings, n_clusters=n_clusters)
    return {"ae": ae, "encoder": encoder, "embeddings": embeddings, **kres}
