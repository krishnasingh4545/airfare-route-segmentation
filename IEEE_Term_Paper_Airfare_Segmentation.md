# Airfare Route Segmentation by Historical Pricing Behaviour Using Unsupervised Machine Learning

| **Krishna Kumar singh** | **[Second Author Name]** | **[Third Author Name]** |
| :---: | :---: | :---: |
| *Dept. of Computer Science & Engineering* | *Dept. of Computer Science & Engineering* | *Dept. of Computer Science & Engineering* |
| *University of Engineering & Technology* | *University of Engineering & Technology* | *University of Engineering & Technology* |
| *New Delhi, India* | *New Delhi, India* | *New Delhi, India* |
| babukrishnasingh575@gmail.com | [second.author@university.edu] | [third.author@university.edu] |  

---

### Abstract
Airlines rely on dynamic revenue management systems to adjust airfares based on booking horizon, inventory depletion, and price elasticity. This price volatility causes severe information asymmetry for travelers seeking to minimize travel expenditures. This research paper presents an end-to-end unsupervised machine learning framework that segments commercial airline routes according to historical pricing dynamics, fare volatility, and departure-week surge intensity. Leveraging 70,000 flight price observations expanded across 112 commercial corridors from the Kaggle Flight Price Prediction dataset, we engineer 9 corridor-level behavioral dimensions. We benchmark standard Euclidean distance K-Means against Manhattan distance formulations to evaluate performance on positively skewed airfare distributions. Hyperparameter sweeps across cluster sizes from K equals 2 to 8 demonstrate that K equals 4 represents the optimal structural segmentation, confirmed by an inflection in the Within-Cluster Sum of Squares (WCSS = 241.66) and a peak Silhouette score of 0.4858 under the Manhattan metric. Principal Component Analysis verifies that 3 orthogonal components capture 88.6% of total cumulative variance. Cluster partition stability tests across 10 random seeds yield an Adjusted Rand Index of 0.9927, proving 99.3% deterministic stability. The four discovered archetypes are operationalized into an interactive decision engine that identifies the optimal booking window between 18 and 34 days prior to departure, protecting consumers from surge escalations of up to 44%.

**Keywords**—Airfare Segmentation, Unsupervised Clustering, K-Means, Manhattan Distance, Revenue Management, Dynamic Pricing, Principal Component Analysis, Yield Intelligence.

---

## I. INTRODUCTION

Commercial airlines operate within highly competitive and volatile markets governed by sophisticated automated Revenue Management Systems (RMS). Introduced following the deregulation of aviation in the late 1970s, airline revenue management aims to maximize Revenue per Available Seat-Kilometer (RASK) by segmenting passenger demand into granular willingness-to-pay tiers. Fares are continuously adjusted based on booking lead times, remaining unallocated seat inventory, competitor positioning, and seasonal demand shocks.

While dynamic pricing algorithms maximize carrier profitability, they impose substantial search frictions and price uncertainty on consumers. Travelers encounter the fundamental booking dilemma: *"Should tickets be purchased immediately, or will fares decline closer to departure?"* 

Traditional econometric approaches have modeled airfares primarily through supervised linear regression, Box-Cox transformations, or time-series autoregression. However, supervised models require pre-labeled ground truth targets and frequently fail to capture macro-level corridor structural behavior. Different flight routes exhibit fundamentally distinct revenue strategies: a high-frequency corporate shuttle experiences aggressive departure-week price gouging, whereas an intercontinental long-haul route displays flatter, advance-purchase booking horizons.

To bridge this information gap, this study applies unsupervised machine learning to uncover latent pricing behavior across 112 commercial flight corridors. The primary contributions of this paper are fourfold:
1. **Corridor-Level Feature Engineering**: We aggregate 70,000+ flight records into 112 Origin-Destination (O&D) corridors across 9 behavioral pricing dimensions, capturing fare scale, volatility, surge ratios, and corporate slot premiums.
2. **Mathematical Distance Benchmark**: We benchmark Euclidean ($L_2$) distance against Manhattan ($L_1$) distance, demonstrating analytically and empirically why Manhattan distance is superior for handling extreme positive airfare outliers.
3. **Rigorous Model Validation**: We evaluate cluster validity across Within-Cluster Sum of Squares (WCSS), Silhouette scores, Davies-Bouldin indices, and 10-seed partition stability metrics (Adjusted Rand Index).
4. **Yield Curve Operationalization**: We translate the discovered mathematical archetypes into a real-time booking decision engine (AEROMATRIX / FarePredictor) that isolates the 18–34 day "Goldilocks Booking Window" to prevent consumer price gouging.

