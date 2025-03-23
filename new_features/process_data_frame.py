import pandas as pd
import altair as alt
from flight_passengers_footprint import flight_mappings_excel

def organized_flights_by_day(df):
    grouped_flights = {date: flights for date, flights in df.groupby("Date")}
    return grouped_flights
 
def add_footprint(df):
    df["Passengers"] = 0
    df["Passengers"] = df["Flight number"].apply(assess_passengers)
    return df

def assess_passengers(unique_display_number): 
    return flight_mappings_excel.get(unique_display_number, 188)

def flights_per_halfHour_df(df):
    x_df = df[['Date', 'time', 'Flight number','Passengers']].copy()
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
    time_offsets = [-2.5, -2.0, -1.5, -1.0, -0.5]  # In hours
    percentages = [0.1, 0.25, 0.50, 0.25, 0.1]
    
    distributions = []

    time_obj = pd.to_datetime(time_str, format='%H:%M')

    # Special time range checks

    if (time_obj >= pd.to_datetime("07:00", format='%H:%M')) and (time_obj <= pd.to_datetime("08:30", format='%H:%M')):
        passengers *= 0.9

    if (time_obj >= pd.to_datetime("14:00", format='%H:%M')) and (time_obj <= pd.to_datetime("15:00", format='%H:%M')):
        passengers *= 2

    if (time_obj >= pd.to_datetime("19:30", format='%H:%M')) and (time_obj < pd.to_datetime("20:30", format='%H:%M')):
        passengers *= 1

    else:
        passengers *= 1  # For all other times, no change


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
    new_df = pd.DataFrame(all_rows)
    new_df = new_df.groupby('time', as_index=False).sum()
    
    return new_df

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

def plot_passenger_traffic(df):
   
    # Ensure time column is parsed, sorted, and formatted
    df["time"] = pd.to_datetime(df["time"], format="%H:%M").dt.strftime("%H:%M")
    
    # Generate the full set of time slots (every 30 minutes between the min and max time)
    time_slots = pd.date_range(df["time"].min(), df["time"].max(), freq="30min").strftime("%H:%M")
    
    # Merge with the original data, filling missing time slots with zero passengers
    df = pd.merge(pd.DataFrame({'time': time_slots}), df, on="time", how="left").fillna({'passengers': 0}) 

    p_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('time:N', title="Time Slots", sort=list(df['time']), axis=alt.Axis(labelAngle=-90, tickCount=len(time_slots))),
        y=alt.Y('passengers:Q', 
                title="Number of Passengers", 
                scale=alt.Scale(domain=[0, 1200])),
        color=alt.value("#3498db"), 
        tooltip=[
            alt.Tooltip('time:N', title="Time"),
            alt.Tooltip('passengers:Q', title="Passengers", format=',d')  # Formatted number
        ]
    ).properties(
        width=800,
        height=400,
    )

    return p_chart
