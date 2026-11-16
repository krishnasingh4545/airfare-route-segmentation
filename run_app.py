"""
FarePredictor Web Application Launcher.
Starts the local Flask web server on port 5000.
To run outside the sandbox for browser access:
  python run_app.py
"""

import os
import sys
import webbrowser

app_dir = os.path.join(os.path.dirname(__file__), "app")
sys.path.append(app_dir)

from app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("=" * 80)
    print("FAREDETECTOR & AIRFARE ROUTE SEGMENTATION INTELLIGENCE")
    print(f"Server starting on http://127.0.0.1:{port}")
    print(f"Sample Route URL: http://127.0.0.1:{port}/?from=DEL&to=LON&depart=2026-11-26&return=2026-11-28")
    print("=" * 80)
    app.run(host="127.0.0.1", port=port, debug=False)