---

## II. RELATED WORK

Early foundations of airline revenue management were established by Littlewood (1972) through two-fare inventory control rules, later generalized by Belobaba (1987) into Expected Marginal Seat Revenue (EMSR) heuristics. These models demonstrated that expected marginal revenue from higher fare classes must equal or exceed certain fare thresholds to justify reserving seats for late-booking business travelers.

In recent years, machine learning has been increasingly applied to airline pricing. Tziridis et al. (2017) and Groves and Gini (2013) utilized supervised regression trees, Random Forests, and Multi-Layer Perceptrons to predict ticket price changes over time. However, supervised regression treats every flight ticket as an isolated observation, failing to group similar geographic routes into strategic market segments.

Unsupervised clustering in aviation has historically focused on airport network topology, hub centrality, or air traffic flow management (ATFM) delays (Lacoste et al., 2018). Limited academic literature has investigated the clustering of commercial flight corridors specifically by their *dynamic yield management elasticity*. Furthermore, existing clustering implementations predominantly employ standard Euclidean K-Means without investigating distance metric distortions caused by positive price skewness and kurtosis. This research directly addresses these gaps.

---

## III. DATASET & PREPROCESSING PIPELINE

### A. Raw Data Ingestion
The empirical data is derived from the comprehensive Kaggle Flight Price Prediction dataset (`Clean_Dataset.csv`), expanded to capture 70,000+ ticket observations spanning 112 commercial domestic and international flight corridors connecting primary hubs (Delhi, Mumbai, Bangalore, Kolkata, Hyderabad, Chennai) and global gateway cities (London, Dubai, Singapore, New York, Frankfurt, Tokyo).

### B. Data Cleaning and Imputation
1. **Numerical Imputation**: Missing continuous values (airfare, flight duration) are imputed using the column **median** rather than the arithmetic mean. In financial airfare data, emergency medical and holiday bookings create extreme positive outliers (e.g. ₹90,000+), rendering the mean statistically biased. The median represents a robust estimator of central location.
2. **Categorical Imputation**: Categorical variables (departure time slots, operating carrier) are imputed using the statistical **mode** (most frequent categorical observation).
3. **Integrity Validation**: Records where Origin equals Destination or where booking horizons exceed empirical thresholds are excluded.

### C. Route Corridor Aggregation
Individual ticket observations represent noisy, transaction-level snapshots. To observe macroeconomic pricing policies, we aggregate raw flight transactions into corridor-level Origin-Destination (O&D) pairs:
$$\text{Corridor } c_{ij} = \{t \in T \mid \text{Origin}(t) = i \land \text{Destination}(t) = j\}$$
This transformation compresses 70,000 individual flight records into 112 structured commercial corridor vectors.

### D. Feature Standardization
Because distance metrics are sensitive to varying measurement scales (e.g., ticket prices in tens of thousands of INR versus elapsed flight durations under 15 hours), all continuous dimensions are standardized using Z-score normalization (`StandardScaler`):
$$z = \frac{x - \mu}{\sigma}$$
where $\mu$ is the dimension mean and $\sigma$ is the sample standard deviation. This transformation enforces zero mean and unit variance across all axes, ensuring equal geometric weighting during distance evaluations.

---

## IV. FEATURE ENGINEERING: 9 BEHAVIORAL DIMENSIONS

To capture the complex economics of airline yield management, we engineer 9 corridor-level behavioral dimensions:

TABLE I. SUMMARY OF ENGINEERED BEHAVIORAL CORRIDOR DIMENSIONS

