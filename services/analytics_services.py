import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def top_destination(df):
    destination_count = df['AirportName'].value_counts().reset_index()
    destination_count.columns = ['Destination', 'FlightCount']
    top_3 = destination_count.head(3)
    
    return top_3

def total_flights(df):
    return len(df)

def flights_left(df):
    return len(df[df['Status'] == 'On time'])

def total_delayed_flights(df):
    return len(df[df['Status'] == 'Delayed'])


def prep_closing_time(df):
    last_flight = df.tail(1).copy()
    last_flight['time'] = pd.to_datetime(last_flight['time'], errors='coerce').dt.round('h')
    
    # Get the actual timestamp from the last row.
    last_time = last_flight['time'].iloc[0]
    
    last_hour = last_time.hour
    prep_close_hour = last_hour - 2
    
    # Format the hours into a string (e.g., "07:00 PM").
    formatted_time_p = datetime.strptime(str(prep_close_hour), "%H").strftime("%I:%M %p")
    formatted_time_c = datetime.strptime(str(last_hour), "%H").strftime("%I:%M %p")
    
    return formatted_time_p, formatted_time_c

def analytics(df):
    
    top_destinations = top_destination(df)
    total_f = total_flights(df)
    pre_close, close = prep_closing_time(df)
    fl = flights_left(df)
    delayed_flights = total_delayed_flights(df)
    
    return fl, delayed_flights, top_destinations, total_f, pre_close, close
    