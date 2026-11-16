"""
Model Evaluation and Validation Module for Unsupervised Clustering.
Computes:
1. Within-Cluster Sum of Squares (WCSS / Inertia / Elbow Method).
2. Silhouette Coefficient (Overall mean & per-cluster samples).
3. Davies-Bouldin Index (Cluster separation to scatter ratio).
4. Distance Metric Comparison (Euclidean vs Manhattan).
5. Cluster Stability Analysis across random initializations (ARI & NMI).
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    silhouette_score,
    silhouette_samples,
    davies_bouldin_score,
    adjusted_rand_score,
    normalized_mutual_info_score,
    pairwise_distances
)
from clustering import run_kmeans_clustering, run_manhattan_clustering

def evaluate_kmeans_sweep(X: np.ndarray, k_range: list = [2, 3, 4, 5, 6, 7, 8], random_state: int = 42) -> pd.DataFrame:
    """
    Evaluates K-Means across a spectrum of cluster counts K.
    Calculates WCSS (Inertia), Silhouette Score, and Davies-Bouldin Index for each K.
    """
    results = []

    for k in k_range:
        kmeans = run_kmeans_clustering(X, k=k, random_state=random_state)
        labels = kmeans.labels_

        wcss = kmeans.inertia_
        sil = silhouette_score(X, labels, metric="euclidean")
        db = davies_bouldin_score(X, labels)

        results.append({
            "k": k,
            "wcss": round(wcss, 2),
            "silhouette": round(sil, 4),
            "davies_bouldin": round(db, 4)
        })

    return pd.DataFrame(results)

def compare_distance_metrics(X: np.ndarray, k_values: list = [3, 4, 5], random_state: int = 42) -> pd.DataFrame:
    """
    Compares Euclidean Distance (K-Means) against Manhattan Distance (K-Medians).
    Evaluates:
    - Silhouette Score (computed under Euclidean and Manhattan metrics)
    - Davies-Bouldin Index
    - Cluster size balance / dispersion
    """
    comparison = []

    for k in k_values:
        # 1. Euclidean K-Means
        kmeans = run_kmeans_clustering(X, k=k, random_state=random_state)
        euc_labels = kmeans.labels_
        euc_sil_euc = silhouette_score(X, euc_labels, metric="euclidean")
        euc_sil_man = silhouette_score(X, euc_labels, metric="manhattan")
        euc_db = davies_bouldin_score(X, euc_labels)

        comparison.append({
            "k": k,
            "algorithm": "K-Means (Euclidean L2)",
            "silhouette_euclidean": round(euc_sil_euc, 4),
            "silhouette_manhattan": round(euc_sil_man, 4),
            "davies_bouldin": round(euc_db, 4),
            "inertia": round(kmeans.inertia_, 2)
        })

        # 2. Manhattan K-Medians
        kmedians = run_manhattan_clustering(X, k=k, random_state=random_state)
        man_labels = kmedians.labels_
        man_sil_euc = silhouette_score(X, man_labels, metric="euclidean")
        man_sil_man = silhouette_score(X, man_labels, metric="manhattan")
        man_db = davies_bouldin_score(X, man_labels)

        comparison.append({
            "k": k,
            "algorithm": "K-Medians (Manhattan L1)",
            "silhouette_euclidean": round(man_sil_euc, 4),
            "silhouette_manhattan": round(man_sil_man, 4),
            "davies_bouldin": round(man_db, 4),
            "inertia": round(kmedians.inertia_, 2)
        })

    return pd.DataFrame(comparison)

def evaluate_cluster_stability(X: np.ndarray, k: int = 4, n_runs: int = 10) -> dict:
    """
    Tests clustering solution stability across varying random initializations.
    Computes pairwise Adjusted Rand Index (ARI) and Normalized Mutual Information (NMI).
    ARI close to 1.0 indicates strong deterministic partition stability.
    """
    all_labels = []
    for seed in range(n_runs):
        km = run_kmeans_clustering(X, k=k, random_state=seed * 17 + 3)
        all_labels.append(km.labels_)

    ari_scores = []
    nmi_scores = []

    for i in range(n_runs):
        for j in range(i + 1, n_runs):
            ari_scores.append(adjusted_rand_score(all_labels[i], all_labels[j]))
            nmi_scores.append(normalized_mutual_info_score(all_labels[i], all_labels[j]))

    return {
        "k": k,
        "n_runs": n_runs,
        "mean_ari": round(float(np.mean(ari_scores)), 4),
        "std_ari": round(float(np.std(ari_scores)), 4),
        "mean_nmi": round(float(np.mean(nmi_scores)), 4),
        "std_nmi": round(float(np.std(nmi_scores)), 4)
    }

def compute_silhouette_distribution(X: np.ndarray, labels: np.ndarray) -> dict:
    """
    Computes per-cluster silhouette scores to detect weak or overlapping clusters.
    """
    samples = silhouette_samples(X, labels)
    k = len(np.unique(labels))
    cluster_scores = {}

    for c in range(k):
        sub_samples = samples[labels == c]
        cluster_scores[c] = {
            "mean_silhouette": round(float(np.mean(sub_samples)), 4),
            "min_silhouette": round(float(np.min(sub_samples)), 4),
            "max_silhouette": round(float(np.max(sub_samples)), 4),
            "sample_count": int(len(sub_samples))
        }

    return cluster_scores
