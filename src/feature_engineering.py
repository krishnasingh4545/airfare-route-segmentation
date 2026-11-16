"""
Feature Engineering and Preprocessing Module for Flight Price Prediction & Route Segmentation.
Performs:
1. Handling missing values (median/mode imputation).
2. Categorical variable encoding (Ordinal & One-Hot).
3. Route-level historical pricing behavior feature aggregation.
4. Numerical scaling (StandardScaler & RobustScaler).
5. Generation of modeling matrices for K-Means clustering.
"""

import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, RobustScaler

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def preprocess_flight_records(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw flight records, handles missing values, and creates standard derived variables.
    """
    df = df.copy()

    # Drop index column if present
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    # 1. Missing Value Check & Imputation
    num_cols = df.select_dtypes(include=[np.number]).columns
    cat_cols = df.select_dtypes(include=["object"]).columns

    for col in num_cols:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(df[col].median())

    for col in cat_cols:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(df[col].mode()[0])

    # 2. Derive Route identifier
    df["route"] = df["source_city"] + " - " + df["destination_city"]

    # 3. Ordinal mapping for stops & class
    stops_map = {"zero": 0, "one": 1, "two_or_more": 2}
    df["stops_num"] = df["stops"].map(stops_map).fillna(1)

    class_map = {"Economy": 0, "Business": 1}
    df["class_num"] = df["class"].map(class_map).fillna(0)

    # 4. Booking advance windows
    df["is_last_minute"] = (df["days_left"] <= 3).astype(int)
    df["is_early_bird"] = (df["days_left"] >= 21).astype(int)
    df["is_peak_hour"] = df["departure_time"].isin(["Morning", "Evening"]).astype(int)

    return df

def aggregate_route_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates historical flight pricing behavior at the route corridor level.
    Constructs behavioral dimensions:
    - Mean & Median Price
    - Price Standard Deviation & Coefficient of Variation (Volatility)
    - Last-Minute Surge Ratio (Yield Management Aggressiveness)
    - Early Bird Savings Gradient
    - Price Spread (90th - 10th Percentile)
    - Business Class Share & Spread
    - Direct Flight Ratio & Average Duration
    - Airline Competition Index
    """
    routes = []

    for route_name, group in df.groupby("route"):
        src = group["source_city"].iloc[0]
        dst = group["destination_city"].iloc[0]
        sample_count = len(group)

        # Baseline pricing metrics
        mean_price = group["price"].mean()
        median_price = group["price"].median()
        price_std = group["price"].std() if sample_count > 1 else 0
        price_cv = (price_std / mean_price) if mean_price > 0 else 0

        # Percentiles
        p10 = group["price"].quantile(0.10)
        p25 = group["price"].quantile(0.25)
        p75 = group["price"].quantile(0.75)
        p90 = group["price"].quantile(0.90)
        price_iqr = p75 - p25
        price_spread = p90 - p10

        # Last minute pricing behavior (days_left <= 3 vs days_left >= 21)
        last_minute = group[group["days_left"] <= 3]["price"]
        advance_book = group[group["days_left"] >= 21]["price"]

        last_min_mean = last_minute.mean() if len(last_minute) > 0 else mean_price * 1.5
        advance_mean = advance_book.mean() if len(advance_book) > 0 else mean_price * 0.9
        last_minute_surge_ratio = last_min_mean / advance_mean if advance_mean > 0 else 1.5

        # Flight duration & Direct flight ratio
        avg_duration = group["duration"].mean()
        direct_ratio = (group["stops_num"] == 0).mean()

        # Business class share & premium multiplier
        business_ratio = (group["class_num"] == 1).mean()
        econ_mean = group[group["class_num"] == 0]["price"].mean() if (group["class_num"] == 0).any() else mean_price
        biz_mean = group[group["class_num"] == 1]["price"].mean() if (group["class_num"] == 1).any() else mean_price * 3.5
        business_premium_ratio = (biz_mean / econ_mean) if econ_mean > 0 else 3.5

        # Peak hour departure premium
        peak_mean = group[group["is_peak_hour"] == 1]["price"].mean() if (group["is_peak_hour"] == 1).any() else mean_price
        offpeak_mean = group[group["is_peak_hour"] == 0]["price"].mean() if (group["is_peak_hour"] == 0).any() else mean_price
        peak_premium_ratio = (peak_mean / offpeak_mean) if offpeak_mean > 0 else 1.1

        # Carrier competition
        unique_airlines = group["airline"].nunique()

        routes.append({
            "route": route_name,
            "source_city": src,
            "destination_city": dst,
            "sample_count": sample_count,
            "mean_price": round(mean_price, 2),
            "median_price": round(median_price, 2),
            "price_std": round(price_std, 2),
            "price_cv": round(price_cv, 4),
            "p10_price": round(p10, 2),
            "p25_price": round(p25, 2),
            "p75_price": round(p75, 2),
            "p90_price": round(p90, 2),
            "price_spread": round(price_spread, 2),
            "price_iqr": round(price_iqr, 2),
            "last_minute_surge_ratio": round(last_minute_surge_ratio, 4),
            "avg_duration": round(avg_duration, 2),
            "direct_flight_ratio": round(direct_ratio, 4),
            "business_ratio": round(business_ratio, 4),
            "business_premium_ratio": round(business_premium_ratio, 4),
            "peak_premium_ratio": round(peak_premium_ratio, 4),
            "airline_count": unique_airlines
        })

    route_df = pd.DataFrame(routes)
    return route_df

def prepare_clustering_matrix(route_df: pd.DataFrame, feature_cols: list = None, scaler_type: str = "standard"):
    """
    Extracts numerical features and scales them for clustering algorithms.
    Supports 'standard' (StandardScaler) and 'robust' (RobustScaler).
    """
    if feature_cols is None:
        feature_cols = [
            "mean_price",
            "price_cv",
            "price_spread",
            "last_minute_surge_ratio",
            "avg_duration",
            "direct_flight_ratio",
            "business_ratio",
            "business_premium_ratio",
            "peak_premium_ratio"
        ]

    X_raw = route_df[feature_cols].values

    if scaler_type == "robust":
        scaler = RobustScaler()
    else:
        scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X_raw)
    return X_scaled, scaler, feature_cols

if __name__ == "__main__":
    from data_loader import load_or_generate_dataset
    df = load_or_generate_dataset()
    clean_df = preprocess_flight_records(df)
    routes_df = aggregate_route_features(clean_df)
    print(f"Extracted {len(routes_df)} unique routes.")
    print(routes_df.head())
