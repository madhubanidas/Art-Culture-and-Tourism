import pandas as pd
import requests
import time
from geopy.geocoders import Nominatim
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize geocoder
geolocator = Nominatim(user_agent="india_cultural_map")

def geocode_destination(name, state):
    try:
        query = f"{name}, {state}, India"
        location = geolocator.geocode(query, exactly_one=True)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        print(f"Error geocoding {name}: {str(e)}")
    return None, None

def batch_geocode(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    
    if 'LATITUDE' not in df.columns:
        df['LATITUDE'] = None
        df['LONGITUDE'] = None
    
    for idx, row in df.iterrows():
        if pd.isna(row['LATITUDE']) or pd.isna(row['LONGITUDE']):
            lat, lon = geocode_destination(row['Destination'], row['State'])
            df.at[idx, 'LATITUDE'] = lat
            df.at[idx, 'LONGITUDE'] = lon
            time.sleep(1)  # Respect rate limits
    
    df.to_csv(output_csv, index=False)
    return df

