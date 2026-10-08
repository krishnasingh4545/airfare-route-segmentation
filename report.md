# Airfare Route Segmentation by Booking-Window Pricing Behaviour Using Clustering

**Author:** Krishna Kumar Singh
**Date:** October 2025
**Project Type:** Unsupervised Machine Learning / Data Science

---

## Abstract

This project segments 30 Indian domestic airfare routes based on their booking-window pricing behaviour using K-Means clustering. We analyse 294,745 cleaned records from six major Indian cities (Delhi, Mumbai, Bangalore, Chennai, Hyderabad, Kolkata) and build 13 pricing-behaviour features per route, including average price, volatility (coefficient of variation), and last-minute premium. We cluster Economy and Business class separately due to their radically different price distributions. Our analysis finds 4 distinct Economy segments (Premium, Metro, Value, Last-Minute Punishers) and 3 Business segments (Delhi Metro, East-South Stable, Premium Mumbai Mixed). A key finding: Economy prices increase up to 3.11x for last-minute bookings on the Chennai-Mumbai route, while Business class prices remain relatively flat (max 1.20x). This work demonstrates that pricing behaviour segmentation differs fundamentally between Economy and Business classes, with Economy segments being driven by behaviour and Business segments being driven by geography.

---

## 1. Introduction

### 1.1 Problem Statement

Airlines and online travel agencies (OTAs) such as MakeMyTrip, Booking.com, and Skyscanner need to understand how prices vary across routes and booking horizons. Not all routes behave the same way: some are stable and predictable, others punish last-minute buyers heavily, and some have strong seasonality. Treating all routes identically leads to poor revenue management, missed pricing opportunities, and suboptimal customer recommendations.

This project addresses the question: **Can we automatically segment airfare routes based on their pricing behaviour over the booking window?**

### 1.2 Objectives

1. Build a dataset of Indian domestic airfare routes with cleaned price data.
2. Engineer pricing-behaviour features that capture the level, volatility, and time-dependent dynamics of each route.
3. Apply K-Means clustering to group routes with similar pricing behaviour.
4. Interpret the resulting segments in business terms.
5. Compare Economy and Business class pricing behaviour.

### 1.3 Scope and Limitations

- **Scope:** 30 directional routes between 6 major Indian cities.
- **Time axis:** Booking window (`days_left`), not calendar date.
- **Limitation:** The dataset does not contain calendar dates, so calendar-based seasonality is not analysed.
- **Future work:** Extend to include calendar seasonality and a Streamlit dashboard for route-level recommendations.

---

## 2. Data

### 2.1 Source

The dataset is the "Flight Price Cleaned" dataset from Kaggle (originally scraped from Indian OTA platforms). It contains 300,153 records representing flight searches with prices.

### 2.2 Columns

| Column | Description |
|--------|-------------|
| airline | Airline carrier |
| flight | Flight number |
| source_city | Departure city |
| destination_city | Arrival city |
| departure_time | Time-of-day bucket |
| arrival_time | Time-of-day bucket |
| stops | Number of stops |
| class | Economy or Business |
| duration | Flight duration (hours) |
| days_left | Days before departure |
| price | Ticket price (INR) |

### 2.3 Cleaning Steps

1. Created a composite `route` column: `source_city + "-" + destination_city`.
2. Removed exact duplicates.
3. Coerced numeric columns to correct types.
4. Trimmed outliers per class (1% top and bottom on price) to preserve valid Business fares.
5. Final dataset: 294,745 rows, 30 unique routes.

### 2.4 Distribution Insight

The dataset has bimodal pricing behaviour:
- Economy: median ₹5,772, range ₹1,714 – ₹19,667
- Business: median ₹53,164, range ₹20,684 – ₹84,896

This ~9x price gap confirms that Economy and Business must be analysed separately.

---

## 3. Methodology

### 3.1 Overall Pipeline

The project follows a standard data science pipeline:

1. **Data ingestion:** Download from Kaggle via API.
2. **Cleaning:** Handle duplicates, types, outliers.
3. **Feature engineering:** Compress per-route price series into summary features.
4. **Scaling:** StandardScaler on all features.
5. **Clustering:** K-Means with elbow method + silhouette score for k selection.
6. **Interpretation:** Profile clusters, name them, validate business meaning.
7. **Visualization:** PCA scatter, boxplots, price curves.