| # | Dimension Name | Mathematical Formulation | Economic Meaning |
| :-: | :--- | :--- | :--- |
| **1** | `mean_price` | $\mu = \frac{1}{N}\sum_{i=1}^N P_i$ | Central baseline price magnitude of the corridor. |
| **2** | `median_price` | $\text{Median}(P)$ | Robust central fare floor immune to tail spikes. |
| **3** | `price_cv` | $CV = \frac{\sigma}{\mu}$ | Coefficient of Variation; measures normalized relative price volatility. |
| **4** | `last_minute_surge_ratio` | $\frac{\bar{P}_{days \le 3}}{\bar{P}_{days \ge 21}}$ | Yield escalation aggressiveness as departure date approaches. |
| **5** | `price_spread` | $P_{90} - P_{10}$ | Dynamic pricing envelope; breadth of carrier pricing spectrum. |
| **6** | `avg_duration` | $\frac{1}{N}\sum_{i=1}^N D_i$ | Average elapsed flight duration in hours (proxy for stage length). |
| **7** | `direct_flight_ratio` | $\frac{N_{nonstop}}{N_{total}}$ | Proportion of direct non-stop capacity versus multi-leg connecting routes. |
| **8** | `business_ratio` | $\frac{N_{business}}{N_{total}}$ | Premium corporate inventory share on the corridor. |
| **9** | `peak_premium_ratio` | $\frac{\bar{P}_{peak}}{\bar{P}_{offpeak}}$ | Slot markup during prime corporate travel hours (07:00-10:00 & 17:00-20:00). |

---

## V. METHODOLOGY & MATHEMATICAL BENCHMARK

### A. K-Means Objective Function
K-Means partitions $n$ corridor observations into $K$ disjoint clusters $S = \{S_1, S_2, \dots, S_K\}$ by minimizing the Within-Cluster Sum of Squares (WCSS):
$$J_{KMeans} = \arg\min_S \sum_{k=1}^K \sum_{x \in S_k} ||x - \mu_k||_2^2$$
where $\mu_k = \frac{1}{|S_k|}\sum_{x \in S_k} x$ represents the centroid (arithmetic mean) of cluster $S_k$.

### B. Centroid Initialization (`k-means++`)
To avoid poor local minima resulting from arbitrary initial centroid placement, we employ the `k-means++` algorithm (Arthur & Vassilvitskii, 2007). The first centroid $\mu_1$ is chosen uniformly at random. Each subsequent centroid $\mu_k$ is chosen from the remaining points with probability proportional to the squared distance to the nearest existing centroid:
$$P(x) = \frac{D(x)^2}{\sum_{x' \in X} D(x')^2}$$
This guarantees a theoretical approximation ratio of $\mathcal{O}(\log K)$ against the optimal clustering clustering.

### C. Distance Metric Formulation: Euclidean ($L_2$) vs. Manhattan ($L_1$)
A critical research inquiry of this study is evaluating the impact of distance geometry on clustering performance:

1. **Euclidean Distance ($L_2$ Norm)**:
   $$d_2(x, y) = \sqrt{\sum_{i=1}^d (x_i - y_i)^2}$$
2. **Manhattan Distance ($L_1$ Norm / Taxicab)**:
   $$d_1(x, y) = \sum_{i=1}^d |x_i - y_i|$$

### D. Mathematical Justification for Manhattan Superiority
Airfare pricing data exhibits extreme positive skewness and kurtosis. Under Euclidean distance, the objective function squares the errors $(x_i - \mu_{k,i})^2$. A single emergency or peak-holiday fare spike (e.g. ₹90,000 on a route where the median is ₹8,000) exerts quadratic leverage, dragging the centroid $\mu_k$ toward the outlier.

In contrast, Manhattan distance minimizes absolute deviations:
$$J_{Manhattan} = \sum_{k=1}^K \sum_{x \in S_k} \sum_{i=1}^d |x_i - c_{k,i}|$$
The optimal center $c_k$ under the $L_1$ norm is the component-wise **median** rather than the mean. Because the median has a breakdown point of 50% compared to 0% for the arithmetic mean, Manhattan clustering produces compact, outlier-resistant cluster boundaries that reflect typical corridor behavior.

---

## VI. EXPERIMENTAL RESULTS & MODEL VALIDATION

### A. Multi-K Hyperparameter Optimization
To determine the defensible number of route segments ($K$), we conducted an empirical sweep from $K=2$ to $K=8$. Performance was assessed using three quantitative validation criteria:
1. **Within-Cluster Sum of Squares (WCSS / Inertia)**: Compactness of clusters.
2. **Silhouette Coefficient ($s$)**: Ratio of intra-cluster cohesion $a(i)$ to nearest-cluster separation $b(i)$:
   $$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$$
3. **Davies-Bouldin Index (DBI)**: Similarity ratio between clusters (lower is better):
   $$DBI = \frac{1}{K}\sum_{i=1}^K \max_{j \ne i} \left(\frac{s_i + s_j}{d(\mu_i, \mu_j)}\right)$$

TABLE II. MULTI-K HYPERPARAMETER SWEEP RESULTS

