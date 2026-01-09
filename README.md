# Garfield Location Tracker

Tracks Garfield's location using Apple's Find My network and visualizes movement history on an interactive map.

## Architecture

![Architecture Diagram](architecture.png)

## How it works

1. **AirTag** - Attached to Garfield, broadcasts location via Apple's Find My network
2. **MacMini** - Runs a bash script that periodically reads location data from Apple's cache and pushes it to GitHub
3. **GitHub** - Stores location history as the central data repository
4. **Streamlit** - Web app that reads from GitHub and displays Garfield's movement on an interactive map
5. **Manual Orchestration** - Laptop used to manage and coordinate the system components