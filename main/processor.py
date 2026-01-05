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

if __name__=="__main__":
    update_data()