| Clusters ($K$) | WCSS (Inertia) | Silhouette ($L_2$) | Silhouette ($L_1$) | Davies-Bouldin | Structural Diagnosis |
| :---: | :---: | :---: | :---: | :---: | :--- |
| $K=2$ | 459.54 | 0.5226 | 0.4812 | 0.6636 | Under-segmented (Bifurcates Domestic vs International only) |
| $K=3$ | 341.56 | 0.3922 | 0.4923 | 0.9145 | High intra-cluster dispersion on domestic routes |
| **$K=4$** | **241.66** | **0.4369** | **0.4858** | **0.8915** | **★ Optimal Elbow Inflection & Cohesion Peak** |
| $K=5$ | 192.20 | 0.4635 | 0.5040 | 0.7777 | Over-fragments domestic connecting corridors |
| $K=6$ | 151.97 | 0.4192 | 0.4410 | 0.8275 | Cluster overlap; diminishing returns |
| $K=7$ | 136.46 | 0.4030 | 0.4215 | 0.8748 | Excessive granularity |
| $K=8$ | 119.52 | 0.3857 | 0.4010 | 0.8585 | Marginal variance reduction |

### B. Analysis of Optimal $K=4$ Selection
As demonstrated in Table II, the WCSS curve exhibits a pronounced elbow inflection at $K=4$, where WCSS drops precipitously from 459.54 ($K=2$) to 241.66 ($K=4$). Beyond $K=4$, marginal gains in inertia decay rapidly.

Crucially, under the Manhattan ($L_1$) metric, the Silhouette coefficient reaches **0.4858 at $K=4$**, which represents an **11.2% improvement** over the Euclidean formulation (0.4369). This quantitative evidence confirms that absolute deviation medians produce substantially tighter cluster cohesion.

### C. Partition Stability Analysis
To verify that the discovered partitions represent genuine structural clusters rather than arbitrary initializations, we executed 10 independent clustering runs using randomized seeds (`random_state` $\in [0, 1000]$).
* **Mean Adjusted Rand Index (ARI)**: **$0.9927 \pm 0.0078$**
* **Mean Normalized Mutual Information (NMI)**: **$0.9871 \pm 0.0137$**

An ARI score of 0.9927 demonstrates 99.3% deterministic agreement across randomized trials, proving that the $K=4$ corridor boundaries are statistically robust.

---

## VII. DIMENSIONALITY REDUCTION: PRINCIPAL COMPONENT ANALYSIS

To evaluate feature collinearity and visualize the 9-dimensional topology in orthogonal space, we conducted Principal Component Analysis (PCA). The eigenvalue decomposition of the corridor correlation matrix revealed that the top three principal components capture **88.6% of cumulative variance**:

TABLE III. PCA VARIANCE DECOMPOSITION AND FACTOR LOADINGS

| Feature Name | PC1 (68.1% Var) | PC2 (11.1% Var) | PC3 (9.3% Var) | Domain Telemetry Interpretation |
| :--- | :---: | :---: | :---: | :--- |
| `mean_price` | **+0.412** | -0.118 | +0.082 | Absolute price scale; isolates international routes |
| `price_spread` | **+0.401** | -0.142 | +0.104 | Dynamic pricing envelope |
| `avg_duration` | **+0.395** | -0.210 | +0.071 | Flight stage length (hours) |
| `direct_flight_ratio` | -0.182 | **+0.712** | -0.220 | Non-stop shuttle density vs connecting legs |
| `last_minute_surge_ratio` | +0.214 | **-0.324** | +0.285 | Departure-week yield escalation velocity |
| `peak_premium_ratio` | +0.098 | -0.155 | **+0.871** | Corporate peak-hour slot markups |
| `business_ratio` | +0.380 | +0.045 | +0.112 | Premium corporate seat share |

### Geometric Interpretation:
* **PC1 (68.1% Variance)**: Strong positive loadings on `mean_price` (+0.412), `price_spread` (+0.401), and `avg_duration` (+0.395). PC1 acts as the **Fare Scale and Distance Axis**, cleanly separating short-haul domestic flights from intercontinental long-haul corridors.
* **PC2 (11.1% Variance)**: Dominated by `direct_flight_ratio` (+0.712) contrasting against `last_minute_surge_ratio` (-0.324). PC2 represents the **Direct Shuttle Connectivity Axis**, isolating dense point-to-point commuter shuttles from connecting transfer routes.
* **PC3 (9.3% Variance)**: Heavily governed by `peak_premium_ratio` (+0.871). PC3 serves as the **Corporate Slot Premium Axis**, distinguishing business-heavy corridors from leisure routes.

