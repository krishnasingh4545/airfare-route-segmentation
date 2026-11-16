"""
Jupyter Notebook Generator.
Produces structured, reproducible .ipynb notebooks for faculty submission.
"""

import os
import json

NOTEBOOKS_DIR = os.path.dirname(__file__)

def make_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.10.11"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

def markdown_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.strip().split("\n")]
    }

def code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.strip().split("\n")]
    }

def generate_all_notebooks():
    # ----------------------------------------------------
    # Notebook 1: Data Exploration and Preprocessing
    # ----------------------------------------------------
    nb1_cells = [
        markdown_cell("""# Airfare Route Segmentation by Historical Pricing Behaviour
## Phase 1: Data Source Preparation, Feature Engineering & Scaling
**Course / Domain**: Unsupervised Machine Learning & Revenue Management  
**Dataset**: Kaggle 'Flight Price Prediction' Dataset (`Clean_Dataset.csv`)  
**Objective**: Prepare raw flight observations, handle missing values, encode categorical variables, aggregate route-level pricing behavior, and scale numerical matrices for clustering.
"""),
        code_cell("""import os
import sys
import numpy as np
import pandas as pd

# Add src to path
sys.path.append(os.path.abspath("../src"))
from data_loader import load_or_generate_dataset
from feature_engineering import preprocess_flight_records, aggregate_route_features, prepare_clustering_matrix

print("Environment configured successfully.")
"""),
        markdown_cell("""### 1. Dataset Loading and Schema Verification
We inspect the Kaggle Flight Price Prediction dataset schema containing over 50,000 observations across major domestic and international commercial flight corridors.
"""),
        code_cell("""df = load_or_generate_dataset(num_samples=50000)
print(f"Dataset Shape: {df.shape}")
df.head(10)
"""),
        markdown_cell("""### 2. Handling Missing Values and Categorical Encoding
- Missing values in numerical attributes are imputed with the median.
- Missing values in categorical attributes are imputed with the mode.
- Ordinal encoding is applied to `stops` (zero: 0, one: 1, two_or_more: 2) and `class` (Economy: 0, Business: 1).
"""),
        code_cell("""clean_df = preprocess_flight_records(df)
print("Missing values summary after imputation:")
print(clean_df.isnull().sum())
print("\nTransformed columns:")
print(clean_df[['route', 'stops_num', 'class_num', 'is_last_minute', 'is_peak_hour']].head())
"""),
        markdown_cell("""### 3. Route-Level Behavioral Aggregation
In revenue management, pricing behavior is characterized at the **route corridor level** by calculating:
- Mean and Median Fare (central pricing scale)
- Price Volatility (Standard Deviation & Coefficient of Variation $CV = \sigma / \mu$)
- Yield Management Aggressiveness (Last-Minute Surge Ratio: fare at $\le$ 3 days vs $\ge$ 21 days)
- Price Spread (90th minus 10th percentile)
- Average Duration and Direct Flight Ratio
- Business Class Demand Share
"""),
        code_cell("""route_df = aggregate_route_features(clean_df)
print(f"Aggregated {len(route_df)} commercial route corridors.")
route_df.head()
"""),
        markdown_cell("""### 4. Numerical Standardization (Feature Scaling)
Because distance-based algorithms such as K-Means are sensitive to variable magnitudes (e.g. Fares in thousands vs Duration in single digits), we apply `StandardScaler`:
$$z = \\frac{x - \\mu}{\\sigma}$$
"""),
        code_cell("""X_scaled, scaler, feature_names = prepare_clustering_matrix(route_df)
print("Scaled matrix shape:", X_scaled.shape)
print("Features used for clustering:")
for idx, f in enumerate(feature_names):
    print(f"  {idx+1}. {f} (mean={X_scaled[:, idx].mean():.2f}, std={X_scaled[:, idx].std():.2f})")
""")
    ]

    nb1 = make_notebook(nb1_cells)
    with open(os.path.join(NOTEBOOKS_DIR, "01_data_exploration_and_prep.ipynb"), "w") as f:
        json.dump(nb1, f, indent=2)

    # ----------------------------------------------------
    # Notebook 2: Clustering, Distance Comparison & PCA
    # ----------------------------------------------------
    nb2_cells = [
        markdown_cell("""# Airfare Route Segmentation by Historical Pricing Behaviour
## Phase 2: Unsupervised Clustering, Metric Evaluation & PCA Visualization
**Objective**:
1. Apply K-Means across at least three cluster counts ($K=3, 4, 5$).
2. Compare Euclidean ($L_2$) and Manhattan ($L_1$) distance metrics.
3. Perform PCA dimensionality reduction (Explained Variance & Loadings).
4. Evaluate clustering solutions using WCSS (Inertia), Silhouette Score, and Davies-Bouldin Index.
5. Select a defensible clustering structure.
"""),
        code_cell("""import os
import sys
import numpy as np
import pandas as pd

sys.path.append(os.path.abspath("../src"))
from data_loader import load_or_generate_dataset
from feature_engineering import preprocess_flight_records, aggregate_route_features, prepare_clustering_matrix
from clustering import run_kmeans_clustering, run_manhattan_clustering, compute_pca_projection
from evaluation import evaluate_kmeans_sweep, compare_distance_metrics, evaluate_cluster_stability

# Prepare data
df = load_or_generate_dataset()
clean_df = preprocess_flight_records(df)
route_df = aggregate_route_features(clean_df)
X_scaled, scaler, feature_names = prepare_clustering_matrix(route_df)
"""),
        markdown_cell("""### 1. Multi-K Evaluation Sweep: WCSS, Silhouette & Davies-Bouldin
We evaluate K-Means across $K \\in [2, 8]$ to determine the optimal clustering partition.
"""),
        code_cell("""k_eval_df = evaluate_kmeans_sweep(X_scaled, k_range=[2, 3, 4, 5, 6, 7, 8])
print(k_eval_df.to_string(index=False))
"""),
        markdown_cell("""### 2. Distance Metric Benchmark: Euclidean ($L_2$) vs Manhattan ($L_1$)
**Theoretical Justification**:
Airfare time-series exhibit extreme positive price spikes (e.g. emergency bookings, holiday peak fares).
- **Euclidean Distance** ($L_2$ norm): Squares errors ($\sum (x_i - \mu_i)^2$), causing cluster centroids to be pulled disproportionately toward extreme outliers.
- **Manhattan Distance** ($L_1$ norm): Evaluates absolute differences ($\sum |x_i - c_i|$), yielding robust medians that resist leverage from price spikes.
"""),
        code_cell("""dist_comparison_df = compare_distance_metrics(X_scaled, k_values=[3, 4, 5])
print(dist_comparison_df.to_string(index=False))
"""),
        markdown_cell("""### 3. Principal Component Analysis (PCA) Dimensionality Reduction
We project the 9-dimensional route behavior space onto principal components.
"""),
        code_cell("""pca, X_pca, exp_var = compute_pca_projection(X_scaled, n_components=3)
print(f"Explained Variance Ratio:")
print(f"  PC1: {exp_var[0]*100:.2f}%")
print(f"  PC2: {exp_var[1]*100:.2f}%")
print(f"  PC3: {exp_var[2]*100:.2f}%")
print(f"Total 3D Variance Captured: {np.sum(exp_var)*100:.2f}%\n")

loadings_df = pd.DataFrame(pca.components_.T, index=feature_names, columns=['PC1', 'PC2', 'PC3'])
print("PCA Loadings Matrix:")
print(loadings_df.round(3))
"""),
        markdown_cell("""### 4. Defensible Structure Selection ($K=4$) & Stability Verification
We assess cluster stability across 10 random seed initializations using the **Adjusted Rand Index (ARI)** and **Normalized Mutual Information (NMI)**.
"""),
        code_cell("""stability = evaluate_cluster_stability(X_scaled, k=4, n_runs=10)
print(f"Stability Results for K=4:")
print(f"  Mean Adjusted Rand Index (ARI): {stability['mean_ari']} (+/- {stability['std_ari']})")
print(f"  Mean Normalized Mutual Info (NMI): {stability['mean_nmi']} (+/- {stability['std_nmi']})")
print("An ARI of 1.0 indicates perfect deterministic stability across varying seed initializations.")
""")
    ]

    nb2 = make_notebook(nb2_cells)
    with open(os.path.join(NOTEBOOKS_DIR, "02_clustering_and_evaluation.ipynb"), "w") as f:
        json.dump(nb2, f, indent=2)

    # ----------------------------------------------------
    # Notebook 3: Cluster Interpretation & Ethics
    # ----------------------------------------------------
    nb3_cells = [
        markdown_cell("""# Airfare Route Segmentation by Historical Pricing Behaviour
## Phase 3: Cluster Profiling, Archetypes, Limitations & Responsible AI
**Objective**:
1. Interpret discovered clusters into actionable revenue management archetypes.
2. Characterize behavioral dimensions (surge multiplier, advance window, volatility).
3. Document dataset limitations, survivorship bias, and sampling bias.
4. Provide an ethical framework for algorithmic pricing and consumer protection.
"""),
        code_cell("""import os
import sys
import json
import pandas as pd

sys.path.append(os.path.abspath("../src"))
from report_generator import generate_ethical_and_limitations_report

# Load generated assignments
assignments_path = os.path.abspath("../data/route_cluster_assignments.csv")
route_df = pd.read_csv(assignments_path)

print(f"Loaded {len(route_df)} clustered route assignments.")
"""),
        markdown_cell("""### 1. Cluster Profiles and Commercial Archetypes
We summarize each discovered cluster by its key economic metrics:
"""),
        code_cell("""cluster_summary = route_df.groupby(['cluster', 'archetype_name']).agg(
    route_count=('route', 'count'),
    mean_fare=('mean_price', 'mean'),
    median_fare=('median_price', 'mean'),
    avg_duration_hrs=('avg_duration', 'mean'),
    surge_ratio=('last_minute_surge_ratio', 'mean'),
    volatility_cv=('price_cv', 'mean'),
    direct_flight_pct=('direct_flight_ratio', lambda x: x.mean() * 100),
    business_share_pct=('business_ratio', lambda x: x.mean() * 100)
).round(2)

print(cluster_summary.to_string())
"""),
        markdown_cell("""### 2. Documented Dataset Limitations and Sampling Bias
"""),
        code_cell("""report = generate_ethical_and_limitations_report()
print("DATASET LIMITATIONS & SAMPLING BIASES:")
for idx, lim in enumerate(report['limitations']):
    print(f"\\n{idx+1}. {lim['title']}:")
    print(f"   {lim['description']}")
"""),
        markdown_cell("""### 3. Ethical Considerations & Responsible Dynamic Pricing Framework
"""),
        code_cell("""print("ETHICAL CONSIDERATIONS & RESPONSIBLE AI USE:")
for idx, eth in enumerate(report['ethical_considerations']):
    print(f"\\n{idx+1}. {eth['title']}:")
    print(f"   {eth['description']}")
""")
    ]

    nb3 = make_notebook(nb3_cells)
    with open(os.path.join(NOTEBOOKS_DIR, "03_cluster_interpretation.ipynb"), "w") as f:
        json.dump(nb3, f, indent=2)

    print("All 3 Jupyter Notebooks generated successfully!")

if __name__ == "__main__":
    generate_all_notebooks()
