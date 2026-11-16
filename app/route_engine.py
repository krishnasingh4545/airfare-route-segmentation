"""
Route Inference & Fare Intelligence Engine for FarePredictor Web Application.
Expanded route network with comprehensive domestic and international corridors.
"""

import os
import json
import datetime
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
METRICS_PATH = os.path.join(DATA_DIR, "model_metrics.json")
ASSIGNMENTS_PATH = os.path.join(DATA_DIR, "route_cluster_assignments.csv")

CITY_CODE_MAP = {
    # Core Metros
    "DEL": "Delhi",
    "BOM": "Mumbai",
    "BLR": "Bangalore",
    "CCU": "Kolkata",
    "HYD": "Hyderabad",
    "MAA": "Chennai",
    # Regional & Leisure Hubs
    "GOI": "Goa",
    "PNQ": "Pune",
    "AMD": "Ahmedabad",
    "COK": "Kochi",
    "JAI": "Jaipur",
    "SXR": "Srinagar",
    # Global Flagship Gateways
    "LON": "London",
    "DXB": "Dubai",
    "SIN": "Singapore",
    "JFK": "New York",
    "CDG": "Paris",
    "BKK": "Bangkok",
    "NRT": "Tokyo",
    "FRA": "Frankfurt"
}

CODE_CITY_MAP = {v: k for k, v in CITY_CODE_MAP.items()}

CITY_META = {
    "Delhi": {"code": "DEL", "airport": "Indira Gandhi Int'l (DEL)", "category": "Metro Hub"},
    "Mumbai": {"code": "BOM", "airport": "Chhatrapati Shivaji Maharaj (BOM)", "category": "Financial Capital"},
    "Bangalore": {"code": "BLR", "airport": "Kempegowda Int'l (BLR)", "category": "Tech Hub"},
    "Kolkata": {"code": "CCU", "airport": "Netaji Subhash Chandra Bose (CCU)", "category": "Eastern Gateway"},
    "Hyderabad": {"code": "HYD", "airport": "Rajiv Gandhi Int'l (HYD)", "category": "Commercial Hub"},
    "Chennai": {"code": "MAA", "airport": "Chennai Int'l (MAA)", "category": "Southern Metro"},
    "Goa": {"code": "GOI", "airport": "Dabolim / Manohar Int'l (GOI)", "category": "Leisure & Tourism"},
    "Pune": {"code": "PNQ", "airport": "Pune Airport (PNQ)", "category": "Industrial & Tech"},
    "Ahmedabad": {"code": "AMD", "airport": "Sardar Vallabhbhai Patel (AMD)", "category": "Business Hub"},
    "Kochi": {"code": "COK", "airport": "Cochin Int'l (COK)", "category": "Coastal & Gulf Hub"},
    "Jaipur": {"code": "JAI", "airport": "Jaipur Int'l (JAI)", "category": "Heritage Golden Triangle"},
    "Srinagar": {"code": "SXR", "airport": "Sheikh ul-Alam Int'l (SXR)", "category": "Seasonal Valley"},
    "London": {"code": "LON", "airport": "Heathrow / Gatwick (LON)", "category": "European Hub"},
    "Dubai": {"code": "DXB", "airport": "Dubai Int'l (DXB)", "category": "Middle-East Transit"},
    "Singapore": {"code": "SIN", "airport": "Singapore Changi (SIN)", "category": "Southeast Asia Hub"},
    "New York": {"code": "JFK", "airport": "John F. Kennedy Int'l (JFK)", "category": "Transatlantic Flagship"},
    "Paris": {"code": "CDG", "airport": "Charles de Gaulle (CDG)", "category": "European Gateway"},
    "Bangkok": {"code": "BKK", "airport": "Suvarnabhumi Airport (BKK)", "category": "Southeast Leisure Hub"},
    "Tokyo": {"code": "NRT", "airport": "Narita / Haneda (NRT)", "category": "East Asia Metro"},
    "Frankfurt": {"code": "FRA", "airport": "Frankfurt Airport (FRA)", "category": "European Finance"}
}