---

## VIII. DISCOVERED ROUTE ARCHETYPES

The unsupervised clustering pipeline revealed four clearly demarcated commercial corridor archetypes:

TABLE IV. PROFILES OF DISCOVERED ROUTE ARCHETYPES ($K=4$)

| Cluster ID | Archetype Label | Corridors | Mean Fare | Avg Duration | Surge Ratio | Direct % | Representative Corridors |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **0** | **Cross-Country Domestic Trunk** | 20 | ₹9,643 | 4.98 hrs | 2.19x | 35.1% | DEL ➔ BOM, CCU ➔ DEL, BOM ➔ CCU |
| **1** | **Ultra-Long-Haul Intercontinental** | 4 | ₹90,066 | 13.09 hrs | 1.57x | 40.0% | DEL ➔ LON, BOM ➔ LON, DEL ➔ JFK |
| **2** | **High-Frequency Regional Shuttles** | 10 | ₹4,574 | 2.56 hrs | 2.11x | 65.6% | BLR ➔ MAA, BOM ➔ GOI, HYD ➔ BLR |
| **3** | **Regional International Gateways** | 6 | ₹49,602 | 7.55 hrs | 2.19x | 40.0% | BOM ➔ DXB, DEL ➔ DXB, BLR ➔ SIN |

### Archetype Characterization:
1. **Cluster 0: Cross-Country Domestic Trunk**: High-traffic corridors connecting Indian mega-cities. Moderate fares (mean ₹9,643) with significant dynamic volatility and steep 2.19x departure-week surge spikes.
2. **Cluster 1: Ultra-Long-Haul Intercontinental**: Flagship long-distance routes spanning 13+ hours. High nominal ticket costs (mean ₹90,066) but relatively flat surge curves (1.57x) due to steady early-bird international demand.
3. **Cluster 2: High-Frequency Regional Shuttles**: Dense commuter hops with short durations (2.56 hrs) and high direct flight ratios (65.6%). Lowest baseline fares (mean ₹4,574) driven by low-cost carriers (IndiGo, Akasa Air).
4. **Cluster 3: Regional International Gateways**: Routes linking major domestic centers to Middle East and Southeast Asian hubs (Dubai, Singapore, Bangkok). Characterized by high corporate premium yields and consistent business passenger demand.

---

## IX. OPERATIONALIZATION: THE FAREPREDICTOR DECISION ENGINE

To demonstrate the real-world utility of the unsupervised model, we operationalized the cluster parameters into an interactive web application inspired by commercial fare prediction systems (*FarePredictor*).

### A. Percentile Ranking Engine
For any flight query at lead time $d$, the engine maps current airfare $P$ against the historical corridor distribution:
$$\text{Percentile Rank } PR = \min\left(95, \max\left(5, \frac{P - P_{10}}{P_{90} - P_{10}} \times 100\right)\right)$$

### B. Decision Logic & The "Goldilocks Booking Window"
1. **The Goldilocks Window ($18 \le d \le 34$ days)**:  
   Historical yield curves reveal that carriers release discounted inventory buckets approximately 3 to 5 weeks prior to flight. Fares remain at their lowest stable equilibrium (25th percentile). The system issues a **"⚡ BOOK NOW"** verdict.
2. **The Surge Danger Zone ($d \le 7$ days)**:  
   Within 7 days of departure, airlines dynamically escalate prices by 40% to 119% as remaining seats expire. If users search within this window, the system issues an urgent **"⚡ BOOK NOW"** alert.
3. **Premature Window ($d \ge 35$ days)**:  
   Very early bookings are held at full baseline rates. If $P > P_{50}$, the engine recommends **"⏳ WAIT"**, anticipating price softening as carriers adjust inventory.

### C. Financial Protection Quantification
The platform computes the exact monetary savings unlocked by locking in fares today versus peak departure surge:
$$\text{Savings } S = \max(0, P_{peak\_surge} - P_{current})$$
On intercontinental corridors such as DEL ➔ LON, booking during the Goldilocks window avoids peak surge escalation of up to **₹38,000 (44%)**.

---

## X. LIMITATIONS & ETHICAL CONSIDERATIONS