### 3.2 Why Clustering?

Clustering is unsupervised learning — no labels are needed. Unlike supervised models (which require known categories), clustering discovers structure on its own. For a novel question like "how many pricing behaviour types exist?" this is the correct approach.

### 3.3 Why K-Means?

- Fast and scalable
- Interpretable (each cluster has a clear centroid)
- Works well with the moderate dataset size (30 routes per class)
- Provides a clear path to business meaning

Alternative methods (hierarchical, DBSCAN, GMM) were considered. K-Means was chosen for its speed and interpretability.

---

## 4. Feature Engineering

### 4.1 Rationale

Each route has thousands of raw price records — one per (flight × days_left) combination. To cluster routes, we need a fixed-length numeric vector per route. We compress each route's price series into 13 features.

### 4.2 Features Built

**Level (how expensive is this route?):**
- mean_price, median_price, min_price, max_price

**Variability (how much does price swing?):**
- std_price, cv_price (= std/mean), range_price, iqr_price

**Shape (is the distribution symmetric?):**
- skew_price

**Time-based (how does price change over booking window?):**
- last_minute_premium (price at days≤5 / price at days≥40)
- late_price (avg at days≤5)
- early_price (avg at days≥40)
- days_price_corr (Pearson corr between days_left and price)
- days_price_slope (linear regression slope)

### 4.3 Feature Selection

Using relative variation (std/mean) across routes:
- Economy: dropped `max_price` (0.006) and `range_price` (0.028)
- Business: dropped `max_price` (0.020) and `last_minute_premium` (0.034)

Final: 11 features per route.

### 4.4 Scaling

Log-transform applied to skewed money features (`mean_price`, `late_price`, `early_price`, etc.). Then StandardScaler applied to all features so that mean=0, std=1.

**Why scale?** K-Means uses Euclidean distance. Without scaling, features with larger numeric ranges (e.g., mean_price in thousands) dominate features with smaller ranges (e.g., last_minute_premium ~2–3). Standardization makes every feature contribute equally.

---


## 5. Results

### 5.1 Overview

We clustered Economy and Business routes separately. K-Means was run for k = 2 to 8, and k was chosen by combining elbow method, silhouette score, cluster-size sanity, and business interpretability.

| Class | Best k | Silhouette | Routes per Cluster |
|---|---|---|---|
| Economy | 4 | 0.328 | 11, 10, 2, 7 |
| Business | 3 | 0.338 | 6, 7, 17 |

PCA projections captured 67.3% (Economy) and 64.4% (Business) of the total variance in two dimensions, providing reliable visual confirmation of the cluster separation.

### 5.2 Economy Segments

Four distinct Economy segments were identified:

**Cluster 0 — Premium Routes (11 routes)**
- Highest mean price: Rs.7,198
- Moderate last-minute premium: 2.24x
- Example routes: Delhi-Kolkata, Mumbai-Kolkata, Bangalore-Kolkata
- Profile: Expensive regardless of booking window; stable premium behaviour.

**Cluster 1 — Metro Corridors (10 routes)**
- Mean price: Rs.6,010 (lowest)
- Last-minute premium: 2.47x
- Example routes: Delhi-Mumbai, Mumbai-Delhi, Bangalore-Delhi
- Profile: High-volume business corridors with predictable pricing.

**Cluster 2 — Last-Minute Punishers (2 routes)**
- Mean price: Rs.6,207
- Highest last-minute premium: 3.01x
- Steepest price slope: -179 INR per day
- Routes: Chennai-Mumbai, Mumbai-Chennai
- Profile: Extreme last-minute premium; only 2 routes but the strongest signal in the dataset.

**Cluster 3 — Value Routes (7 routes)**
- Mean price: Rs.6,258
- Lowest last-minute premium: 2.18x
- Least steep price slope: -120 INR per day
- Example routes: Bangalore-Hyderabad, Hyderabad-Delhi, Bangalore-Mumbai
- Profile: Prices rise gently near departure; less punishing for last-minute buyers.

