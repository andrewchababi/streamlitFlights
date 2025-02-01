import sqlite3
import pandas as pd
from datetime import datetime

querry = f"""
    SELECT * FROM flights_today
    WHERE gate BETWEEN ? AND ?;

"""

def flight_gate_df(g1, g2): 
    if g1 >= g2: 
        return "Please enter gate1 lower than gate 2."
    connection = sqlite3.connect('flights_today.db')
    df = pd.read_sql(querry, con=connection, params=(g1, g2))
    connection.close()
    
    return df


def top_destination(df):
    destination_count = df['AirportName'].value_counts().reset_index()
    destination_count.columns = ['Destination', 'FlightCount']
    top_3 = destination_count.head(3)
    
    return top_3

def total_flights(df):
    return len(df)


def prep_closing_time(df):
    last_flight = df.tail(1).copy()
    last_flight['time'] = pd.to_datetime(last_flight['time'], errors='coerce')
    last_hour = last_flight['time'].dt.hour.values[0]
    
    prep_close_hour = last_hour - 2
    
    formatted_time_p = datetime.strptime(str(prep_close_hour), "%H").strftime("%I:%M %p")
    formatted_time_c = datetime.strptime(str(last_hour), "%H").strftime("%I:%M %p")
    
    return formatted_time_p, formatted_time_c

def rush_hours(flights_df, time_col="time", window_minutes=60, top_n=3):
     # Ensure the time column is a datetime type
    flights_df = flights_df.copy()
    flights_df[time_col] = pd.to_datetime(flights_df[time_col], errors='coerce')
    
    # Bin the time into intervals (e.g., 30-minute windows)
    flights_df['time_window'] = flights_df[time_col].dt.floor(f"{window_minutes}min")
    
    # Group by time window and count flights
    rush_hours = (
        flights_df.groupby('time_window')
        .size()
        .reset_index(name='flight_count')
        .sort_values('flight_count', ascending=False)
        .head(top_n)
    )
    
    # Format the time window as a string (HH:MM)
    rush_hours['time_window'] = rush_hours['time_window'].dt.strftime('%H:%M')
    
    return rush_hours.reset_index(drop=True)

def analytics(df):
    """
    Compute key analytics for flight data, including top destinations, total flights, closing times, and rush hours.

    Parameters:
        df (pd.DataFrame): Flight data containing at minimum the columns:
            - 'AirportName' (str): Destination airport names.
            - 'time' (datetime): Scheduled departure times.

    Returns:
        tuple: A tuple containing:
            - top_destinations (pd.DataFrame): Top destinations with flight counts.
                Columns:
                    'Destination' (str): Destination name.
                    'FlightCount' (int): Number of flights to the destination.
            
            - total_f (int): Total number of flights for the day.
            
            - pre_close (str): Preparation closing time formatted as "%H:%M".
            
            - close (str): Final closing time formatted as "%H:%M".
            
            - rh (pd.DataFrame): Rush hours with flight counts per time window.
                Columns:
                    'time_window' (str): Time interval (e.g., "09:00-09:30").
                    'flight_count' (int): Number of flights in the interval.

    Example:
        >>> top_dest, total, pre_close, close, rush_hours = analytics(flights_df)
        >>> print(top_dest)
           Destination  FlightCount
        0  Punta Cana            5
        1      Cancun            3

        >>> print(total)
        42

        >>> print(pre_close)
        "17:30"

        >>> print(rush_hours)
           time_window  flight_count
        0  09:00-09:30           12
        1  14:30-15:00            9
    """
    top_destinations = top_destination(df)
    total_f = total_flights(df)
    pre_close, close = prep_closing_time(df)
    rh = rush_hours(df)
    
    return top_destinations, total_f, pre_close, close, rh
    
    

def main():
    carlos_flights = flight_gate_df(62, 69)
    print(carlos_flights)
    print(analytics(carlos_flights))
    
main()