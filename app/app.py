import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium
import os


# Streamlit layout and title
st.title("Where is Garfield?")

# Get the current directory of the app (app.py is inside the 'app' folder)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one level from the 'app' folder to the root directory where locations.csv is
file_path = os.path.join(current_dir, "../data/cleaned/locations.csv")

# Check if the file exists before loading it
if os.path.exists(file_path):
    original_df = pd.read_csv(file_path)
else:
    st.error(f"File not found: {file_path}")
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
