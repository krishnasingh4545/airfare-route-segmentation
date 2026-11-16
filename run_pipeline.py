"""
End-to-End Reproducible Pipeline for Airfare Route Segmentation Using Clustering.
Executes data preprocessing, multi-K evaluation, Euclidean vs Manhattan comparison,
PCA dimensionality reduction, cluster interpretation, and export of results.
"""

import os
import sys
import json
import numpy as np
import pandas as pd

# Add src to system path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from data_loader import load_or_generate_dataset
from feature_engineering import (
    preprocess_flight_records,
    aggregate_route_features,
    prepare_clustering_matrix
)
from clustering import (
    run_kmeans_clustering,
    compute_pca_projection,
    generate_cluster_archetypes
)
from evaluation import (
    evaluate_kmeans_sweep,
    compare_distance_metrics,
    evaluate_cluster_stability,
    compute_silhouette_distribution
)
from report_generator import generate_ethical_and_limitations_report

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def run():
    print("=" * 80)
    print("AIRFARE ROUTE SEGMENTATION BY HISTORICAL PRICING BEHAVIOUR")
    print("Unsupervised Learning Machine Learning Pipeline")
    print("=" * 80)

    # 1. Load Data
    print("\n[Step 1/7] Loading Kaggle 'Flight Price Prediction' Dataset (Expanded Network)...")
    raw_df = load_or_generate_dataset(num_samples=70000, force_regenerate=True)
    print(f"Total Flight Records Loaded: {len(raw_df):,}")

    # 2. Preprocess & Feature Engineering
    print("\n[Step 2/7] Preprocessing Data & Handling Missing Values...")
    clean_df = preprocess_flight_records(raw_df)
    
    print("\n[Step 3/7] Aggregating Historical Pricing Behaviour by Route Corridor...")
    route_df = aggregate_route_features(clean_df)
    route_csv_path = os.path.join(DATA_DIR, "processed_route_features.csv")
    route_df.to_csv(route_csv_path, index=False)
    print(f"Aggregated {len(route_df)} commercial route corridors.")
    print(f"Exported to {route_csv_path}")

    # 3. Prepare Scaled Clustering Matrix
    X_scaled, scaler, feature_cols = prepare_clustering_matrix(route_df)
    print(f"Clustering Matrix Shape: {X_scaled.shape} across {len(feature_cols)} behavioural features:")
    for f in feature_cols:
        print(f"  - {f}")

    # 4. Multi-K Hyperparameter Sweep (WCSS, Silhouette, Davies-Bouldin)
    print("\n[Step 4/7] Evaluating K-Means Across Multiple Cluster Counts (K=2 to 8)...")
    k_eval_df = evaluate_kmeans_sweep(X_scaled, k_range=[2, 3, 4, 5, 6, 7, 8])
    print(k_eval_df.to_string(index=False))

    # 5. Distance Metric Comparison (Euclidean vs Manhattan)
    print("\n[Step 5/7] Comparing Euclidean vs Manhattan Distance Formulations (K=3, 4, 5)...")
    dist_comp_df = compare_distance_metrics(X_scaled, k_values=[3, 4, 5])
    print(dist_comp_df.to_string(index=False))

    # 6. Cluster Stability & Selection of Defensible K
    chosen_k = 4
    print(f"\n[Step 6/7] Defensible Clustering Selected: K={chosen_k}")
    stability_res = evaluate_cluster_stability(X_scaled, k=chosen_k, n_runs=10)
    print(f"Stability (10 Random Seed Initializations):")
    print(f"  Mean Adjusted Rand Index (ARI): {stability_res['mean_ari']} (+/- {stability_res['std_ari']})")
    print(f"  Mean Normalized Mutual Info (NMI): {stability_res['mean_nmi']} (+/- {stability_res['std_nmi']})")

    # Final Fit on chosen K
    final_kmeans = run_kmeans_clustering(X_scaled, k=chosen_k, random_state=42)
    cluster_labels = final_kmeans.labels_
    route_df["cluster"] = cluster_labels

    # PCA Dimensionality Reduction
    pca, X_pca, exp_var = compute_pca_projection(X_scaled, n_components=3)
    route_df["pca_1"] = X_pca[:, 0]
    route_df["pca_2"] = X_pca[:, 1]
    route_df["pca_3"] = X_pca[:, 2]

    print(f"PCA Variance Explained: PC1={exp_var[0]*100:.1f}%, PC2={exp_var[1]*100:.1f}%, PC3={exp_var[2]*100:.1f}% (Total: {np.sum(exp_var)*100:.1f}%)")

    # Cluster Archetypes & Profiling
    archetypes = generate_cluster_archetypes(route_df, cluster_labels, k=chosen_k)
    route_df["archetype_name"] = route_df["cluster"].map(lambda c: archetypes[c]["archetype_name"])

    # Export labeled assignments
    assignments_path = os.path.join(DATA_DIR, "route_cluster_assignments.csv")
    route_df.to_csv(assignments_path, index=False)
    print(f"Saved clustered route assignments to {assignments_path}")

    # 7. Export Comprehensive Model Metadata for Web Application & Reports
    print("\n[Step 7/7] Generating Cluster Interpretations, Limitations & Ethical Document...")
    silhouette_dist = compute_silhouette_distribution(X_scaled, cluster_labels)
    ethical_doc = generate_ethical_and_limitations_report()

    # PCA feature loadings
    loadings = pd.DataFrame(
        pca.components_.T,
        columns=["PC1", "PC2", "PC3"],
        index=feature_cols
    ).round(4).to_dict(orient="index")

    # PCA points serialization
    pca_points = []
    for idx, row in route_df.iterrows():
        pca_points.append({
            "route": row["route"],
            "cluster": int(row["cluster"]),
            "archetype": row["archetype_name"],
            "pc1": round(float(row["pca_1"]), 3),
            "pc2": round(float(row["pca_2"]), 3),
            "pc3": round(float(row["pca_3"]), 3),
            "mean_price": float(row["mean_price"]),
            "avg_duration": float(row["avg_duration"]),
            "surge_ratio": float(row["last_minute_surge_ratio"])
        })

    model_metadata = {
        "chosen_k": chosen_k,
        "k_eval_sweep": k_eval_df.to_dict(orient="records"),
        "distance_comparison": dist_comp_df.to_dict(orient="records"),
        "stability": stability_res,
        "silhouette_distribution": silhouette_dist,
        "pca_variance_explained": [round(float(v), 4) for v in exp_var],
        "pca_loadings": loadings,
        "pca_points": pca_points,
        "archetypes": archetypes,
        "ethical_considerations": ethical_doc["ethical_considerations"],
        "limitations": ethical_doc["limitations"],
        "feature_names": feature_cols
    }

    metrics_json_path = os.path.join(DATA_DIR, "model_metrics.json")
    with open(metrics_json_path, "w") as f:
        json.dump(model_metadata, f, indent=4)
    print(f"Saved complete metrics payload to {metrics_json_path}")

    print("\n" + "=" * 80)
    print("PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    run()
