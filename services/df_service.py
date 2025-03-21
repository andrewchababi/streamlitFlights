from scripts.script import process_flights_to_df, url
from flight_passenger_map import flight_mappings
import pandas as pd

def flight_gate_df(g1, g2):
    if g1 >= g2: 
        return "Please enter gate1 lower than gate 2."
    df = process_flights_to_df(url=url)
    filtered_df = df[(df['Gate'] >= g1) & (df['Gate'] <= g2)].reset_index(drop=True)
    data = add_footprint(filtered_df)
    
    return data

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
    x_df = df[['AirlineName', 'time', 'Passengers']].copy()
    x_df['time'] = pd.to_datetime(x_df['time'])
    return x_df
    

def round_time_to_halfhour(df): 
    df['time'] = df['time'].dt.round('30min').dt.strftime('%H:%M')
    return df


def adjust_time_slot(time_str: str, offset_hours: float) -> str:
    base_time = pd.to_datetime(time_str, format='%H:%M')
    adjusted_time = (base_time + pd.Timedelta(hours=offset_hours)).strftime('%H:%M')
    return adjusted_time

def distribute_passengers_for_row(time_str: str, passengers: int) -> list:
    time_offsets = [-2.0, -1.5, -1.0]  # In hours
    percentages = [0.25, 0.50, 0.25]
    
    distributions = []
    for offset, pct in zip(time_offsets, percentages):
        adjusted_time = adjust_time_slot(time_str, offset)
        distributions.append({'time': adjusted_time, 'passengers': int(passengers * pct)})
    
    return distributions

def distribute_passengers_df(df: pd.DataFrame) -> pd.DataFrame:
    all_rows = []
    
    for _, row in df.iterrows():
        row_distributions = distribute_passengers_for_row(row['time'], row['Passengers'])
        all_rows.extend(row_distributions)
    
    # Create a new DataFrame and aggregate passengers for duplicate time slots
    distributed_df = pd.DataFrame(all_rows)
    full_time_range = generate_halfhour_time_range()
    
    final_df = full_time_range.merge(distributed_df, on="time", how="left").fillna(0)
    
    final_df['passengers'] = final_df['passengers'].astype(int)
    
    # new_df = new_df.groupby('time', as_index=False).sum()
    
    return final_df

def generate_halfhour_time_range(start="03:00", end="23:30"):
    time_range = pd.date_range(start=start, end=end, freq="30min").strftime('%H:%M')
    return pd.DataFrame({'time': time_range})

def passenger_distribution_df(df):
    df = flights_per_halfHour_df(df)
    df = round_time_to_halfhour(df)
    dist_df = distribute_passengers_df(df)
    return dist_df


def flights_per_hour_distribution_df(df, time_col='time'):
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