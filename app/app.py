# Libraries -csv
import csv
from pathlib import Path
import json
from datetime import datetime
from zoneinfo import ZoneInfo


def update_data():
    # Basic version
    # Instanciate dictionaries
    data_rows = []
    headers = ["ts","date","time","lat","lon"]

    # Loop through all files and open them
    folder_path = Path("../data/raw")

    for file_path in folder_path.iterdir():
        if file_path.is_file() and file_path.suffix == ".txt":
            with file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                
                # Convert time
                ts_ms = data[0]["location"]["timeStamp"]
                dt = datetime.fromtimestamp(ts_ms / 1000, tz=ZoneInfo("Australia/Melbourne"))
                
                # Update data rows
                data_rows.append(
                    {"ts":ts_ms,
                    "date":dt.strftime("%Y-%m-%d"),
                    "time":dt.strftime("%H:%M:%S"),
                    "lat":data[0]["location"]["latitude"],
                    "lon":data[0]["location"]["longitude"],
                    
                    }
                                )


    # Remove duplicates
    unique_data_rows = [dict(t) for t in set(tuple(d.items()) for d in data_rows)]

    # Sort by timestamp
    unique_data_rows.sort(key=lambda item: item['ts'])

    # Export to csv "data/cleaned/locations.csv"
    with open("../data/cleaned/locations.csv", "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()  # Writes the header row
        writer.writerows(unique_data_rows) # Writes all dictionary rows




import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium


# Streamlit layout and title
st.title("Where is Garfield?")

# Load the dataframe
original_df = pd.read_csv("../data/cleaned/locations.csv")

# Unique dates list for selection
date_list = original_df['date'].unique().tolist()

# Store the previous date in session state (for comparison)
if 'previous_date' not in st.session_state:
    st.session_state.previous_date = None

# Streamlit selectbox for date selection
selected_date = st.selectbox("Select date", date_list)

# Check if the date has changed, if so, reset the slider
if selected_date != st.session_state.previous_date:
    # Reset the slider to 1 when the date changes (show first marker)
    st.session_state.num_markers = 1
    st.session_state.previous_date = selected_date  # Update previous date

# Filter the dataframe for the selected date
df = original_df[original_df['date'] == selected_date].reset_index(drop=True)


st.write("Use the slider to track Garfy's movements")

# Set the slider's max value to the number of rows available for the selected date
if 'num_markers' not in st.session_state:
    st.session_state.num_markers = 1  # Set default slider value on first load

num_markers = st.slider("Step", 1, len(df), st.session_state.num_markers)

# Get the time for the current marker (based on the slider position)
current_time = df.iloc[num_markers - 1]['time']

# Display the time under the slider
st.write(f"Time at marker {num_markers}: {current_time}")

# Create the map centered at the first point
m = folium.Map(location=[df["lat"].iloc[0], df["lon"].iloc[0]], zoom_start=17)

# Store the coordinates for the polyline
coordinates = []

# Loop through the DataFrame and add markers for the selected number of markers
for i, row in df.iloc[:num_markers].iterrows():
    # Append coordinates to the list for polyline
    coordinates.append([row["lat"], row["lon"]])
    
    if i == num_markers - 1:
        # If this is the current marker (based on the slider), make it a cat emoji
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"<b>{row['time']}</b>",  # Timestamp in popup
            icon=folium.DivIcon(html=f'<div style="font-size: 24px; color: black;">🐱</div>')  # Cat emoji
        ).add_to(m)
    else:
        continue

# Add a polyline to connect the markers
folium.PolyLine(locations=coordinates, color="orange", weight=2.5, opacity=1).add_to(m)

# Render the map in Streamlit using `st_folium`
st_folium(m, width=700, height=500)
