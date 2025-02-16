import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from script import process_flights_to_df, url

def flight_gate_df(g1, g2):
    if g1 >= g2: 
        return "Please enter gate1 lower than gate 2."
    df = process_flights_to_df(url=url)
    filtered_df = df[(df['gate'] >= g1) & (df['gate'] <= g2)]
    return filtered_df


def top_destination(df):
    destination_count = df['AirportName'].value_counts().reset_index()
    destination_count.columns = ['Destination', 'FlightCount']
    top_3 = destination_count.head(3)
    
    return top_3

def total_flights(df):
    return len(df)

def flights_left(df):
    return len(df[df['status'] == 'On time'])

def total_delayed_flights(df):
    return len(df[df['status'] == 'Delayed'])



def prep_closing_time(df):
    last_flight = df.tail(1).copy()
    last_flight['time'] = pd.to_datetime(last_flight['time'], errors='coerce')
    last_hour = last_flight['time'].dt.hour.values[0]
    
    prep_close_hour = last_hour - 2
    
    formatted_time_p = datetime.strptime(str(prep_close_hour), "%H").strftime("%I:%M %p")
    formatted_time_c = datetime.strptime(str(last_hour), "%H").strftime("%I:%M %p")
    
    return formatted_time_p, formatted_time_c

def rush_hours(flights_df, time_col="time", window_minutes=60, top_n=3):
    flights_df = flights_df.copy()
    flights_df[time_col] = pd.to_datetime(flights_df[time_col], errors='coerce')
    
    flights_df['time_window'] = flights_df[time_col].dt.floor(f"{window_minutes}min")
    
    rush_hours = (
        flights_df.groupby('time_window')
        .size()
        .reset_index(name='flight_count')
        .sort_values('flight_count', ascending=False)
        .head(top_n)
    )
    
    rush_hours['time_window'] = rush_hours['time_window'].dt.strftime('%H:%M')
    
    return rush_hours.reset_index(drop=True)


def plot_flights_by_hour(df, time_col="time"):
    # Ensure pyplot import is correct first
    df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
    df['rounded_time'] = df[time_col].dt.round("h")
    df['rounded_hour'] = df['rounded_time'].dt.hour
    
    flight_counts = df.groupby('rounded_hour').size().reindex(range(24), fill_value=0)
    
    # Set style using proper reference
    sns.set_theme(
        style='ticks',
        context="talk",
        palette="viridis",
        font="Arial"
    )
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(flight_counts.index, flight_counts.values, color='royalblue', alpha=0.7)
    
    # Customize labels and title with improved font sizes and weights
    ax.set_xlabel("Hour of Day", fontsize=12)
    ax.set_ylabel("Number of Flights", fontsize=12)
    ax.set_xlim(3,23)
    ax.set_xticks(range(3, 23))
    ax.set_xticklabels(range(3, 23), fontsize=10)
    
    plt.tight_layout()
    return fig, ax

def highlight_delayed(row):
    """Style function for pandas Styler"""
    if row['status'] == 'Delayed' or row['status'] == 'Cancelled':
        return ['background-color: #800020'] * len(row)  # Light red
    return [''] * len(row)

def analytics(df):
    """
    Compute key analytics for flight data, including top destinations, total flights, closing times,  store sales and rush hours.

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
    fl = flights_left(df)
    delayed_flights = total_delayed_flights(df)
    
    return fl, delayed_flights, top_destinations, total_f, pre_close, close, rh
    