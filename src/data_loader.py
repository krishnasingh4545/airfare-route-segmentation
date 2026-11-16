"""
Data Loader & Dataset Generator for Kaggle Flight Price Prediction.
Expanded commercial route network with comprehensive domestic and international corridors.
"""

import os
import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CLEAN_DATASET_PATH = os.path.join(DATA_DIR, "Clean_Dataset.csv")

# Expanded Airlines
AIRLINES = [
    "Indigo", "Air_India", "Vistara", "SpiceJet", "AirAsia", "GO_FIRST",
    "Emirates", "British_Airways", "Singapore_Airlines", "Air_France", "Lufthansa"
]

# Domestic Metros & Leisure/Regional Hubs
DOMESTIC_CITIES = [
    "Delhi", "Mumbai", "Bangalore", "Kolkata", "Hyderabad", "Chennai",
    "Goa", "Pune", "Ahmedabad", "Kochi", "Jaipur", "Srinagar"
]

# International Commercial & Holiday Gateways
INTERNATIONAL_CITIES = [
    "London", "Dubai", "Singapore", "New York", "Paris", "Bangkok", "Tokyo", "Frankfurt"
]

ALL_CITIES = DOMESTIC_CITIES + INTERNATIONAL_CITIES

TIME_SLOTS = ["Early_Morning", "Morning", "Afternoon", "Evening", "Night", "Late_Night"]
STOPS_OPTIONS = ["zero", "one", "two_or_more"]
CLASSES = ["Economy", "Business"]

AIRLINE_BASE_COST = {
    "SpiceJet": 0.88,
    "AirAsia": 0.90,
    "Indigo": 0.96,
    "GO_FIRST": 0.92,
    "Air_India": 1.15,
    "Vistara": 1.25,
    "Emirates": 1.85,
    "British_Airways": 1.95,
    "Singapore_Airlines": 1.90,
    "Air_France": 1.88,
    "Lufthansa": 1.92,
}

# Distance matrix in KM
ROUTE_DISTANCES_KM = {
    # Core Domestic Metros
    ("Delhi", "Mumbai"): 1150,
    ("Delhi", "Bangalore"): 1740,
    ("Delhi", "Kolkata"): 1300,
    ("Delhi", "Hyderabad"): 1250,
    ("Delhi", "Chennai"): 1760,
    ("Delhi", "Goa"): 1510,
    ("Delhi", "Pune"): 1170,
    ("Delhi", "Ahmedabad"): 775,
    ("Delhi", "Kochi"): 2050,
    ("Delhi", "Jaipur"): 240,
    ("Delhi", "Srinagar"): 650,
    ("Mumbai", "Bangalore"): 840,
    ("Mumbai", "Kolkata"): 1660,
    ("Mumbai", "Hyderabad"): 620,
    ("Mumbai", "Chennai"): 1030,
    ("Mumbai", "Goa"): 440,
    ("Mumbai", "Pune"): 120,
    ("Mumbai", "Ahmedabad"): 440,
    ("Mumbai", "Kochi"): 1070,
    ("Mumbai", "Jaipur"): 920,
    ("Mumbai", "Srinagar"): 1670,
    ("Bangalore", "Kolkata"): 1560,
    ("Bangalore", "Hyderabad"): 500,
    ("Bangalore", "Chennai"): 290,
    ("Bangalore", "Goa"): 480,
    ("Bangalore", "Pune"): 730,
    ("Bangalore", "Ahmedabad"): 1230,
    ("Bangalore", "Kochi"): 370,
    ("Kolkata", "Hyderabad"): 1180,
    ("Kolkata", "Chennai"): 1370,
    ("Kolkata", "Goa"): 1730,
    ("Hyderabad", "Chennai"): 510,
    ("Hyderabad", "Goa"): 540,
    ("Chennai", "Goa"): 710,
    ("Chennai", "Kochi"): 560,
    # International Flagship Corridors
    ("Delhi", "London"): 6720,
    ("Mumbai", "London"): 7200,
    ("Delhi", "Dubai"): 2180,
    ("Mumbai", "Dubai"): 1930,
    ("Bangalore", "Dubai"): 2690,
    ("Hyderabad", "Dubai"): 2550,
    ("Bangalore", "Singapore"): 3180,
    ("Chennai", "Singapore"): 2910,
    ("Mumbai", "Singapore"): 3920,
    ("Delhi", "Singapore"): 4150,
    ("Delhi", "Bangkok"): 2920,
    ("Mumbai", "Bangkok"): 3010,
    ("Kolkata", "Bangkok"): 1620,
    ("Delhi", "Paris"): 6580,
    ("Mumbai", "Paris"): 7010,
    ("Delhi", "Frankfurt"): 6120,
    ("Mumbai", "Frankfurt"): 6560,
    ("Delhi", "New York"): 11750,
    ("Mumbai", "New York"): 12540,
    ("Delhi", "Tokyo"): 5840,
    ("Mumbai", "Tokyo"): 6750,
}

def get_route_distance(src, dst):
    if src == dst:
        return 400
    if (src, dst) in ROUTE_DISTANCES_KM:
        return ROUTE_DISTANCES_KM[(src, dst)]
    if (dst, src) in ROUTE_DISTANCES_KM:
        return ROUTE_DISTANCES_KM[(dst, src)]
    return 1450

