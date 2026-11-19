"""
Flask Web Application for FarePredictor & Airfare Route Segmentation Intelligence.
Provides interactive UI and REST API for route clustering, 'Book Now vs. Wait' decisions,
PCA visualization, and unsupervised learning academic model evaluation.
"""

import os
import sys
from flask import Flask, render_template, request, jsonify

# Add parent directory and src to path
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(CURRENT_DIR)
sys.path.append(os.path.join(PARENT_DIR, "src"))

from route_engine import RoutePredictorEngine

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
engine = RoutePredictorEngine()

@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/")
def index():
    # Support query params just like FarePredictor: ?from=DEL&to=LON&depart=2026-11-26&return=2026-11-28
    from_city = request.args.get("from", "DEL")
    to_city = request.args.get("to", "LON")
    depart_date = request.args.get("depart", "2026-11-26")
    return_date = request.args.get("return", "2026-11-28")
    travel_class = request.args.get("class", "Economy")

    initial_prediction = engine.predict_booking_decision(
        origin=from_city,
        destination=to_city,
        depart_date_str=depart_date,
        travel_class=travel_class
    )

    return render_template(
        "index.html",
        initial_prediction=initial_prediction,
        from_city=from_city,
        to_city=to_city,
        depart_date=depart_date,
        return_date=return_date,
        travel_class=travel_class,
        metrics=engine.metrics
    )

@app.route("/presentation")
def presentation():
    return render_template("presentation.html", metrics=engine.metrics)

@app.route("/download/pptx")
def download_pptx():
    pptx_path = os.path.join(PARENT_DIR, "presentation", "Airfare_Route_Segmentation_Presentation.pptx")
    if os.path.exists(pptx_path):
        from flask import send_file
        return send_file(pptx_path, as_attachment=True, download_name="Airfare_Route_Segmentation_Presentation.pptx")
    return jsonify({"error": "File not found"}), 404

@app.route("/api/predict", methods=["GET", "POST"])
def api_predict():
    if request.method == "POST":
        data = request.get_json(silent=True) or request.form
    else:
        data = request.args

    origin = data.get("from", data.get("origin", "DEL"))
    destination = data.get("to", data.get("destination", "LON"))
    depart = data.get("depart", "2026-11-26")
    travel_class = data.get("class", "Economy")

    result = engine.predict_booking_decision(
        origin=origin,
        destination=destination,
        depart_date_str=depart,
        travel_class=travel_class
    )
    return jsonify(result)

@app.route("/api/metrics")
def api_metrics():
    return jsonify(engine.metrics)

@app.route("/api/routes")
def api_routes():
    if not engine.routes_df.empty:
        records = engine.routes_df.to_dict(orient="records")
        return jsonify({"count": len(records), "routes": records})
    return jsonify({"count": 0, "routes": []})

@app.route("/api/pca")
def api_pca():
    pca_points = engine.metrics.get("pca_points", [])
    variance = engine.metrics.get("pca_variance_explained", [])
    loadings = engine.metrics.get("pca_loadings", {})
    return jsonify({
        "points": pca_points,
        "variance_explained": variance,
        "loadings": loadings
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
