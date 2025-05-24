from db_config import get_snowflake_connection
import pandas as pd
import os
from geocoder import batch_geocode
from cultural_info_fetcher import get_cultural_info
import time


DATA_DIR = "assets/data"

def load_museums_data():
    df = pd.read_csv(os.path.join(DATA_DIR, "List_Of_Museums.csv"))
    df = df.dropna(subset=["Museum Name ", "District "])  # Clean missing names/states
    return df

def load_tourism_statistics():
    df = pd.read_csv(os.path.join(DATA_DIR, "India-Tourism-Statistics-2021-Table-5.1.1.csv"))
    df.columns = df.columns.str.strip().str.replace("\n", " ")
    df = df.dropna(how="all")  # Drop rows where all values are NaN
    return df

def load_culturalheritage_sites():
    df = pd.read_csv(os.path.join(DATA_DIR, "Convergenceproject_Conservationofhertiagestructure_automated_parkings_Jammu_2018_1.csv"))
    return df

def load_historical_sites():
    df = pd.read_csv(os.path.join(DATA_DIR, "D31-CulturalHeritage_1.csv"))
    df = df.dropna( how='all')
    return df

def load_hotel_data():
    df = pd.read_csv(os.path.join(DATA_DIR, "Number_of_Hotel_rooms_upto_2012.csv"))
    df = df.dropna()
    return df

def load_resident_departures():
    df = pd.read_csv(os.path.join(DATA_DIR, "Residents_Departures_upto_2011.csv"))
    return df

def load_monthly_visitors():
    df = pd.read_csv(os.path.join(DATA_DIR, "Visitors_Arrivals_Monthly_upto_may_2014.csv"))
    return df

def load_tourism_by_country():  
    df = pd.read_csv(os.path.join(DATA_DIR, "syb-18-chapter_26_tourism_table_26.2.csv"))
    df = df.dropna()
    return df

def load_tourism_monthly():
    df = pd.read_csv(os.path.join(DATA_DIR, "syb-18-chapter_26_tourism_table_26.3.csv"))
    df = df.dropna()
    return df

def load_geo_heritage():
    df = pd.read_csv(os.path.join(DATA_DIR, "geo_heritage.csv"))
    df = df.dropna()
    return df

def load_state_tourism():
    df = pd.read_csv(os.path.join(DATA_DIR, "State_wise_FTV_DTV.csv"))
    df = df.dropna()
    return df

def load_tourism_funding():
    df = pd.read_csv(os.path.join(DATA_DIR, "Statewise_funds_from_gov.csv"))
    df = df.dropna()
    return df

def load_tourism_website():
    df = pd.read_csv(os.path.join(DATA_DIR, "State_Tourism_Links.csv"))
    df = df.dropna()
    return df

def load_destinations():
    dest_path = os.path.join(DATA_DIR, "Visiting_place_statewise.csv")
    cached_path = os.path.join(DATA_DIR, "cultural_destinations_enriched.csv")
    
    if os.path.exists(cached_path):
        return pd.read_csv(cached_path)
    
    if not os.path.exists(os.path.join(DATA_DIR, "cultural_destinations_geocoded.csv")):
        batch_geocode(dest_path, os.path.join(DATA_DIR, "cultural_destinations_geocoded.csv"))
    
    df = pd.read_csv(os.path.join(DATA_DIR, "cultural_destinations_geocoded.csv"))
    
   
    if 'CULTURAL_IMPORTANCE' not in df.columns:
        cultural_info = []
        for _, row in df.iterrows():
            info = get_cultural_info(row['Destination'], row['State'])
            cultural_info.append(info)
            time.sleep(2)  # Be gentle with Wikipedia's servers
            print(f"Fetched info for {row['Destination']}")
        
        df['CULTURAL_IMPORTANCE'] = cultural_info
        df.to_csv(cached_path, index=False)
    

    df = df[
        df['LATITUDE'].notna() &
        df['LONGITUDE'].notna() &
        df['LATITUDE'].between(-90, 90) &
        df['LONGITUDE'].between(-180, 180)
    ]
    
    return df


