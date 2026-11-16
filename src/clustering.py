"""
Clustering and Dimensionality Reduction Module.
Implements:
1. Standard K-Means (Euclidean Distance).
2. Manhattan-Distance K-Medians / L1 Clustering.
3. Multi-K hyperparameter sweep (K=2 through K=8, focusing on K=3, 4, 5).
4. Principal Component Analysis (PCA) 2D/3D projections and biplot loading analysis.
5. Cluster centroid profiling and assignment.
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances

class ManhattanKMedians:
    """
    K-Medians clustering using Manhattan (L1) distance metric.
    Robust to extreme airfare outliers and asymmetric price spikes.
    """
    def __init__(self, n_clusters: int = 4, max_iter: int = 300, tol: float = 1e-4, random_state: int = 42):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.cluster_centers_ = None
        self.labels_ = None
        self.inertia_ = None

    def fit(self, X: np.ndarray):
        np.random.seed(self.random_state)
        n_samples, n_features = X.shape

        # Initialize medians randomly from existing data points
        init_indices = np.random.choice(n_samples, self.n_clusters, replace=False)
        self.cluster_centers_ = X[init_indices].copy()

        for iteration in range(self.max_iter):
            # Compute Manhattan (L1) distance from all samples to cluster centers
            # shape: (n_samples, n_clusters)
            dist_matrix = pairwise_distances(X, self.cluster_centers_, metric="manhattan")
            labels = np.argmin(dist_matrix, axis=1)

            new_centers = np.zeros_like(self.cluster_centers_)
            for k in range(self.n_clusters):
                cluster_points = X[labels == k]
                if len(cluster_points) > 0:
                    # Component-wise median minimizes L1 distance
                    new_centers[k] = np.median(cluster_points, axis=0)
                else:
                    # If empty cluster, re-initialize to a random data point
                    new_centers[k] = X[np.random.choice(n_samples)]

            center_shift = np.sum(np.abs(self.cluster_centers_ - new_centers))
            self.cluster_centers_ = new_centers

            if center_shift < self.tol:
                break

        self.labels_ = labels
        # Calculate L1 inertia (sum of Manhattan distances to nearest center)
        final_dists = pairwise_distances(X, self.cluster_centers_, metric="manhattan")
        self.inertia_ = np.sum(np.min(final_dists, axis=1))
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        dist_matrix = pairwise_distances(X, self.cluster_centers_, metric="manhattan")
        return np.argmin(dist_matrix, axis=1)

def run_kmeans_clustering(X: np.ndarray, k: int, random_state: int = 42) -> KMeans:
    """
    Fits standard K-Means clustering with Euclidean distance.
    """
    kmeans = KMeans(
        n_clusters=k,
        init="k-means++",
        n_init=15,
        max_iter=300,
        random_state=random_state
    )
    kmeans.fit(X)
    return kmeans

def run_manhattan_clustering(X: np.ndarray, k: int, random_state: int = 42) -> ManhattanKMedians:
    """
    Fits K-Medians clustering using Manhattan (L1) distance.
    """
    kmedians = ManhattanKMedians(
        n_clusters=k,
        max_iter=300,
        tol=1e-4,
        random_state=random_state
    )
    kmedians.fit(X)
    return kmedians

def compute_pca_projection(X: np.ndarray, n_components: int = 3):
    """
    Applies PCA dimensionality reduction for visual inspection.
    Returns:
    - pca model
    - X_pca (projected coordinates)
    - explained_variance_ratio
    - loadings DataFrame
    """
    pca = PCA(n_components=n_components, random_state=42)
    X_pca = pca.fit_transform(X)
    explained_variance = pca.explained_variance_ratio_

    return pca, X_pca, explained_variance

def generate_cluster_archetypes(route_df: pd.DataFrame, cluster_labels: np.ndarray, k: int) -> dict:
    """
    Assigns human-interpretable domain archetypes to discovered route clusters
    based on mean price, duration, volatility, and surge characteristics.
    """
    df = route_df.copy()
    df["cluster"] = cluster_labels
    cluster_profiles = {}

    for c in range(k):
        sub = df[df["cluster"] == c]
        avg_price = sub["mean_price"].mean()
        avg_dur = sub["avg_duration"].mean()
        avg_vol = sub["price_cv"].mean()
        avg_surge = sub["last_minute_surge_ratio"].mean()
        avg_biz = sub["business_ratio"].mean()
        direct_pct = sub["direct_flight_ratio"].mean()

        # Defensible archetype categorization based on pricing scale, duration, and directness
        if avg_dur > 10.0 or avg_price > 75000:
            archetype_name = "Ultra-Long-Haul Intercontinental Corridors"
            description = "High-ticket intercontinental corridors with premium cabin reliance, wide fare dispersion, and significant advance booking lead times."
            badge_color = "#6366f1"  # Indigo
        elif avg_price > 35000:
            archetype_name = "Regional International Gateway Corridors"
            description = "High-volume short-haul international business and transit hubs with elevated baseline yields and steady business traveler demand."
            badge_color = "#0ea5e9"  # Sky Blue
        elif avg_dur < 3.2 and direct_pct > 0.50:
            archetype_name = "High-Frequency Short-Haul Regional Shuttles"
            description = "High direct flight density routes between neighboring economic hubs, driven by low-cost carriers with rapid departure day price spikes."
            badge_color = "#10b981"  # Emerald
        else:
            archetype_name = "Cross-Country Domestic Trunk Corridors"
            description = "Major domestic cross-country connecting lines connecting primary Indian metros, characterized by mixed direct/connecting traffic."
            badge_color = "#f59e0b"  # Amber

        cluster_profiles[c] = {
            "cluster_id": c,
            "archetype_name": archetype_name,
            "description": description,
            "badge_color": badge_color,
            "route_count": len(sub),
            "routes": sub["route"].tolist(),
            "mean_price": round(float(avg_price), 2),
            "median_price": round(float(sub["median_price"].mean()), 2),
            "avg_duration_hrs": round(float(avg_dur), 2),
            "price_volatility_cv": round(float(avg_vol), 4),
            "last_minute_surge_ratio": round(float(avg_surge), 2),
            "direct_flight_pct": round(float(direct_pct * 100), 1),
            "business_share_pct": round(float(avg_biz * 100), 1)
        }

    return cluster_profiles
