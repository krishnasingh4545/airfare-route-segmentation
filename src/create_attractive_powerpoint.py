"""
Executive Presentation (.pptx) Generator for Airfare Route Segmentation Project.
Generates an editorial, high-end white-theme presentation using structured card layouts,
metric callouts, distinct color accents, and clean typography.
"""

import os
import zipfile
import xml.sax.saxutils as saxutils

def escape(text):
    return saxutils.escape(str(text))

def slide_base_xml(slide_content_xml, slide_num, category_tag):
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name=""/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm>
          <a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/>
        </a:xfrm>
      </p:grpSpPr>

      <!-- Background Fill -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="2" name="SlideBg"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="0" y="0"/><a:ext cx="12192000" cy="6858000"/></a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
        </p:spPr>
      </p:sp>

      <!-- Top Accent Bar (Gradient Sapphire & Emerald) -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="3" name="TopAccentBar"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="0" y="0"/><a:ext cx="12192000" cy="70000"/></a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:solidFill><a:srgbClr val="2563EB"/></a:solidFill>
        </p:spPr>
      </p:sp>

      <!-- Category Pill -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="4" name="CategoryPill"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="720000" y="320000"/><a:ext cx="3500000" cy="300000"/></a:xfrm>
          <a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 20000"/></a:avLst></a:prstGeom>
          <a:solidFill><a:srgbClr val="EFF6FF"/></a:solidFill>
          <a:ln w="12700"><a:solidFill><a:srgbClr val="BFDBFE"/></a:solidFill></a:ln>
        </p:spPr>
        <p:txBody>
          <a:bodyPr lIns="90000" tIns="40000" rIns="90000" bIns="40000"/>
          <a:lstStyle/>
          <a:p>
            <a:r>
              <a:rPr lang="en-US" sz="1100" b="1">
                <a:solidFill><a:srgbClr val="2563EB"/></a:solidFill>
              </a:rPr>
              <a:t>{escape(category_tag)}</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>

      <!-- Footer Bar -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="5" name="Footer"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="720000" y="6420000"/><a:ext cx="10752000" cy="320000"/></a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
        </p:spPr>
        <p:txBody>
          <a:bodyPr lIns="0" tIns="0" rIns="0" bIns="0"/>
          <a:lstStyle/>
          <a:p>
            <a:r>
              <a:rPr lang="en-US" sz="1100" b="1"><a:solidFill><a:srgbClr val="64748B"/></a:solidFill></a:rPr>
              <a:t>AEROMATRIX • Airfare Route Segmentation Using Clustering</a:t>
            </a:r>
            <a:r>
              <a:rPr lang="en-US" sz="1100"><a:solidFill><a:srgbClr val="94A3B8"/></a:solidFill></a:rPr>
              <a:t>  |  Faculty Evaluation Deck</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>

      <!-- Slide Number Badge -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="6" name="SlideNumBadge"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="10500000" y="6380000"/><a:ext cx="1000000" cy="280000"/></a:xfrm>
          <a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 20000"/></a:avLst></a:prstGeom>
          <a:solidFill><a:srgbClr val="F1F5F9"/></a:solidFill>
          <a:ln w="9525"><a:solidFill><a:srgbClr val="CBD5E1"/></a:solidFill></a:ln>
        </p:spPr>
        <p:txBody>
          <a:bodyPr lIns="40000" tIns="40000" rIns="40000" bIns="40000"/>
          <a:lstStyle/>
          <a:p>
            <a:pPr algn="ctr"/>
            <a:r>
              <a:rPr lang="en-US" sz="1100" b="1"><a:solidFill><a:srgbClr val="0F172A"/></a:solidFill></a:rPr>
              <a:t>{slide_num} / 10</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>

      {slide_content_xml}

    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>"""

def make_card(x, y, cx, cy, title, desc, bullet_items=None, border_color="E2E8F0", bg_color="F8FAFC", title_color="0F172A", stat_callout=None):
    items_xml = ""
    if bullet_items:
        for b in bullet_items:
            if isinstance(b, tuple):
                h, d = b
                items_xml += f"""
                <a:p>
                  <a:pPr marL="200000" indent="-150000"><a:buFont typeface="Arial"/><a:buChar char="▪"/></a:pPr>
                  <a:r><a:rPr lang="en-US" sz="1300" b="1"><a:solidFill><a:srgbClr val="0F172A"/></a:solidFill></a:rPr><a:t>{escape(h)}: </a:t></a:r>
                  <a:r><a:rPr lang="en-US" sz="1250"><a:solidFill><a:srgbClr val="475569"/></a:solidFill></a:rPr><a:t>{escape(d)}</a:t></a:r>
                </a:p>"""
            else:
                items_xml += f"""
                <a:p>
                  <a:pPr marL="200000" indent="-150000"><a:buFont typeface="Arial"/><a:buChar char="▪"/></a:pPr>
                  <a:r><a:rPr lang="en-US" sz="1300"><a:solidFill><a:srgbClr val="334155"/></a:solidFill></a:rPr><a:t>{escape(b)}</a:t></a:r>
                </a:p>"""

    stat_xml = ""
    if stat_callout:
        val, sub = stat_callout
        stat_xml = f"""
        <a:p>
          <a:r><a:rPr lang="en-US" sz="2600" b="1"><a:solidFill><a:srgbClr val="2563EB"/></a:solidFill></a:rPr><a:t>{escape(val)}</a:t></a:r>
        </a:p>
        <a:p>
          <a:r><a:rPr lang="en-US" sz="1100" b="1"><a:solidFill><a:srgbClr val="64748B"/></a:solidFill></a:rPr><a:t>{escape(sub)}</a:t></a:r>
        </a:p>"""

    return f"""
    <p:sp>
      <p:nvSpPr><p:cNvPr id="{int(x/1000 + y/1000)}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
      <p:spPr>
        <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
        <a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 8000"/></a:avLst></a:prstGeom>
        <a:solidFill><a:srgbClr val="{bg_color}"/></a:solidFill>
        <a:ln w="15875"><a:solidFill><a:srgbClr val="{border_color}"/></a:solidFill></a:ln>
      </p:spPr>
      <p:txBody>
        <a:bodyPr lIns="200000" tIns="180000" rIns="200000" bIns="180000"/>
        <a:lstStyle/>
        {stat_xml}
        <a:p>
          <a:r><a:rPr lang="en-US" sz="1600" b="1"><a:solidFill><a:srgbClr val="{title_color}"/></a:solidFill></a:rPr><a:t>{escape(title)}</a:t></a:r>
        </a:p>
        <a:p>
          <a:r><a:rPr lang="en-US" sz="1250"><a:solidFill><a:srgbClr val="64748B"/></a:solidFill></a:rPr><a:t>{escape(desc)}</a:t></a:r>
        </a:p>
        <a:p><a:endParaRPr lang="en-US" sz="600"/></a:p>
        {items_xml}
      </p:txBody>
    </p:sp>"""

def make_title_block(title, subtitle):
    return f"""
    <p:sp>
      <p:nvSpPr><p:cNvPr id="999"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
      <p:spPr>
        <a:xfrm><a:off x="720000" y="700000"/><a:ext cx="10752000" cy="950000"/></a:xfrm>
        <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
      </p:spPr>
      <p:txBody>
        <a:bodyPr lIns="0" tIns="0" rIns="0" bIns="0"/>
        <a:lstStyle/>
        <a:p>
          <a:r><a:rPr lang="en-US" sz="2600" b="1"><a:solidFill><a:srgbClr val="0F172A"/></a:solidFill></a:rPr><a:t>{escape(title)}</a:t></a:r>
        </a:p>
        <a:p>
          <a:r><a:rPr lang="en-US" sz="1350" i="1"><a:solidFill><a:srgbClr val="475569"/></a:solidFill></a:rPr><a:t>{escape(subtitle)}</a:t></a:r>
        </a:p>
      </p:txBody>
    </p:sp>"""

def generate_full_deck():
    slides = []

    # Slide 1: Cover
    s1_content = make_title_block(
        "Airfare Route Segmentation by Historical Pricing Behaviour",
        "An Unsupervised Machine Learning Framework for Airline Revenue Management & Dynamic Pricing"
    )
    s1_content += make_card(720000, 1850000, 3400000, 4200000,
        "70,000+ Observations", "Clean Kaggle dataset observations across Indian metros and global transit hubs.",
        [("Dataset", "Kaggle Flight Price Prediction"), ("Features", "11 raw attributes -> 9 corridor dimensions")],
        border_color="BFDBFE", bg_color="F8FAFC", title_color="2563EB", stat_callout=("70,000+", "FLIGHT TICKETS")
    )
    s1_content += make_card(4400000, 1850000, 3400000, 4200000,
        "112 Commercial Corridors", "Aggregated corridor network spanning domestic trunks, leisure express, and intercontinental lines.",
        [("Metros Covered", "DEL, BOM, BLR, CCU, HYD, MAA"), ("Global Flagships", "London, Dubai, New York, Singapore, Paris")],
        border_color="A7F3D0", bg_color="F8FAFC", title_color="059669", stat_callout=("112", "COMMERCIAL CORRIDORS")
    )
    s1_content += make_card(8080000, 1850000, 3400000, 4200000,
        "K=4 Cluster Structure", "Validated optimal partitioning using WCSS Elbow, Silhouette, and Davies-Bouldin metrics.",
        [("Algorithms", "K-Means L2 & Manhattan L1 K-Medians"), ("Validation", "ARI = 0.9927 (99.3% Deterministic)")],
        border_color="C7D2FE", bg_color="F8FAFC", title_color="4F46E5", stat_callout=("K = 4", "DEFENSIBLE CLUSTERS")
    )
    slides.append((s1_content, 1, "EXECUTIVE PRESENTATION • AIRFARE PRICING AI"))

    # Slide 2: Problem Statement
    s2_content = make_title_block(
        "Problem Statement: Airline Dynamic Pricing Volatility",
        "Understanding Market Asymmetry and the 'Book Now vs. Wait' Dilemma"
    )
    s2_content += make_card(720000, 1850000, 5200000, 4200000,
        "The Airline Perspective: Yield Escalation",
        "How airline revenue management systems (RMS) optimize profits dynamically:",
        [
            ("Inventory Bucketing", "Seats are partitioned into non-linear pricing buckets that escalate as departure date approaches."),
            ("Urgency Exploitation", "Travelers booking in the final 7 days exhibit high price-inelasticity, triggering up to 2.6x surge multipliers."),
            ("Algorithmic Asymmetry", "Carriers employ automated pricing engines while travelers rely on guesswork and fragmented rules of thumb.")
        ],
        border_color="FED7AA", bg_color="FFFBEB", title_color="D97706"
    )
    s2_content += make_card(6240000, 1850000, 5200000, 4200000,
        "The Traveler's Solution: Segmented Intelligence",
        "Empowering consumers with statistical corridor profiling:",
        [
            ("Corridor Segmentation", "Classify flight routes into distinct volatility archetypes rather than treating all flights identically."),
            ("Goldilocks Window", "Pinpoint the historical low-fare window (18–34 days out) before surge triggers."),
            ("Deterministic Signals", "Deliver high-confidence recommendations (Book Now, Typical, Wait) with percentile gauges.")
        ],
        border_color="A7F3D0", bg_color="ECFDF5", title_color="059669"
    )
    slides.append((s2_content, 2, "DOMAIN MOTIVATION • PROBLEM STATEMENT"))

    # Slide 3: Preprocessing Pipeline
    s3_content = make_title_block(
        "Data Source Preparation & Network Topology",
        "Transforming 70,000+ Raw Flight Observations into Standardized Route Matrices"
    )
    s3_content += make_card(720000, 1850000, 3400000, 4200000,
        "01. Imputation & Cleaning",
        "Ensuring complete data integrity:",
        [
            ("Median Numerical Fill", "Robust to positive fare skewness; replaces missing fare and duration values."),
            ("Mode Categorical Fill", "Replaces missing airline and time slots with modal frequencies."),
            ("Noise Filtering", "Clips anomalies and validates origin != destination.")
        ],
        border_color="BFDBFE", bg_color="F8FAFC", title_color="2563EB"
    )
    s3_content += make_card(4400000, 1850000, 3400000, 4200000,
        "02. Feature Encoding",
        "Mapping categorical variables to numerical space:",
        [
            ("Ordinal Stop Mapping", "zero=0, one=1, two_or_more=2 reflecting layover inconvenience."),
            ("Cabin Class Encoding", "Economy=0, Business=1 capturing premium yield tiers."),
            ("Temporal Windows", "Flags last-minute (days<=3) and early-bird (days>=21).")
        ],
        border_color="E2E8F0", bg_color="F8FAFC", title_color="0F172A"
    )
    s3_content += make_card(8080000, 1850000, 3400000, 4200000,
        "03. StandardScaler Scaling",
        "Normalizing disparate feature scales:",
        [
            ("Z-Score Formula", "z = (x - mean) / std ensures zero mean and unit variance."),
            ("Scale Parity", "Prevents ₹90,000 fares from dominating 2.5-hour durations in distance metrics."),
            ("Clustering Ready", "Produces standardized matrix X across 112 corridors.")
        ],
        border_color="A7F3D0", bg_color="F8FAFC", title_color="059669"
    )
    slides.append((s3_content, 3, "DATA PREPARATION • ETL PIPELINE"))

    # Slide 4: Feature Engineering
    s4_content = make_title_block(
        "Feature Engineering: 9 Behavioral Pricing Dimensions",
        "Capturing Macroeconomic Scale, Volatility, and Convenience across Corridors"
    )
    s4_content += make_card(720000, 1850000, 3400000, 4200000,
        "Pillar 1: Price Scale & Spread",
        "Quantifying absolute baseline cost:",
        [
            ("mean_price", "Corridor baseline average fare."),
            ("median_price", "Outlier-resistant central price point."),
            ("price_spread", "Absolute spread (P90 - P10) measuring total price envelope.")
        ],
        border_color="BFDBFE", bg_color="F8FAFC", title_color="2563EB"
    )
    s4_content += make_card(4400000, 1850000, 3400000, 4200000,
        "Pillar 2: Volatility & Surge Velocity",
        "Measuring dynamic pricing aggression:",
        [
            ("price_cv", "Coefficient of Variation (sigma / mu) measuring relative volatility."),
            ("last_minute_surge_ratio", "Price ratio at <=3 days vs >=21 days (yield escalation speed)."),
            ("peak_premium_ratio", "Markup for prime morning/evening departure slots.")
        ],
        border_color="FED7AA", bg_color="F8FAFC", title_color="D97706"
    )
    s4_content += make_card(8080000, 1850000, 3400000, 4200000,
        "Pillar 3: Route Transit & Service",
        "Reflecting convenience and passenger mix:",
        [
            ("avg_duration", "Mean flight duration separating regional from long-haul."),
            ("direct_flight_ratio", "Percentage of non-stop flights on corridor."),
            ("business_ratio", "Proportion of corporate premium seat capacity.")
        ],
        border_color="A7F3D0", bg_color="F8FAFC", title_color="059669"
    )
    slides.append((s4_content, 4, "FEATURE ENGINEERING • CORRIDOR METRICS"))

    # Slide 5: Distance Benchmark
    s5_content = make_title_block(
        "Distance Metric Benchmark: Euclidean (L2) vs. Manhattan (L1)",
        "Overcoming Severe Outlier Distortion in Volatile Airfare Distributions"
    )
    s5_content += make_card(720000, 1850000, 5200000, 4200000,
        "Euclidean Distance (L2 Norm)",
        "Standard K-Means formulation: d(x, mu) = sqrt(sum (x_i - mu_i)^2)",
        [
            ("Squared Error Penalty", "Squaring large errors gives disproportionate leverage to rare, extreme fare spikes (e.g. ₹95,000 tickets)."),
            ("Centroid Pull", "Outliers artificially shift cluster centroids away from representative corridor patterns."),
            ("Validation Result", "Achieves Silhouette score of 0.4369 at K=4.")
        ],
        border_color="CBD5E1", bg_color="F8FAFC", title_color="475569"
    )
    s5_content += make_card(6240000, 1850000, 5200000, 4200000,
        "Manhattan Distance (L1 Norm) ★ Winner",
        "K-Medians formulation: d(x, c) = sum |x_i - c_i|",
        [
            ("Linear Residual Growth", "Evaluates absolute differences, maintaining equal penalty per unit deviation."),
            ("Median Robustness", "Component-wise medians resist price spikes, producing tighter and more interpretable clusters."),
            ("Empirical Superiority", "Achieves Silhouette score of 0.4858 at K=4 (+11.2% higher cluster cohesion).")
        ],
        border_color="A7F3D0", bg_color="ECFDF5", title_color="059669"
    )
    slides.append((s5_content, 5, "MATHEMATICAL METHODOLOGY • DISTANCE METRICS"))

    # Slide 6: Multi-K Sweep
    s6_content = make_title_block(
        "Hyperparameter Sweep & Quantitative Model Validation",
        "Defensible Selection of K=4 via WCSS, Silhouette & Davies-Bouldin Metrics"
    )
    s6_content += make_card(720000, 1850000, 5200000, 4200000,
        "Multi-K Evaluation Spectrum",
        "Rigorous benchmark across cluster counts K=2 through K=8:",
        [
            ("K=2 (WCSS: 459.54)", "Under-segmented binary partition (Domestic vs. International)."),
            ("K=3 (WCSS: 341.56)", "High intra-cluster dispersion; merges regional shuttles with trunks."),
            ("K=4 (WCSS: 241.66) ★", "Optimal inflection point: Silhouette = 0.4858, Davies-Bouldin = 0.8915."),
            ("K=5+ (Diminishing Returns)", "Fragments domestic corridors into redundant micro-groups.")
        ],
        border_color="BFDBFE", bg_color="EFF6FF", title_color="2563EB"
    )
    s6_content += make_card(6240000, 1850000, 5200000, 4200000,
        "Partition Stability Verification",
        "Testing reproducibility across 10 random seed initializations:",
        [
            ("Mean ARI: 0.9927 (+/- 0.0078)", "Adjusted Rand Index verifies 99.3% deterministic agreement across runs."),
            ("Mean NMI: 0.9871 (+/- 0.0137)", "Normalized Mutual Information confirms mutual information preservation."),
            ("Academic Conclusion", "The 4-cluster structure is statistically defensible, reproducible, and invariant to initialization.")
        ],
        border_color="A7F3D0", bg_color="ECFDF5", title_color="059669", stat_callout=("0.9927", "ADJUSTED RAND INDEX (ARI)")
    )
    slides.append((s6_content, 6, "HYPERPARAMETER SWEEP • VALIDATION"))

    # Slide 7: PCA Dimensionality Reduction
    s7_content = make_title_block(
        "PCA Dimensionality Reduction & Loading Compass",
        "Capturing 88.6% Total Cumulative Variance Across 3 Orthogonal Components"
    )
    s7_content += make_card(720000, 1850000, 3400000, 4200000,
        "PC1: 68.1% Variance",
        "Fare Magnitude & Flight Distance:",
        [
            ("mean_price (+0.41)", "Primary driver of PC1 position."),
            ("price_spread (+0.40)", "Dispersion across fare buckets."),
            ("avg_duration (+0.39)", "Separates short domestic from intercontinental flights.")
        ],
        border_color="BFDBFE", bg_color="F8FAFC", title_color="2563EB", stat_callout=("68.1%", "PC1 VARIANCE EXPLAINED")
    )
    s7_content += make_card(4400000, 1850000, 3400000, 4200000,
        "PC2: 11.1% Variance",
        "Direct Density vs. Volatility:",
        [
            ("direct_flight_ratio (+0.71)", "High-density direct shuttle corridor index."),
            ("surge_ratio (-0.32)", "Inversely loaded against last-minute surge velocity."),
            ("Discriminator", "Isolates point-to-point routes from connecting lines.")
        ],
        border_color="A7F3D0", bg_color="F8FAFC", title_color="059669", stat_callout=("11.1%", "PC2 VARIANCE EXPLAINED")
    )
    s7_content += make_card(8080000, 1850000, 3400000, 4200000,
        "PC3: 9.3% Variance",
        "Departure Elasticity:",
        [
            ("peak_premium (+0.87)", "Reflects morning/evening business flight willingness-to-pay."),
            ("Cumulative Total: 88.6%", "Over 88% of 9D space captured in 3 dimensions."),
            ("Visual Hyperplane", "Clean 2D/3D scatter visualization without information loss.")
        ],
        border_color="C7D2FE", bg_color="F8FAFC", title_color="4F46E5", stat_callout=("88.6%", "TOTAL 3D VARIANCE")
    )
    slides.append((s7_content, 7, "PCA REDUCTION • LOADING COMPASS"))

    # Slide 8: Discovered Archetypes
    s8_content = make_title_block(
        "Discovered Commercial Route Archetypes",
        "4 Defensible Market Profiles Extracted via Unsupervised Clustering"
    )
    s8_content += make_card(720000, 1850000, 5200000, 2000000,
        "Cluster 0: Cross-Country Domestic Trunk",
        "Connecting & trunk lines between major Indian metros (DEL-BOM, CCU-DEL, BOM-CCU).",
        [("Metrics", "Mean: ₹9,643 | Duration: 4.98 hrs | Surge: 2.19x | Direct: 35.1%")],
        border_color="FED7AA", bg_color="FFFBEB", title_color="D97706"
    )
    s8_content += make_card(6240000, 1850000, 5200000, 2000000,
        "Cluster 1: Ultra-Long-Haul Intercontinental",
        "Flagship transatlantic/intercontinental corridors (DEL-LON, BOM-LON, DEL-JFK).",
        [("Metrics", "Mean: ₹90,066 | Duration: 13.09 hrs | Surge: 1.57x | High Premium Share")],
        border_color="C7D2FE", bg_color="EEF2FF", title_color="4F46E5"
    )
    s8_content += make_card(720000, 4000000, 5200000, 2000000,
        "Cluster 2: High-Frequency Regional Shuttles",
        "Short-haul hops between neighboring economic centers (BLR-MAA, BOM-GOI, HYD-BLR).",
        [("Metrics", "Mean: ₹4,574 | Duration: 2.56 hrs | Direct: 65.6% | Low-Cost Carrier Base")],
        border_color="A7F3D0", bg_color="ECFDF5", title_color="059669"
    )
    s8_content += make_card(6240000, 4000000, 5200000, 2000000,
        "Cluster 3: Regional International Gateways",
        "Short-haul international business lines (BOM-DXB, DEL-DXB, BLR-SIN, DEL-BKK).",
        [("Metrics", "Mean: ₹49,602 | Duration: 7.55 hrs | Direct: 40.0% | Steady Corporate Yield")],
        border_color="BAE6FD", bg_color="F0F9FF", title_color="0284C7"
    )
    slides.append((s8_content, 8, "CLUSTER PROFILING • MARKET ARCHETYPES"))

    # Slide 9: Limitations & Bias
    s9_content = make_title_block(
        "Documented Limitations, Sampling Biases & Academic Rigor",
        "Critical Evaluation of Observational Boundaries and Data Censoring"
    )
    s9_content += make_card(720000, 1850000, 5200000, 2000000,
        "1. Observation Horizon Truncation",
        "The Kaggle dataset records fares up to 49 days prior, omitting ultra-early bird inventory released 6-12 months ahead.",
        [("Impact", "Early-stage yield exploration is truncated, focusing analysis on the final 7-week trajectory.")],
        border_color="FED7AA", bg_color="F8FAFC", title_color="D97706"
    )
    s9_content += make_card(6240000, 1850000, 5200000, 2000000,
        "2. Survivorship & Censoring Bias",
        "Scrapes only record available unsold seats. Completely sold-out flights disappear from the dataset.",
        [("Impact", "Departure-week fares are biased toward either expensive unsold premium seats or distressed inventory.")],
        border_color="FED7AA", bg_color="F8FAFC", title_color="D97706"
    )
    s9_content += make_card(720000, 4000000, 5200000, 2000000,
        "3. Metropolitan Hub Concentration",
        "Dataset concentrates predominantly on primary Indian Tier-1 hubs (Delhi, Mumbai, Bangalore).",
        [("Impact", "Regional Tier-2/Tier-3 routes with monopolistic airline pricing may exhibit higher surge sensitivity.")],
        border_color="CBD5E1", bg_color="F8FAFC", title_color="475569"
    )
    s9_content += make_card(6240000, 4000000, 5200000, 2000000,
        "4. Exogenous Variable Omission",
        "Aviation fuel (ATF) price shocks, seasonal monsoon weather, and holiday demand surges are unobserved.",
        [("Defense", "Corridor-level aggregation dampens transient ticket noise and isolates structural yield behaviors.")],
        border_color="CBD5E1", bg_color="F8FAFC", title_color="475569"
    )
    slides.append((s9_content, 9, "ACADEMIC RIGOR • LIMITATIONS & BIAS"))

    # Slide 10: Ethics & Web Deployment
    s10_content = make_title_block(
        "Ethical Considerations & AEROMATRIX Web Deployment",
        "Deploying Responsible AI for Consumer Dynamic Pricing Protection"
    )
    s10_content += make_card(720000, 1850000, 5200000, 4200000,
        "Ethical AI & Consumer Protection",
        "Counteracting automated dynamic pricing exploitation:",
        [
            ("Asymmetry Leveling", "Transparent percentile gauges (P10, Median, P90) equip travelers with data parity against airline algorithms."),
            ("Emergency Route Protection", "Identifies predatory surge pricing on captive corridors (bereavement, medical emergencies)."),
            ("Anti-Cartelization Protocol", "Independent pricing intelligence prevents carrier algorithms from coordinating prices around cluster norms."),
            ("Statistical Transparency", "Recommendations explicitly display confidence ratings (e.g. 94%) rather than absolute guarantees.")
        ],
        border_color="A7F3D0", bg_color="ECFDF5", title_color="059669"
    )
    s10_content += make_card(6240000, 1850000, 5200000, 4200000,
        "AEROMATRIX Web Platform Architecture",
        "Production-grade editorial light travel intelligence console:",
        [
            ("ATC Flight Strip Input", "Interactive origin/destination selector with instant vector inversion (⇄)."),
            ("Real-Time Verdict Signal", "Deterministic 'Book Now vs. Wait' advice powered by historical percentile ranking."),
            ("Yield Waveform Visualization", "Interactive chart highlighting the 18-34 day Goldilocks booking window."),
            ("PCA Vector Explorer", "Real-time 2D scatter plot spotlighting any of the 112 commercial corridors.")
        ],
        border_color="BFDBFE", bg_color="EFF6FF", title_color="2563EB"
    )
    slides.append((s10_content, 10, "RESPONSIBLE AI • PLATFORM ARCHITECTURE"))

    return slides

def build_attractive_pptx(output_filepath: str):
    slides = generate_full_deck()
    output_dir = os.path.dirname(output_filepath)
    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(output_filepath, "w", zipfile.ZIP_DEFLATED) as z:
        # [Content_Types].xml
        content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
"""
        for i in range(1, 11):
            content_types += f'  <Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>\n'
        content_types += "</Types>"
        z.writestr("[Content_Types].xml", content_types)

        # _rels/.rels
        rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>"""
        z.writestr("_rels/.rels", rels)

        # ppt/presentation.xml
        pres = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>
  <p:sldIdLst>
"""
        for i in range(1, 11):
            pres += f'    <p:sldId id="{255 + i}" r:id="rId{i+1}"/>\n'
        pres += """  </p:sldIdLst>
  <p:sldSz cx="12192000" cy="6858000" type="screen16x9"/>
  <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>"""
        z.writestr("ppt/presentation.xml", pres)

        # ppt/_rels/presentation.xml.rels
        pres_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
"""
        for i in range(1, 11):
            pres_rels += f'  <Relationship Id="rId{i+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>\n'
        pres_rels += "</Relationships>"
        z.writestr("ppt/_rels/presentation.xml.rels", pres_rels)

        # Slide Master & Layout
        slide_master = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
  <p:txStyles/>
</p:sldMaster>"""
        z.writestr("ppt/slideMasters/slideMaster1.xml", slide_master)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>""")

        slide_layout = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
              xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
              xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
              type="blank">
  <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>"""
        z.writestr("ppt/slideLayouts/slideLayout1.xml", slide_layout)
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>""")

        # Add the 10 slides
        for idx, (content, s_num, cat) in enumerate(slides, start=1):
            slide_xml = slide_base_xml(content, s_num, cat)
            z.writestr(f"ppt/slides/slide{idx}.xml", slide_xml)
            z.writestr(f"ppt/slides/_rels/slide{idx}.xml.rels", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>""")

    print(f"[PowerPoint Generator] Successfully created 10-slide executive white-theme deck at: {output_filepath}")

if __name__ == "__main__":
    out_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "presentation", "Airfare_Route_Segmentation_Presentation.pptx")
    build_attractive_pptx(out_path)
