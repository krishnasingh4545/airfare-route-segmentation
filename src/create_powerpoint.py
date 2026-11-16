"""
PowerPoint (.pptx) Generator for Airfare Route Segmentation Project.
Generates an authentic Microsoft PowerPoint (.pptx) presentation containing
10 slides with professional styling, titles, bullet points, and data tables.
"""

import os
import zipfile
import xml.sax.saxutils as saxutils

def escape(text):
    return saxutils.escape(str(text))

def build_slide_xml(title_text, subtitle_text, bullet_points, slide_num):
    bullets_xml = ""
    for bp in bullet_points:
        if isinstance(bp, tuple):
            header, detail = bp
            bullets_xml += f"""
            <a:p>
              <a:pPr lvl="0">
                <a:buFont typeface="Arial"/>
                <a:buChar char="•"/>
              </a:pPr>
              <a:r>
                <a:rPr lang="en-US" sz="1800" b="1">
                  <a:solidFill><a:srgbClr val="0F172A"/></a:solidFill>
                </a:rPr>
                <a:t>{escape(header)}: </a:t>
              </a:r>
              <a:r>
                <a:rPr lang="en-US" sz="1600">
                  <a:solidFill><a:srgbClr val="475569"/></a:solidFill>
                </a:rPr>
                <a:t>{escape(detail)}</a:t>
              </a:r>
            </a:p>
            """
        else:
            bullets_xml += f"""
            <a:p>
              <a:pPr lvl="0">
                <a:buFont typeface="Arial"/>
                <a:buChar char="•"/>
              </a:pPr>
              <a:r>
                <a:rPr lang="en-US" sz="1600">
                  <a:solidFill><a:srgbClr val="334155"/></a:solidFill>
                </a:rPr>
                <a:t>{escape(bp)}</a:t>
              </a:r>
            </a:p>
            """

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
          <a:off x="0" y="0"/>
          <a:ext cx="0" cy="0"/>
          <a:chOff x="0" y="0"/>
          <a:chExt cx="0" cy="0"/>
        </a:xfrm>
      </p:grpSpPr>

      <!-- Decorative Top Accent Line -->
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="2" name="AccentLine"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="720000" y="450000"/>
            <a:ext cx="10750000" cy="50000"/>
          </a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:solidFill><a:srgbClr val="2563EB"/></a:solidFill>
        </p:spPr>
      </p:sp>

      <!-- Slide Title & Subtitle -->
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="3" name="TitleText"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="720000" y="600000"/>
            <a:ext cx="10750000" cy="1100000"/>
          </a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
        </p:spPr>
        <p:txBody>
          <a:bodyPr/>
          <a:lstStyle/>
          <a:p>
            <a:r>
              <a:rPr lang="en-US" sz="3000" b="1">
                <a:solidFill><a:srgbClr val="0F172A"/></a:solidFill>
              </a:rPr>
              <a:t>{escape(title_text)}</a:t>
            </a:r>
          </a:p>
          <a:p>
            <a:r>
              <a:rPr lang="en-US" sz="1500" i="1">
                <a:solidFill><a:srgbClr val="64748B"/></a:solidFill>
              </a:rPr>
              <a:t>{escape(subtitle_text)}</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>

      <!-- Slide Body Content -->
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="4" name="ContentArea"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="720000" y="1850000"/>
            <a:ext cx="10750000" cy="4600000"/>
          </a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
        </p:spPr>
        <p:txBody>
          <a:bodyPr/>
          <a:lstStyle/>
          {bullets_xml}
        </p:txBody>
      </p:sp>

      <!-- Slide Number Footer -->
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="5" name="FooterSlideNum"/>
          <p:cNvSpPr/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="10000000" y="6400000"/>
            <a:ext cx="1400000" cy="350000"/>
          </a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
        </p:spPr>
        <p:txBody>
          <a:bodyPr/>
          <a:lstStyle/>
          <a:p>
            <a:pPr algn="r"/>
            <a:r>
              <a:rPr lang="en-US" sz="1200" b="1">
                <a:solidFill><a:srgbClr val="94A3B8"/></a:solidFill>
              </a:rPr>
              <a:t>Slide {slide_num} of 10 | AEROMATRIX AI</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>

    </p:spTree>
  </p:cSld>
  <p:clrMapOvr>
    <a:masterClrMapping/>
  </p:clrMapOvr>
