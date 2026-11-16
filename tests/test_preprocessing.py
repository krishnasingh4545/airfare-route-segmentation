"""
Unit Tests for Preprocessing and Feature Engineering.
"""

import os
import sys
import unittest
import numpy as np
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from data_loader import load_or_generate_dataset
from feature_engineering import (
    preprocess_flight_records,
    aggregate_route_features,
    prepare_clustering_matrix
)

class TestPreprocessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw_df = load_or_generate_dataset(num_samples=1000)

    def test_raw_dataset_structure(self):
        self.assertGreaterEqual(len(self.raw_df), 1000)
        expected_cols = ["airline", "source_city", "destination_city", "price", "days_left"]
        for col in expected_cols:
            self.assertIn(col, self.raw_df.columns)

    def test_preprocessing_imputation_and_encoding(self):
        clean = preprocess_flight_records(self.raw_df)
        self.assertEqual(clean.isnull().sum().sum(), 0)
        self.assertIn("stops_num", clean.columns)
        self.assertIn("class_num", clean.columns)
        self.assertIn("route", clean.columns)

    def test_route_aggregation(self):
        clean = preprocess_flight_records(self.raw_df)
        routes = aggregate_route_features(clean)
        self.assertGreater(len(routes), 5)
        self.assertIn("mean_price", routes.columns)
        self.assertIn("last_minute_surge_ratio", routes.columns)
        self.assertIn("price_cv", routes.columns)

    def test_matrix_scaling(self):
        clean = preprocess_flight_records(self.raw_df)
        routes = aggregate_route_features(clean)
        X, scaler, feature_names = prepare_clustering_matrix(routes)
        self.assertEqual(len(X.shape), 2)
        self.assertAlmostEqual(float(np.mean(X[:, 0])), 0.0, delta=0.5)

if __name__ == "__main__":
    unittest.main()
