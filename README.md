# Airfare Route Segmentation by Booking-Window Pricing Behaviour

Segmenting 30 Indian domestic airfare routes into behaviourally distinct groups using K-Means clustering on pricing-behaviour features.

## Key Findings

* **Economy routes** split into **4 segments**: Premium, Metro Corridors, Value, and Last-Minute Punishers
* **Business routes** split into **3 segments** driven by geography (Delhi cheap, Mumbai premium, East-South stable)
* **Chennai-Mumbai Economy route** charges **3.11x** more for last-minute bookings
* **Business class prices** stay flat regardless of booking window (max 1.20x premium)
* Economy pricing is **2.5x more volatile** than Business pricing

## Project Overview

This project answers the question: can we automatically segment airfare routes by how their prices behave over the booking window?

The analysis uses **294,745 cleaned records** covering **30 Indian domestic routes** between six major cities (Delhi, Mumbai, Bangalore, Chennai, Hyderabad, Kolkata).

## Methodology

1. **Data acquisition** - Kaggle API for the source dataset
2. **Cleaning** - duplicate removal, type fixing, per-class outlier trim
3. **Feature engineering** - 13 pricing-behaviour features per route
4. **Preprocessing** - log transform + StandardScaler
5. **Clustering** - K-Means with elbow method + silhouette score
6. **Interpretation** - profile clusters, assign business names

## Segments Discovered

### Economy (k=4, silhouette=0.328)

|Segment|Routes|Key Trait|
|-|-|-|
|Premium Routes|11|Highest mean price (Rs.7,198)|
|Metro Corridors|10|Standard high-volume corridors|
|Last-Minute Punishers|2|3.01x last-minute premium|
|Value Routes|7|Lowest last-minute premium (2.18x)|

### Business (k=3, silhouette=0.338)

|Segment|Routes|Key Trait|
|-|-|-|
|Delhi Metro Business|6|Cheapest Business fares (Rs.45,534)|
|East-South Stable Business|7|Most stable (CV=0.14)|
|Premium Mumbai Mixed Business|17|Most expensive (Rs.54,780)|

## Visualizations

### Economy - Price Trajectory by Segment

!\[Economy Price Curves](plots/plot\_economy\_price\_curves.png)

The Last-Minute Punishers (Chennai-Mumbai) diverge sharply as departure approaches.

### Economy vs Business Comparison

!\[Economy vs Business](plots/plot\_economy\_vs\_business.png)

Economy has higher volatility and premium; Business has higher mean price.

### PCA Projections

!\[Economy PCA](plots/plot\_economy\_pca.png)

!\[Business PCA](plots/plot\_business\_pca.png)

## Repository Structure

airfare-route-segmentation/
README.md
LICENSE
.gitignore
data/
business\_with\_clusters.csv
economy\_with\_clusters.csv
features\_business.csv
features\_economy.csv
notebooks/
plots/
\[8 visualization PNGs]
report/
report.md

## Tech Stack

* Python 3 - pandas, NumPy, scikit-learn, matplotlib, seaborn
* Environment - Google Colab
* Data source - Kaggle: Flight Price Cleaned

## How to Run

1. Open Colab and recreate the analysis from the report
2. Or explore report/report.md for the full writeup

## Limitations

* No calendar dates in the dataset - analysis covers booking-window behaviour, not calendar seasonality
* Only 30 routes - the Last-Minute Punisher cluster (2 routes) is a signal but not generalizable
* Single data snapshot - different OTAs may price differently

## Business Impact

* For airlines: Last-Minute Punisher routes have untapped dynamic-pricing upside
* For OTAs: Route-specific 'book early' alerts could improve customer retention
* For consumers: Booking early saves up to 68% on the most extreme routes

## Author

**Krishna Kumar Singh**

## License

MIT License - see LICENSE file for details.

## Acknowledgements

* Dataset: Kaggle - Flight Price Cleaned
* Built as a self-paced 25-day data science project



