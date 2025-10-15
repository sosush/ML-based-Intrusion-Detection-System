import numpy as np

def vulnerability_score_from_confidence(probs, cluster_labels=None):
    attack_prob = probs[:, 1:].sum(axis=1) if probs.shape[1] > 1 else probs.flatten()
    base_score = attack_prob
    if cluster_labels is not None:
        outlier_boost = np.where(cluster_labels == -1, 0.15, 0.0)
        return np.clip(base_score + outlier_boost, 0.0, 1.0)
    return base_score