### 5.3 Business Segments

Three distinct Business segments were identified:

**Cluster 0 — Delhi Metro Business (6 routes)**
- Lowest mean price: Rs.45,534
- CV: 0.24
- All routes involve Delhi
- Example routes: Bangalore-Delhi, Delhi-Mumbai, Hyderabad-Delhi
- Profile: Delhi is India's most competitive business hub; Business fares here are relatively cheap.

**Cluster 1 — East-South Stable Business (7 routes)**
- Mean price: Rs.53,824
- Lowest CV: 0.14 (very stable)
- Flattest slope: -24 INR per day
- Example routes: Chennai-Hyderabad, Chennai-Kolkata, Hyderabad-Kolkata
- Profile: Thinner corridors, stable pricing year-round.

**Cluster 2 — Premium Mumbai Mixed Business (17 routes)**
- Highest mean price: Rs.54,780
- Highest std: Rs.11,608
- Example routes: All Mumbai routes plus remaining corridors
- Profile: Mumbai routes command premium pricing; broader variation than East-South.

### 5.4 Economy vs Business — Direct Comparison

| Metric | Economy | Business |
|---|---|---|
| Mean last-minute premium | 2.35x | 1.09x |
| Mean CV (volatility) | 0.51 | 0.20 |
| Mean price | Rs.6,517 | Rs.52,708 |
| Segment driver | Behaviour | Geography |
| Best silhouette | 0.328 (k=4) | 0.338 (k=3) |

Key insight: Economy routes vary in HOW they price (behaviour). Business routes vary in WHERE they operate (geography). This is the central finding of the project.

### 5.5 Visual Evidence

- plot_economy_pca.png — 2D projection showing 4 separated Economy segments
- plot_business_pca.png — 2D projection showing 3 separated Business segments
- plot_economy_price_curves.png — Price vs days-left curves fan out dramatically; Last-Minute Punishers (Chennai-Mumbai) diverge steeply
- plot_business_price_curves.png — Business curves stay relatively flat
- plot_economy_vs_business.png — Side-by-side comparison of premium, volatility, and price level
- plot_economy_silhouette.png — Only 1 of 30 routes has negative silhouette (97% assignment confidence)

---

## 6. Discussion

### 6.1 Interpretation of Findings

**Finding 1: Economy pricing is behaviourally diverse; Business pricing is not.**

Economy routes span a wide range of last-minute premiums (2.18x to 3.11x) and volatility (CV 0.42 to 0.59). Business routes, in contrast, cluster tightly around a 1.08-1.12x premium (CV 0.09 to 0.28). This makes business sense: Business travellers typically book through corporate accounts with less price sensitivity, so airlines have little incentive to vary pricing significantly. Economy travellers are highly price-sensitive and shop around, giving airlines strong motivation to use dynamic pricing.

**Finding 2: Chennai-Mumbai is an outlier route with 3.11x last-minute premium.**

The only 2-route cluster in the analysis (Chennai-Mumbai, Mumbai-Chennai) shows the most extreme pricing behaviour. A ticket booked 5 days before departure costs about 3x more than one booked 40+ days out. This is unusual even among Economy routes and suggests either high business demand on this specific corridor or limited direct competition.

**Finding 3: Business segment structure is geographic.**

Delhi Business routes are consistently cheapest, Mumbai routes premium, East-South corridors stable. This geographic pattern reflects route-specific competition and demand. Delhi, as India's largest business hub, has more airlines competing on each route, keeping prices lower. Mumbai routes command premium due to higher corporate demand.

**Finding 4: Economy segment structure is behavioural.**

Economy clusters form around pricing patterns, not geography. Premium Routes, Metro Corridors, Value Routes, and Last-Minute Punishers contain routes from every city. The clustering algorithm grouped routes by HOW they price, not WHERE they go.

### 6.2 Business Implications

**For airlines (revenue management):**
- Last-Minute Punisher routes (Chennai-Mumbai) offer the highest dynamic pricing upside.
- Value Routes have room to increase premium — prices only rise 2.18x despite capacity constraints.
- Business routes could adopt more aggressive dynamic pricing; current premiums (1.08x) leave revenue on the table.

