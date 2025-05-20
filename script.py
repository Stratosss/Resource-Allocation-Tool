import pandas as pd
import folium
from folium import Map, Icon, Circle
from folium.plugins import TreeLayerControl, MeasureControl
from folium.features import Marker
import random
import matplotlib.colors as mcolors
import staff_coordinates
import glob
import traceback
from datetime import datetime
import msvcrt

print("Developed by Efstratios Gialouris for XYZ Corp. - All rights reserved \n")

while True:
    try:
        radius_input_miles = int(input("Please add radius in miles ( e.g. 30 for 30 miles) and press enter:"))
        break
    except ValueError:
        print("Please input a correct value.")

print("Importing modules....Finding Coordinates....Plotting Map")
print("Please wait while the tool is running, then open the Map.html file \n")

radius_conversion_to_meters = (1.609344 * radius_input_miles)*1000

# Get all available color names
colors = list(mcolors.CSS4_COLORS.keys())

keywords = "Technicians"
try:
    matching_files = glob.glob(f"*{keywords}*.xlsx")
    file_path = matching_files[0]

    df_employees = pd.read_excel(file_path, keep_default_na=False)

    df_accounts = pd.read_excel("Accounts2.xlsx", skiprows=1)  # Adjust file path
    df_accounts = df_accounts.dropna(subset=["Latitude", "Longitude"]) #removes null cells

    m = Map(
        [55.3617609, -3.4433238], 
        zoom_start=6,
        control_scale=True,
        )

    folium.plugins.Geocoder().add_to(m)        
    m.add_child(MeasureControl())  

    df_employees_coordinates = staff_coordinates.get_employee_coordinates(df_employees)
    number_of_employees = len(df_employees_coordinates)

    accounts_tree = {"label": "ACCOUNTS", "select_all_checkbox": "Un/select all", "children": []}
    employee_tree = {"label": f"FSE/APPS ({number_of_employees})", "select_all_checkbox": "Un/select all", "children": []}




    for i, row in df_employees_coordinates.iterrows():
        if row["Latitude"]:
            temp_color = random.choice(colors)
            circle = Circle(
                location=[row["Latitude"], row["Longitude"]],
                radius=radius_conversion_to_meters,
                color=temp_color,
                weight=1,
                fill_opacity=0.6,
                opacity=1,
                fill_color=temp_color,
                fill=False,  # gets overridden by fill_color
                popup=f"{radius_input_miles} miles",
                tooltip=f"{row['Responsible Technician: Member Name']}",
                ) 
            
            FSE_dict = {
                "label": row['Responsible Technician: Member Name'],
                "checked": False,
                "layer": Marker([row["Latitude"], row["Longitude"]], 
                                popup=f"{row['Responsible Technician: Member Name']}",  # Optional popup
                                icon=Icon(color="red" if "Applications"  in row["Service Team Name"]  else "blue", icon="info-sign")).add_to(m),
                "collapsed": True,
                "children":[{
                        "label": "Coverage Area",
                        "checked": False,
                        "layer": circle.add_to(m),
                        "collapsed": True
                    }]
            }
            employee_tree["children"].append(FSE_dict)
        else:
            continue

    #Accounts
    for _, row in df_accounts.iterrows():
        location_dict = {
            "label": row["Ship To Account Name"],
            "layer": Marker([row["Latitude"], row["Longitude"]], icon = Icon(color='purple', icon='building', prefix='fa'),
                            popup=row["Ship To Account Name"]).add_to(m)
        }
        accounts_tree["children"].append(location_dict)
            
    TreeLayerControl(overlay_tree=employee_tree).add_to(m) 
    TreeLayerControl(overlay_tree=accounts_tree).add_to(m) 

    # Save the map
    m.save("Map.html")
    print("Map was created successfully !! Press any key to exit...")
    msvcrt.getch()
except (IndexError, FileNotFoundError) as e:
    print("Error: " + str(e))
    print("Please provide an excel file (extension .xlsx) with the following formatted name: UK&I - Technicians-YYYY-MM-DD-hh-mm-ss and a file named "" ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current time
    error_message = f"[{timestamp}] Error: {e}\n"
    error_details = traceback.format_exc()  # Get full traceback

    # Overwrite and create a new log file from scratch
    with open("error_log.txt", "a") as file:
        file.write(error_message)
        file.write(error_details)  # Write full error details

    print("Error logged in error_log.txt. Press any key to exit...")
    msvcrt.getch()