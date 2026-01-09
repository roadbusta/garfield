# Garfield Location Tracker

Tracks Garfield's location using Apple's Find My network and visualizes movement history on an interactive map.

## How it works

1. `scripts/copy.sh` - Periodically copies location data from Apple's Find My cache
2. `main/processor.py` - Processes raw JSON files and exports cleaned location data to CSV
3. `app/app.py` - Streamlit app that displays locations on a map with a slider to view movement over time