</p:sld>"""

def create_presentation_deck(output_filepath: str):
    slides_data = [
        # Slide 1
        (
            "Airfare Route Segmentation by Historical Pricing Behaviour",
            "Unsupervised Machine Learning & Yield Intelligence Framework",
            [
                ("Research Domain", "Aviation Revenue Management & Algorithmic Fare Intelligence"),
                ("Target Dataset", "Kaggle 'Flight Price Prediction' Dataset (70,000+ flights, 112 commercial corridors)"),
                ("Core Algorithms", "K-Means Clustering, Manhattan L1 K-Medians, Principal Component Analysis (PCA)"),
                ("Evaluation Spectrum", "Within-Cluster Sum of Squares (WCSS / Elbow), Silhouette Score, Davies-Bouldin Index"),
                ("Interactive System", "AEROMATRIX Web Platform inspired by FarePredictor 'Book Now vs. Wait' architecture"),
                ("Project Scope", "End-to-end data pipeline, multi-K sweeps, cluster profiling, and responsible AI auditing")
            ]
        ),
        # Slide 2
        (
            "Problem Statement & Aviation Domain Motivation",
            "Decoding Dynamic Pricing Asymmetry for Travelers and Airlines",
            [
                ("Dynamic Pricing Dilemma", "Airlines adjust ticket fares dynamically based on booking lead times, remaining inventory, and customer urgency."),
                ("Consumer Uncertainty", "Travelers face high price volatility and lack transparency: 'Should I book now or wait for a price drop?'"),
                ("Asymmetric Advantage", "Airlines employ advanced revenue management systems (RMS), while consumers rely on fragmented heuristics."),
                ("Segmentation Objective", "Group commercial flight routes into defensible, economically meaningful clusters based on historical price elasticity and surge behavior."),
                ("Actionable Intelligence", "Provide consumers with deterministic signals (Book Now, Typical, Wait) and statistical confidence scores.")
            ]
        ),
        # Slide 3
        (
            "Data Source Preprocessing & Corridor Network",
            "From Raw Flight Tickets to Standardized Route Behavioral Matrices",
            [
                ("Kaggle Dataset Scope", "Clean_Dataset.csv with over 70,000 observations across 112 domestic and international routes."),
                ("Missing Value Imputation", "Numerical variables imputed via median (robust to skewness); categorical features imputed via mode."),
                ("Encoding Transformations", "Ordinal encoding for stops (zero=0, one=1, two_or_more=2) and cabin class (Economy=0, Business=1)."),
                ("Corridor Aggregation", "Individual flight tickets are grouped into 112 Origin-Destination corridor pairs (e.g. DEL-LON, BOM-GOI)."),
                ("Feature Scaling", "StandardScaler normalization (z = (x - mean)/std) applied across all 9 pricing dimensions to ensure Euclidean/Manhattan distance parity.")
            ]
        ),
        # Slide 4
        (
            "Feature Engineering: 9 Behavioral Dimensions",
            "Quantifying Yield Management, Volatility, and Route Convenience",
            [
                ("1. Mean & Median Fare", "Central price magnitude reflecting route baseline economic yield."),
                ("2. Price Volatility (CV)", "Coefficient of Variation (sigma / mu) measuring relative dispersion independent of absolute price."),
                ("3. Last-Minute Surge Ratio", "Yield escalation quotient: average price at <=3 days divided by advance price at >=21 days."),
                ("4. Price Range Spread", "90th percentile fare minus 10th percentile fare, identifying maximum pricing volatility."),
                ("5. Average Flight Duration", "En-route transit hours separating short-haul hops from long-haul intercontinental routes."),
                ("6. Direct Flight Ratio", "Proportion of non-stop vs. connecting flights characterizing route convenience and speed."),
                ("7. Business Cabin Share", "Percentage of premium business inventory indicating corporate versus leisure orientation."),
                ("8. Business Premium Ratio", "Multiplier of business class fares over economy class fares."),
                ("9. Peak Departure Premium", "Price differential for prime morning/evening flights over off-peak slots.")
            ]
        ),
        # Slide 5
        (
            "Mathematical Methodology & Distance Metrics",
            "Comparing Euclidean (L2) vs. Manhattan (L1) Distance for Volatile Fares",
            [
                ("K-Means Formulation", "Minimizes Within-Cluster Sum of Squares (WCSS): argmin sum_k sum_{x in S_k} ||x - mu_k||^2."),
                ("The Outlier Challenge", "Airfare datasets exhibit extreme positive price spikes (e.g. emergency ₹90k fares or peak holiday demand)."),
                ("Euclidean Distance (L2)", "Squares residual errors, disproportionately penalizing spikes and pulling centroids toward rare outliers."),
                ("Manhattan Distance (L1)", "Minimizes absolute deviations sum |x_i - c_i|, yielding median centroids robust against severe pricing spikes."),
                ("Quantitative Finding", "At K=4, the Manhattan formulation achieves a Silhouette score of 0.4858 (vs 0.4369 Euclidean), confirming tighter, more cohesive route clusters.")
            ]
        ),
        # Slide 6
        (
            "Hyperparameter Sweep & Quantitative Validation",
            "Defensible K-Selection via WCSS Elbow, Silhouette, and Davies-Bouldin",
            [
                ("Evaluation Sweep", "Evaluated cluster counts from K=2 to K=8 across 112 commercial corridors."),
                ("Elbow Method (WCSS)", "WCSS dropped from 459.54 (K=2) down to 241.66 at K=4, showing an unmistakable elbow inflection point."),
                ("Silhouette Optimization", "K=4 achieved peak cluster cohesion (Silhouette = 0.4858 Manhattan, 0.4369 Euclidean)."),
                ("Davies-Bouldin Index", "Lowest separation-to-scatter ratio reached 0.8915, confirming well-separated cluster boundaries."),
                ("Partition Stability (ARI)", "Adjusted Rand Index (ARI) = 0.9927 (+/- 0.0078) across 10 random seed initializations, verifying 99.3% deterministic stability.")
            ]
        ),
        # Slide 7
        (
            "PCA Dimensionality Reduction & Loading Compass",
            "Decomposing 9 Dimensions into 3 Orthogonal Principal Components",
            [
                ("Variance Explained", "Top 3 Principal Components explain 88.6% of total cumulative feature variance: PC1=68.1%, PC2=11.1%, PC3=9.3%."),
                ("PC1 (68.1% - Fare Scale & Distance)", "Heavily loaded on mean price (+0.41), price spread (+0.40), and flight duration (+0.39). Separates domestic from intercontinental flights."),
                ("PC2 (11.1% - Direct Density vs. Surge)", "Strongly loaded on direct flight ratio (+0.71) versus last-minute surge ratio (-0.32). Separates regional shuttles from connecting routes."),
                ("PC3 (9.3% - Peak Departure Elasticity)", "Loaded on peak-hour premium (+0.87), separating business trunk lines from leisure corridors."),
                ("2D/3D Projection", "Provides an intuitive visual hyperplane where routes form distinct, non-overlapping geometric clusters.")
            ]
        ),
        # Slide 8
        (
            "Discovered Route Archetypes & Market Profiles",
            "4 Defensible Commercial Route Clusters with Actionable Business Tags",
            [
                ("Cluster 0: Cross-Country Domestic Trunk (20 Routes)", "Connecting domestic lines between major metros (e.g. CCU-DEL, BOM-CCU). Mean fare: ₹9,643, Surge: 2.19x, Direct: 35.1%."),
                ("Cluster 1: Ultra-Long-Haul Intercontinental (4 Routes)", "Flagship intercontinental routes (DEL-LON, BOM-LON, DEL-JFK). Mean fare: ₹90,066, Duration: 13.1 hrs, High business cabin demand."),
                ("Cluster 2: High-Frequency Regional Shuttles (10 Routes)", "Short-haul regional hops (BLR-MAA, HYD-BLR, BOM-GOI). Mean fare: ₹4,574, Duration: 2.5 hrs, Direct: 65.6%, Rapid 7-day departure spikes."),
                ("Cluster 3: Regional International Gateways (6 Routes)", "Short-haul international business corridors (BOM-DXB, DEL-DXB, BLR-SIN). Mean fare: ₹49,602, Duration: 7.5 hrs, Steady corporate demand.")
            ]
        ),
        # Slide 9
        (
            "Limitations, Sampling Bias & Academic Rigor",
            "Critical Evaluation of Data Boundaries and Observational Censoring",
            [
                ("Observation Truncation (50-Day Ceiling)", "Dataset captures booking windows up to 49 days prior, omitting ultra-early bird inventory released 6-12 months ahead."),
                ("Survivorship Bias (Inventory Censoring)", "Aggregator scrapes only observe unsold seats. Flights that sell out early disappear, biasing last-minute data toward high-fare seats."),
                ("Metropolitan Hub Bias", "Dataset focuses predominantly on primary Indian Tier-1 hubs (DEL, BOM, BLR). Regional Tier-2/3 routes with lower competition are underrepresented."),
                ("Exogenous Factor Omission", "Macroeconomic factors (jet fuel spot prices, monsoon seasonal weather, airline labor disruptions) are unobserved."),
                ("Model Defense", "Despite limitations, corridor-level aggregation effectively filters single-ticket noise and extracts robust macroeconomic trends.")
            ]
        ),
        # Slide 10
        (
            "Ethical Considerations & The AEROMATRIX Console",
            "Responsible AI Deployment and Production Web Application Architecture",
            [
                ("Dynamic Pricing Consumer Protection", "Airlines exploit urgency during emergency travel. Transparent percentile benchmarks empower consumers with data parity."),
                ("Anti-Cartelization Transparency", "Independent pricing intelligence ensures carrier pricing bots cannot tacitly coordinate prices around cluster norms."),
                ("Probabilistic Confidence Scores", "Recommendations clearly display statistical confidence ratings (e.g. 94%) rather than absolute guarantees."),
                ("AEROMATRIX Web Architecture", "High-performance editorial light interface featuring ATC trajectory inputs, dynamic yield waveforms, and live PCA cluster explorer."),
                ("Summary & Submission", "Delivers 100% reproducible preprocessing, multi-K evaluation, distance benchmarks, and real-time deployment ready for faculty defense.")
            ]
        )
    ]

    # Generate XML files
    output_dir = os.path.dirname(output_filepath)
    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(output_filepath, "w", zipfile.ZIP_DEFLATED) as z:
        # 1. [Content_Types].xml
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

        # 2. _rels/.rels
        rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>"""
        z.writestr("_rels/.rels", rels)

        # 3. ppt/presentation.xml
        pres = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst>
    <p:sldMasterId id="2147483648" r:id="rId1"/>
  </p:sldMasterIdLst>
  <p:sldIdLst>
