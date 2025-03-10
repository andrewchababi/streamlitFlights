from scripts.script import process_flights_to_df, url
from flight_passenger_map import flight_mappings

def flight_gate_df(g1, g2):
    if g1 >= g2: 
        return "Please enter gate1 lower than gate 2."
    df = process_flights_to_df(url=url)
    filtered_df = df[(df['Gate'] >= g1) & (df['Gate'] <= g2)].reset_index(drop=True)
    return filtered_df

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