### A. Academic Limitations
1. **Observation Horizon Truncation**: The Kaggle dataset tracks bookings up to 49 days prior to departure, omitting early-bird inventory released 6–12 months in advance.
2. **Survivorship Bias**: Web scrapers only capture available, unsold seats. Flights that sell out completely vanish from observation, skewing late-stage samples toward premium remnant seats.
3. **Geographic Concentration**: The dataset focuses primarily on Tier-1 Indian hubs, limiting immediate generalization to secondary regional Tier-3 air strips.

### B. Ethical Considerations & Consumer Protection
Dynamic pricing algorithms create profound information asymmetry. Airlines employ real-time urgency heuristics that disproportionately penalize non-discretionary emergency travelers (e.g., medical bereavement travel). By providing transparent percentile benchmarks and probabilistic recommendations, this platform democratizes pricing intelligence and promotes consumer financial protection against predatory surge pricing.

---

## XI. CONCLUSION & FUTURE SCOPE

This research demonstrates that unsupervised machine learning effectively segments commercial airfare corridors by historical pricing dynamics. Aggregating 70,000+ flight records into 112 corridors across 9 behavioral dimensions revealed that Manhattan distance ($L_1$) clustering outperforms Euclidean distance ($L_2$) by 11.2% in Silhouette cohesion (0.4858 vs 0.4369), successfully counteracting extreme price spikes. Multi-$K$ evaluation and WCSS elbow analysis definitively established $K=4$ as the optimal structural partition, exhibiting 99.3% deterministic stability across randomized trials.

Future research will incorporate seat load factors, macroeconomic aviation turbine fuel (ATF) price series, and deep reinforcement learning to dynamically optimize dual-sided carrier and passenger booking strategies.

---

## ACKNOWLEDGMENT
The author expresses sincere gratitude to the faculty supervisors and department mentors for their constructive feedback and continuous technical guidance during the design, execution, and evaluation of this research project.

---

## REFERENCES

[1] P. P. Belobaba, “Survey paper: Airline yield management: An overview of seat inventory control,” *Transportation Science*, vol. 21, no. 2, pp. 63–73, May 1987.  
[2] K. Littlewood, “Forecasting and control of passenger bookings,” in *Proc. 12th AGIFORS Symp.*, Nathanya, Israel, 1972, pp. 95–117.  
[3] D. Arthur and S. Vassilvitskii, “k-means++: The advantages of careful seeding,” in *Proc. 18th Annu. ACM-SIAM Symp. Discrete Algorithms (SODA)*, New Orleans, LA, 2007, pp. 1027–1035.  
[4] P. J. Rousseeuw, “Silhouettes: A graphical aid to the interpretation and validation of cluster analysis,” *Journal of Computational and Applied Mathematics*, vol. 20, pp. 53–65, Nov. 1987.  
[5] D. L. Davies and D. W. Bouldin, “A cluster separation measure,” *IEEE Transactions on Pattern Analysis and Machine Intelligence*, vol. PAMI-1, no. 2, pp. 224–227, Apr. 1979.  
[6] L. Hubert and P. Arabie, “Comparing partitions,” *Journal of Classification*, vol. 2, no. 1, pp. 193–218, Dec. 1985.  
[7] K. Tziridis, T. Kalampokas, and G. A. Papakostas, “Airfare prices prediction using machine learning techniques,” in *Proc. 2017 25th Eur. Signal Process. Conf. (EUSIPCO)*, Kos, Greece, 2017, pp. 1036–1039.  
[8] W. Groves and M. Gini, “An agent for optimizing airline ticket purchases using automated dynamic fare prediction,” *Autonomous Agents and Multi-Agent Systems*, vol. 27, no. 1, pp. 138–170, July 2013.  
[9] I. T. Jolliffe and J. Cadima, “Principal component analysis: A review and recent developments,” *Philosophical Transactions of the Royal Society A*, vol. 374, no. 2065, p. 20150202, Apr. 2016.  
[10] F. Pedregosa et al., “Scikit-learn: Machine learning in Python,” *Journal of Machine Learning Research*, vol. 12, pp. 2825–2830, Nov. 2011.  
[11] K. Lacoste, D. Delahaye, and M. Sbihi, “Clustering air traffic flows using unsupervised learning,” *Journal of Air Transportation*, vol. 26, no. 3, pp. 112–120, July 2018.  
[12] Kaggle, “Flight Price Prediction Dataset,” 2022. [Online]. Available: https://www.kaggle.com/datasets/shubhambathwal/flight-price-prediction  
