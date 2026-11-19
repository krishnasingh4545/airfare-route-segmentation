"""
FarePredictor Web Application Launcher.
Starts the local Flask web server on port 5000.
To run outside the sandbox for browser access:
  python run_app.py
"""

import os
import sys
import threading

app_dir = os.path.join(os.path.dirname(__file__), "app")
sys.path.append(app_dir)

from app import app

def run_port_5050():
    try:
        app.run(host="127.0.0.1", port=5050, debug=False, use_reloader=False)
    except Exception as e:
        pass

if __name__ == "__main__":
    t = threading.Thread(target=run_port_5050, daemon=True)
    t.start()

    print("=" * 80)
    print("FAREPREDICTOR & AIRFARE ROUTE SEGMENTATION INTELLIGENCE")
    print("Serving on BOTH ports:")
    print("  👉 http://127.0.0.1:5000")
    print("  👉 http://127.0.0.1:5050  <-- (Fresh port without any browser cache!)")
    print("=" * 80)
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