**For OTAs (MakeMyTrip, Booking.com):**
- Build "book early" alerts specifically for Last-Minute Punisher routes.
- For Value Routes, offer flexible booking options since premiums are low.
- Segment marketing campaigns by route type — one message won't fit all.

**For consumers:**
- On Last-Minute Punisher routes, booking early saves up to 68%.
- On Value Routes, waiting until closer to departure costs relatively little.
- Business class pricing is predictable and doesn't reward early booking.

### 6.3 Limitations

1. No calendar dates: The dataset lacks calendar date information, so we analyse booking-window behaviour, not calendar seasonality.
2. Small sample (30 routes): With only 30 routes per class, the Last-Minute Punisher cluster contains just 2 routes. This is a valid signal but not generalizable.
3. Single snapshot: Data is from one source; routes may behave differently on other OTAs.
4. No airline-level breakdown: We clustered routes, not airline-route combinations. Different airlines may price the same route differently.
5. Feature engineering choices: Our 11 features are one way to characterise routes; alternative features (seasonality, day-of-week) are not included.

### 6.4 Future Work

1. Calendar enrichment: Merge with calendar dates to add seasonality features.
2. Real-time pricing: Build a Streamlit dashboard that shows segment labels for any route.
3. Larger dataset: Expand to 100+ routes for more robust cluster separation.
4. Airline-aware clustering: Segment routes AND airlines jointly.
5. Predictive model: Use segments as features to predict future prices.

---

## 7. Conclusion

This project segmented 30 Indian domestic airfare routes into behaviourally distinct groups using K-Means clustering on 11 pricing-behaviour features. We found that Economy and Business classes represent fundamentally different pricing ecosystems:

- Economy routes split into 4 segments driven by pricing behaviour
- Business routes split into 3 segments driven by geography
- Economy prices can rise up to 3.11x for last-minute bookings; Business prices stay flat (max 1.20x)
- Chennai-Mumbai is the dataset's most extreme route, with a 3.11x last-minute premium

These segments provide actionable insights for airlines (revenue management), OTAs (targeted alerts and messaging), and consumers (when to book). The methodology — feature engineering + scaling + clustering + interpretation — is generalizable to any route-based pricing problem.

The project demonstrates that unsupervised learning can extract meaningful business structure from raw transaction data without labels or prior assumptions.

---

## Appendix A — Project Files

All files are available in the project Google Drive folder:

Data:
- airfare_raw.csv — Raw dataset (300,153 rows)
- airfare_cleaned.csv — Cleaned dataset (294,745 rows)
- features_economy.csv — Economy feature table (30 routes)
- features_business.csv — Business feature table (30 routes)
- features_economy_scaled.csv — Scaled features for modeling
- features_business_scaled.csv — Scaled features for modeling
- economy_with_clusters.csv — Economy routes with segment labels
- business_with_clusters.csv — Business routes with segment labels

Plots:
- plot_economy_pca.png
- plot_business_pca.png
- plot_economy_price_curves.png
- plot_business_price_curves.png
- plot_economy_boxplots.png
- plot_business_boxplots.png
- plot_economy_silhouette.png
- plot_economy_vs_business.png

Code:
- Colab notebooks for Days 4-11 (data, cleaning, features, clustering, visualization, report)

---

## Appendix B — Methodology Summary

1. Downloaded 300,153 airfare records from Kaggle via API
2. Cleaned data: removed duplicates, fixed types, trimmed outliers per class
3. Created composite route column (30 unique routes)
4. Split Economy (206,666 rows) and Business (93,487 rows)
5. Engineered 13 pricing-behaviour features per route
6. Dropped low-variance features (11 features remaining per class)
7. Applied log transform to skewed money features
8. Standardized with StandardScaler
9. Ran K-Means for k = 2 to 8, chose k by elbow + silhouette + business sense
10. Economy: k=4, silhouette=0.328
11. Business: k=3, silhouette=0.338
12. Profiled and named each cluster
13. Generated 8 visualizations
14. Wrote this report

---