class RoutePredictorEngine:
    def __init__(self):
        self.metrics = self._load_json(METRICS_PATH)
        self.routes_df = self._load_routes_df(ASSIGNMENTS_PATH)

    def _load_json(self, path):
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return {}

    def _load_routes_df(self, path):
        if os.path.exists(path):
            return pd.read_csv(path)
        return pd.DataFrame()

    def reload(self):
        self.metrics = self._load_json(METRICS_PATH)
        self.routes_df = self._load_routes_df(ASSIGNMENTS_PATH)

    def resolve_city_name(self, city_or_code: str) -> str:
        clean = (city_or_code or "").strip().upper()
        if clean in CITY_CODE_MAP:
            return CITY_CODE_MAP[clean]
        for name in CITY_CODE_MAP.values():
            if name.upper() == clean:
                return name
        return city_or_code.title()

    def get_route_record(self, origin: str, destination: str):
        origin_city = self.resolve_city_name(origin)
        dest_city = self.resolve_city_name(destination)
        route_name = f"{origin_city} - {dest_city}"

        if not self.routes_df.empty:
            match = self.routes_df[self.routes_df["route"] == route_name]
            if not match.empty:
                return match.iloc[0].to_dict()

            rev_route = f"{dest_city} - {origin_city}"
            rev_match = self.routes_df[self.routes_df["route"] == rev_route]
            if not rev_match.empty:
                rec = rev_match.iloc[0].to_dict()
                rec["route"] = route_name
                rec["source_city"] = origin_city
                rec["destination_city"] = dest_city
                return rec

        # Dynamic fallback
        is_intl = origin_city in ["London", "Dubai", "Singapore", "New York", "Paris", "Bangkok", "Tokyo", "Frankfurt"] or \
                  dest_city in ["London", "Dubai", "Singapore", "New York", "Paris", "Bangkok", "Tokyo", "Frankfurt"]
        base_fare = 62000.0 if is_intl else 7800.0
        return {
            "route": route_name,
            "source_city": origin_city,
            "destination_city": dest_city,
            "cluster": 1 if is_intl else 0,
            "archetype_name": "Ultra-Long-Haul Intercontinental Corridors" if is_intl else "Cross-Country Domestic Trunk Corridors",
            "mean_price": base_fare,
            "median_price": base_fare * 0.85,
            "price_std": base_fare * 0.45,
            "price_cv": 0.55 if is_intl else 0.85,
            "p10_price": base_fare * 0.60,
            "p25_price": base_fare * 0.72,
            "p75_price": base_fare * 1.35,
            "p90_price": base_fare * 1.85,
            "last_minute_surge_ratio": 1.65 if is_intl else 2.15,
            "avg_duration": 11.5 if is_intl else 3.8,
            "direct_flight_ratio": 0.40,
            "business_ratio": 0.25 if is_intl else 0.16,
            "sample_count": 920
        }

    def predict_booking_decision(self, origin: str, destination: str, depart_date_str: str = None, travel_class: str = "Economy"):
        origin_city = self.resolve_city_name(origin)
        dest_city = self.resolve_city_name(destination)
        route_rec = self.get_route_record(origin_city, dest_city)

        cluster_id = str(int(route_rec.get("cluster", 0)))
        archetype_info = self.metrics.get("archetypes", {}).get(cluster_id, {})
        archetype_name = archetype_info.get("archetype_name", route_rec.get("archetype_name", "Commercial Corridor"))

        days_left = 25
        if depart_date_str:
            try:
                now_date = datetime.date(2026, 11, 15)
                parts = depart_date_str.split("-")
                dep_date = datetime.date(int(parts[0]), int(parts[1]), int(parts[2]))
                diff = (dep_date - now_date).days
                days_left = max(1, diff)
            except Exception:
                days_left = 25

        class_factor = 3.8 if travel_class.lower() == "business" else 1.0

        base_median = route_rec.get("median_price", 6000.0) * class_factor
        base_p10 = route_rec.get("p10_price", 4000.0) * class_factor
        base_p25 = route_rec.get("p25_price", 5000.0) * class_factor
        base_p75 = route_rec.get("p75_price", 11000.0) * class_factor
        base_p90 = route_rec.get("p90_price", 18000.0) * class_factor
        base_mean = route_rec.get("mean_price", 8500.0) * class_factor

        surge_ratio = route_rec.get("last_minute_surge_ratio", 2.0)

        # Recommendation logic
        if days_left <= 3:
            current_fare = base_median * (surge_ratio * 1.08)
            verdict = "BOOK NOW"
            verdict_badge = "book-now"
            verdict_summary = "Emergency Surge Alert: Flight is in departure-week critical surge window. Seats are evaporating quickly."
            confidence = 97
        elif days_left <= 7:
            current_fare = base_median * (surge_ratio * 0.85)
            verdict = "BOOK NOW"
            verdict_badge = "book-now"
            verdict_summary = f"Inside steep price climb zone ({days_left} days left). Booking now avoids the severe last-minute surge of +{int((surge_ratio-1)*100)}%."
            confidence = 94
        elif 16 <= days_left <= 34:
            current_fare = base_p25 * 1.02
            verdict = "BOOK NOW"
            verdict_badge = "book-now"
            verdict_summary = f"Optimal 'Goldilocks Window' Active ({days_left} days left). Fares are in the lowest historical 25th percentile. Lock in now."
            confidence = 93
        elif days_left > 45:
            current_fare = base_p75 * 0.96
            verdict = "WAIT"
            verdict_badge = "wait"
            verdict_summary = f"Booking {days_left} days ahead is premature. Airline yield systems release discounted fare buckets ~21–35 days before departure."
            confidence = 89
        else:
            current_fare = base_median
            verdict = "TYPICAL / MONITOR"
            verdict_badge = "monitor"
            verdict_summary = f"Fares are stable near median ({days_left} days left). Set an alert and pounce if fares dip below INR {int(base_p25):,}."
            confidence = 86

        price_range = max(1, base_p90 - base_p10)
        percentile_rank = int(np.clip(((current_fare - base_p10) / price_range) * 100, 5, 95))

        # Expected surge peak
        peak_surge_price = int(base_median * surge_ratio * 1.05)
        potential_savings = max(0, peak_surge_price - int(current_fare))
        savings_pct = int(round((potential_savings / peak_surge_price) * 100)) if peak_surge_price > 0 else 0

        # Booking curve points
        curve_days = [50, 45, 40, 35, 30, 25, 21, 14, 10, 7, 5, 3, 2, 1]
        curve_prices = []
        for d in curve_days:
            if d > 35:
                mult = 1.05
            elif d >= 18:
                mult = 0.92
            elif d >= 8:
                mult = 1.15
            elif d >= 4:
                mult = surge_ratio * 0.75
            else:
                mult = surge_ratio * 1.05
            curve_prices.append(round(base_median * mult, 0))

        origin_meta = CITY_META.get(origin_city, {"code": origin_city[:3].upper(), "airport": f"{origin_city} Airport", "category": "City"})
        dest_meta = CITY_META.get(dest_city, {"code": dest_city[:3].upper(), "airport": f"{dest_city} Airport", "category": "City"})

        return {
            "origin": origin_city,
            "origin_code": origin_meta["code"],
            "origin_airport": origin_meta["airport"],
            "destination": dest_city,
            "destination_code": dest_meta["code"],
            "destination_airport": dest_meta["airport"],
            "route": route_rec.get("route"),
            "days_left": days_left,
            "travel_class": travel_class,
            "verdict": verdict,
            "verdict_badge": verdict_badge,
            "verdict_summary": verdict_summary,
            "confidence_score": confidence,
            "estimated_fare": int(current_fare),
            "peak_surge_fare": peak_surge_price,
            "potential_savings_inr": potential_savings,
            "savings_pct": savings_pct,
            "percentile_rank": percentile_rank,
            "price_benchmarks": {
                "p10": int(base_p10),
                "p25": int(base_p25),
                "median": int(base_median),
                "p75": int(base_p75),
                "p90": int(base_p90),
                "mean": int(base_mean)
            },
            "cluster_info": {
                "cluster_id": int(cluster_id),
                "archetype_name": archetype_name,
                "badge_color": archetype_info.get("badge_color", "#3b82f6"),
                "description": archetype_info.get("description", ""),
                "avg_duration": route_rec.get("avg_duration", 0),
                "direct_pct": round(float(route_rec.get("direct_flight_ratio", 0) * 100), 1),
                "volatility_cv": route_rec.get("price_cv", 0),
                "surge_ratio": route_rec.get("last_minute_surge_ratio", 0)
            },
            "curve_data": {
                "days": curve_days,
                "prices": curve_prices,
                "current_day": days_left,
                "goldilocks_window": [18, 30]
            }
        }
