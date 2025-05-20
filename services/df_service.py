from scripts.script import process_flights_to_df, url
from constants import *
import pandas as pd
from datetime import time

def flight_gate_df(g1, g2):
    if g1 >= g2: 
        return "Please enter gate1 lower than gate 2."
    df = process_flights_to_df(url=url)
    filtered_df = df[(df['Gate'] >= g1) & (df['Gate'] <= g2)].reset_index(drop=True)
    data = add_footprint(filtered_df)
    
    return data

def international_flights():
    df = process_flights_to_df(url=url)
    df["dest_code"] = df["FlightId"].str[-3:]
    intl_df = df[df["dest_code"].isin(international_codes)].reset_index(drop=True)
    data = add_footprint(intl_df)
    return data

def organized_flights_by_day(df):
    grouped_flights = {date: flights for date, flights in df.groupby("Date")}
    return grouped_flights

def add_footprint(df):
    df["Passengers"] = 0
    df["Passengers"] = df["Flight number"].apply(assess_passengers)
    return df

def assess_passengers(unique_display_number): 
    return flight_mappings.get(unique_display_number, 188)

def highlight_delayed(row):
    """Style function for pandas Styler"""
    if row['Status'] == 'Delayed' or row['Status'] == 'Cancelled':
        return ['background-color: #800020'] * len(row)  # Light red
    return [''] * len(row)


def flights_per_halfHour_df(df):
    x_df = df[['AirlineName', 'updatedTime', 'Passengers']].copy()
    x_df['updatedTime'] = pd.to_datetime(x_df['updatedTime'])
    return x_df

def flights_per_halfHour_monthly_df(df):
    x_df = df[['Date', 'time', 'Flight number','Passengers']].copy()
    x_df['time'] = pd.to_datetime(x_df['time'], format="%H:%M:%S", errors="coerce")
    return x_df
    

def round_time_to_halfhour(df): 
    df['updatedTime'] = df['updatedTime'].dt.round('30min').dt.strftime('%H:%M')
    return df

def round_time_to_halfhour_monthly(df): 
    df['time'] = df['time'].dt.round('30min').dt.strftime('%H:%M')
    return df

def adjust_time_slot(time_str: str, offset_hours: float) -> str:
    base_time = pd.to_datetime(time_str, format='%H:%M')
    adjusted_time = (base_time + pd.Timedelta(hours=offset_hours)).strftime('%H:%M')
    return adjusted_time

def distribute_passengers_for_row(time_str: str, passengers: int) -> list:
    time_offsets = [-1.5, -1.0, -0.5]  # In hours
    percentages = [0.25, 0.50, 0.25]
    
    distributions = []
    for offset, pct in zip(time_offsets, percentages):
        adjusted_time = adjust_time_slot(time_str, offset)
        distributions.append({'updatedTime': adjusted_time, 'passengers': int(passengers * pct)})
    
    return distributions

def distribute_passengers_for_row_monthly(time_str: str, passengers: int) -> list:
    time_offsets = [-1.5, -1.0, -0.5]  # In hours
    percentages = [0.25, 0.50, 0.25]
    
    distributions = []
    for offset, pct in zip(time_offsets, percentages):
        adjusted_time = adjust_time_slot(time_str, offset)
        distributions.append({'time': adjusted_time, 'passengers': int(passengers * pct)})
    
    return distributions

def distribute_passengers_df(df: pd.DataFrame) -> pd.DataFrame:
    all_rows = []
    
    for _, row in df.iterrows():
        row_distributions = distribute_passengers_for_row(row['updatedTime'], row['Passengers'])
        all_rows.extend(row_distributions)
    
    # Create a new DataFrame and aggregate passengers for duplicate time slots
    distributed_df = pd.DataFrame(all_rows)
    full_time_range = generate_halfhour_time_range()
    
    final_df = full_time_range.merge(distributed_df, on="updatedTime", how="left").fillna(0)
    
    final_df['passengers'] = final_df['passengers'].astype(int)
    
    return final_df

def distribute_passengers_monthly_df(df: pd.DataFrame) -> pd.DataFrame:
    all_rows = []
    
    for _, row in df.iterrows():
        row_distributions = distribute_passengers_for_row_monthly(row['time'], row['Passengers'])
        all_rows.extend(row_distributions)
    
    # Create a new DataFrame and aggregate passengers for duplicate time slots
    distributed_df = pd.DataFrame(all_rows)
    full_time_range = generate_halfhour_time_range_monthly()
    
    final_df = full_time_range.merge(distributed_df, on="time", how="left").fillna(0)
    
    final_df['passengers'] = final_df['passengers'].astype(int)
    
    return final_df