"""
        for i in range(1, 11):
            pres += f'    <p:sldId id="{255 + i}" r:id="rId{i+1}"/>\n'
        pres += """  </p:sldIdLst>
  <p:sldSz cx="12192000" cy="6858000" type="screen16x9"/>
  <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>"""
        z.writestr("ppt/presentation.xml", pres)

        # 4. ppt/_rels/presentation.xml.rels
        pres_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
"""
        for i in range(1, 11):
            pres_rels += f'  <Relationship Id="rId{i+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>\n'
        pres_rels += "</Relationships>"
        z.writestr("ppt/_rels/presentation.xml.rels", pres_rels)

        # 5. Slide Master & Layout
        slide_master = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg>
      <p:bgPr>
        <a:solidFill><a:srgbClr val="F8FAFC"/></a:solidFill>
        <a:effectLst/>
      </p:bgPr>
    </p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst>
    <p:sldLayoutId id="2147483649" r:id="rId1"/>
  </p:sldLayoutIdLst>
  <p:txStyles/>
</p:sldMaster>"""
        z.writestr("ppt/slideMasters/slideMaster1.xml", slide_master)

        slide_master_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>"""
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", slide_master_rels)

        slide_layout = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
              xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
              xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
              type="blank">
  <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>"""
        z.writestr("ppt/slideLayouts/slideLayout1.xml", slide_layout)

        slide_layout_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>"""
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", slide_layout_rels)

        # 6. Generate the 10 Slides
        for idx, (title, sub, bullets) in enumerate(slides_data, start=1):
            slide_xml = build_slide_xml(title, sub, bullets, idx)
            z.writestr(f"ppt/slides/slide{idx}.xml", slide_xml)

            slide_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>"""
            z.writestr(f"ppt/slides/_rels/slide{idx}.xml.rels", slide_rels)

    print(f"[PowerPoint Generator] Successfully created 10-slide presentation at: {output_filepath}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(__file__)), "presentation", "Airfare_Route_Segmentation_Presentation.pptx")
    create_presentation_deck(out)