def generate_flight_data(num_samples: int = 70000, random_seed: int = 42) -> pd.DataFrame:
    """
    Generates rich, comprehensive flight observations across 70+ corridors
    incorporating realistic yield management, class differentials, and carrier distributions.
    """
    np.random.seed(random_seed)
    records = []

    # Assemble comprehensive route list
    route_pool = []
    for k in ROUTE_DISTANCES_KM.keys():
        src, dst = k
        is_intl = src in INTERNATIONAL_CITIES or dst in INTERNATIONAL_CITIES
        route_pool.append((src, dst, is_intl))
        route_pool.append((dst, src, is_intl))

    for idx in range(num_samples):
        src, dst, is_intl = route_pool[np.random.randint(0, len(route_pool))]

        if is_intl:
            airline = np.random.choice(
                ["Air_India", "Vistara", "British_Airways", "Emirates", "Singapore_Airlines", "Air_France", "Lufthansa", "Indigo"],
                p=[0.20, 0.18, 0.14, 0.15, 0.12, 0.08, 0.08, 0.05]
            )
        else:
            airline = np.random.choice(
                ["Indigo", "Air_India", "Vistara", "SpiceJet", "AirAsia", "GO_FIRST"],
                p=[0.38, 0.22, 0.18, 0.10, 0.08, 0.04]
            )

        prefix = {
            "Indigo": "6E", "Air_India": "AI", "Vistara": "UK", "SpiceJet": "SG",
            "AirAsia": "I5", "GO_FIRST": "G8", "British_Airways": "BA", "Emirates": "EK",
            "Singapore_Airlines": "SQ", "Air_France": "AF", "Lufthansa": "LH"
        }.get(airline, "FL")
        flight_code = f"{prefix}-{np.random.randint(100, 9999)}"

        dep_time = np.random.choice(TIME_SLOTS, p=[0.18, 0.25, 0.18, 0.22, 0.13, 0.04])
        arr_time = np.random.choice(TIME_SLOTS, p=[0.15, 0.23, 0.20, 0.23, 0.15, 0.04])

        dist_km = get_route_distance(src, dst)

        # Stop probability
        if dist_km > 5000:
            stops = np.random.choice(STOPS_OPTIONS, p=[0.35, 0.52, 0.13])
        elif dist_km < 600:
            stops = np.random.choice(STOPS_OPTIONS, p=[0.82, 0.17, 0.01])
        else:
            stops = np.random.choice(STOPS_OPTIONS, p=[0.42, 0.52, 0.06])

        # Duration
        base_flight_hours = dist_km / 780.0
        if stops == "zero":
            duration = round(base_flight_hours + np.random.uniform(0.3, 0.7), 2)
        elif stops == "one":
            layover = np.random.uniform(1.5, 5.5)
            duration = round(base_flight_hours * 1.15 + layover, 2)
        else:
            layover = np.random.uniform(4.0, 10.0)
            duration = round(base_flight_hours * 1.3 + layover, 2)

        # Cabin Class
        if airline in ["SpiceJet", "AirAsia", "GO_FIRST"]:
            travel_class = "Economy"
        elif airline == "Indigo":
            travel_class = np.random.choice(["Economy", "Business"], p=[0.90, 0.10])
        else:
            travel_class = np.random.choice(["Economy", "Business"], p=[0.65, 0.35])

        # Days Left (1 to 50)
        days_left = int(np.random.randint(1, 51))

        # Yield Management Pricing
        base_rate = 3.5 if not is_intl else 4.6
        raw_base_fare = max(1800, dist_km * base_rate * AIRLINE_BASE_COST.get(airline, 1.0))

        class_mult = 1.0 if travel_class == "Economy" else np.random.uniform(3.5, 4.9)

        # Non-linear surge curve
        if days_left <= 3:
            surge_mult = np.random.uniform(1.85, 2.65)
        elif days_left <= 7:
            surge_mult = np.random.uniform(1.45, 1.95)
        elif days_left <= 15:
            surge_mult = np.random.uniform(1.15, 1.45)
        elif days_left <= 32:
            surge_mult = np.random.uniform(0.92, 1.12)
        else:
            surge_mult = np.random.uniform(0.85, 1.02)

        time_mult = 1.12 if dep_time in ["Morning", "Evening"] else (0.88 if dep_time in ["Late_Night", "Night"] else 1.0)
        stops_mult = 1.08 if stops == "zero" else (0.95 if stops == "one" else 0.88)

        noise = np.random.normal(1.0, 0.06)
        calc_price = raw_base_fare * class_mult * surge_mult * time_mult * stops_mult * noise
        final_price = int(np.round(np.clip(calc_price, 1100, 240000)))

        records.append({
            "Unnamed: 0": idx,
            "airline": airline,
            "flight": flight_code,
            "source_city": src,
            "departure_time": dep_time,
            "stops": stops,
            "arrival_time": arr_time,
            "destination_city": dst,
            "class": travel_class,
            "duration": duration,
            "days_left": days_left,
            "price": final_price
        })

    return pd.DataFrame(records)

def load_or_generate_dataset(filepath: str = CLEAN_DATASET_PATH, num_samples: int = 70000, force_regenerate: bool = False) -> pd.DataFrame:
    if os.path.exists(filepath) and not force_regenerate:
        print(f"[DataLoader] Found existing dataset at {filepath}. Loading...")
        df = pd.read_csv(filepath)
    else:
        print(f"[DataLoader] Generating expanded Kaggle dataset with {num_samples} records...")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        df = generate_flight_data(num_samples=num_samples, random_seed=42)
        df.to_csv(filepath, index=False)
        print(f"[DataLoader] Saved {len(df)} records to {filepath}.")
    return df

if __name__ == "__main__":
    df = load_or_generate_dataset(force_regenerate=True)
    print("Dataset generated:")
    print(df.info())
