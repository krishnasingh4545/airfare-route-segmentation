@echo off
title FarePredictor Flight Intelligence Server
echo ======================================================================
echo           STARTING FAREPREDICTOR FLIGHT INTELLIGENCE SERVER
echo ======================================================================
echo.
cd /d "%~dp0"
if exist flight_route_segmentation cd flight_route_segmentation

echo Starting Python server on http://127.0.0.1:5000 and http://127.0.0.1:5050 ...
start "" "http://127.0.0.1:5000/?from=DEL&to=LON&depart=2026-11-26&return=2026-11-28"
python run_app.py
pause