def generate_halfhour_time_range(start="03:00", end="23:30"):
    time_range = pd.date_range(start=start, end=end, freq="30min").strftime('%H:%M')
    return pd.DataFrame({'updatedTime': time_range})

def generate_halfhour_time_range_monthly(start="03:00", end="23:30"):
    time_range = pd.date_range(start=start, end=end, freq="30min").strftime('%H:%M')
    return pd.DataFrame({'time': time_range})


def distribute_resto_client_df(dist_df):
    resto_df = dist_df
    resto_df['passengers'] = resto_df['passengers'] * 0.25
    resto_df = client_rush_hours(resto_df)
    return resto_df

def distribute_resto_client_monthly_df(dist_df):
    resto_df = dist_df
    resto_df['passengers'] = resto_df['passengers'] * 0.15
    resto_df = client_rush_hours_monthly(resto_df)
    return resto_df

def client_rush_hours(df):
    t = pd.to_datetime(df['updatedTime'], format='%H:%M').dt.time
    # lunch & dinner rush boost
    rush = t.between(time(12, 30), time(13, 0)) | t.between(time(17, 30), time(18, 30))
    df.loc[rush, 'passengers'] *= 1.3
    # early‐morning & late‐evening reduction
    off = t.between(time(5, 30), time(6, 30))
    df.loc[off,  'passengers'] *= 0.5
    off = t.between(time(20, 30), time(22, 30))
    df.loc[off,  'passengers'] *= 0.7
    return df

def client_rush_hours_monthly(df):
    t = pd.to_datetime(df['time'], format='%H:%M').dt.time
    # lunch & dinner rush boost
    rush = t.between(time(12, 30), time(13, 0)) | t.between(time(17, 30), time(18, 30))
    df.loc[rush, 'passengers'] *= 1.3
    # early‐morning & late‐evening reduction
    off = t.between(time(5, 30), time(6, 30))
    df.loc[off,  'passengers'] *= 0.5
    off = t.between(time(20, 30), time(22, 30))
    df.loc[off,  'passengers'] *= 0.7
    return df
    
def passenger_distribution_df(df):
    df = flights_per_halfHour_df(df)
    df = round_time_to_halfhour(df)
    dist_df = distribute_passengers_df(df)
    resto_df = distribute_resto_client_df(dist_df)
    return resto_df


def passenger_distribution_monthly_df(df):
    df = flights_per_halfHour_monthly_df(df)
    df = round_time_to_halfhour_monthly(df)
    dist_df = distribute_passengers_monthly_df(df)
    resto_df = distribute_resto_client_monthly_df(dist_df)
    return resto_df

def flights_per_hour_distribution_df(df, time_col='updatedTime'):
    df[time_col] = pd.to_datetime(df[time_col], errors='coerce')

    # Round to the nearest hour
    df['rounded_time'] = df[time_col].dt.round("h")
    df['rounded_hour'] = df['rounded_time'].dt.hour  

    # Count flights per hour
    flight_counts = df.groupby('rounded_hour').size().reset_index(name='flight_counts')

    # Ensure all hours (0 to 23) are included
    all_hours = pd.DataFrame({'rounded_hour': range(3, 24)})  # Now starts at 3 AM
    flight_counts = all_hours.merge(flight_counts, on='rounded_hour', how='left').fillna(0)

    # Convert flight_counts to integer
    flight_counts['flight_counts'] = flight_counts['flight_counts'].astype(int)

    return flight_counts

def flights_per_half_hour_distribution_df(df: pd.DataFrame, time_col='updatedTime'):
    df[time_col] = pd.to_datetime(df[time_col], errors='coerce')

    df['rounded_half_hour_time'] = df[time_col].dt.round('30min').dt.strftime('%H:%M')

    flights_count = df.groupby('rounded_half_hour_time').size().reset_index(name="flights_count")

    all_half_hours = generate_halfhour_time_range().rename(columns={"updatedTime":'rounded_half_hour_time'})

    flights_count = all_half_hours.merge(flights_count, on='rounded_half_hour_time', how='left').fillna(0)
    
    flights_count['flights_count'] = flights_count['flights_count'].astype(int)
    
    return flights_count
