import pandas as pd
import pgeocode
from geopy.geocoders import Nominatim
import time

# NOTES: 
# Geocode: geocode doesnt recognise NI postcodes and also gives wrong postcodes for irrelevant inputs such as OSLO etc. but handles UK postcodes with accuracy
# Pgeocode: can't handle locations with precision (~20km deviation maybe more), so we will use it only for N.I., and Ireland postcodes.

geolocator = Nominatim(user_agent="geo_lookup", timeout=10)

def get_employee_coordinates(file):
    df = file
    df = df[df["Responsible Technician: Member Name"].notna() & (df["Responsible Technician: Member Name"] != "")]
    df = df.drop_duplicates(subset=["Responsible Technician: Member Name"], keep="first") #Removes duplicate inputs
    df = df.sort_values(by="Responsible Technician: Member Name", ascending=True) #Alphabetically ascending sorting
    
    #Creates 2 more empty columns for Longitude and Latitude to be populated below
    df["Latitude"] = None
    df["Longitude"] = None
    
    # Drop unnecessary columns
    columns_to_drop = ["Inventory Location: Location Name", "Member Name"]
    df = df.drop(columns=columns_to_drop, axis='columns')
    
    for index, row in df.iterrows():
        postcode = str(row["Zip"]).strip()
        country = row['Country']
        # Skip rows with empty or invalid postcodes
        if pd.isna(postcode) or postcode == "" or postcode.isspace():
            print(f"Skipping row with empty postcode at index {index}")
            continue  # Skip this row
        
        if country == 'United Kingdom':
            try:
                # Search for the postcode in the specified country
                location = geolocator.geocode(f"{postcode}, GB", exactly_one=True)
                
                if location:
                    # If location is found, store the latitude and longitude
                    df.at[index, "Latitude"] = location.latitude
                    df.at[index, "Longitude"] = location.longitude
                    print(f"Found coordinates for {postcode}: {location.latitude}, {location.longitude}")
                else:
                    print(f"No location found for postcode {postcode}")
                # Prevent server overload (important when making many requests)
                time.sleep(1)  
            except Exception as e:
                print(f"Error with postcode {postcode}: {e}")
        else:
            # Initialize geocoders
            geo_uk = pgeocode.Nominatim("GB")  # Covers UK (England, Scotland, Wales, N. Ireland) - Interested in NI for this
            geo_ie = pgeocode.Nominatim("IE")  # Covers Ireland
            
            # Try UK geocoding first
            result_uk = geo_uk.query_postal_code(postcode)
            if pd.notna(result_uk.latitude) and pd.notna(result_uk.longitude):
                df.at[index, "Latitude"] = result_uk.latitude
                df.at[index, "Longitude"] = result_uk.longitude
                continue  # Skip to next row if found

            # If not found in UK, try Ireland geocoding
            result_ie = geo_ie.query_postal_code(postcode)
            if pd.notna(result_ie.latitude) and pd.notna(result_ie.longitude):
                df.at[index, "Latitude"] = result_ie.latitude
                df.at[index, "Longitude"] = result_ie.longitude


            
    # Format Latitude and Longitude to 6 decimal places
    df['Latitude'] = df['Latitude'].apply(lambda x: "{:.6f}".format(float(str(x).replace(",", "."))) if pd.notna(x) else x)
    df['Longitude'] = df['Longitude'].apply(lambda x: "{:.6f}".format(float(str(x).replace(",", "."))) if pd.notna(x) else x)
  
    # Save the results to an Excel file
    df.to_excel("UK&I_engineers_sorted_for_reference.xlsx", index=False)

    return df
