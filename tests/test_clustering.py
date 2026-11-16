"""
Unit Tests for Clustering and Dimensionality Reduction.
"""

import os
import sys
import unittest
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from clustering import (
    run_kmeans_clustering,
    run_manhattan_clustering,
    compute_pca_projection
)
from evaluation import evaluate_kmeans_sweep, compare_distance_metrics

class TestClustering(unittest.TestCase):
    def setUp(self):
        np.random.seed(42)
        # 3 artificial clusters in 5-dimensional space
        c1 = np.random.normal(loc=-3, scale=0.5, size=(15, 5))
        c2 = np.random.normal(loc=0, scale=0.5, size=(15, 5))
        c3 = np.random.normal(loc=4, scale=0.5, size=(15, 5))
        self.X = np.vstack([c1, c2, c3])

    def test_kmeans_euclidean(self):
        km = run_kmeans_clustering(self.X, k=3, random_state=42)
        self.assertEqual(len(np.unique(km.labels_)), 3)
        self.assertGreater(km.inertia_, 0)

    def test_manhattan_clustering(self):
        kmed = run_manhattan_clustering(self.X, k=3, random_state=42)
        self.assertEqual(len(np.unique(kmed.labels_)), 3)
        self.assertGreater(kmed.inertia_, 0)

    def test_pca_projection(self):
        pca, X_pca, exp_var = compute_pca_projection(self.X, n_components=3)
        self.assertEqual(X_pca.shape, (45, 3))
        self.assertEqual(len(exp_var), 3)
        self.assertAlmostEqual(float(np.sum(exp_var)), 1.0, delta=0.2)

    def test_evaluation_sweep(self):
        res_df = evaluate_kmeans_sweep(self.X, k_range=[2, 3, 4])
        self.assertEqual(len(res_df), 3)
        self.assertIn("silhouette", res_df.columns)
        self.assertIn("davies_bouldin", res_df.columns)

if __name__ == "__main__":
    unittest.main()
