import streamlit as st
import pandas as pd
from monthly_flight_scripts import extract_flight_data_excel
from process_data_frame import plot_passenger_traffic , add_footprint, organized_flights_by_day, passenger_distribution_df

df = extract_flight_data_excel()

df = add_footprint(df)

# Display the complete dataframe
st.write("### Complete Flight Data")
st.dataframe(df)

# Organize flights by day
df2 = organized_flights_by_day(df)

# Get the first 14 days (two weeks)
first_14_days = list(df2.keys())[:14]
last_index = 0
# Loop through the first 14 days and display each day separately
for day in first_14_days:
    st.write(f"### Flights for {day}")

    # Get the current day's data
    day_df = df2[day]

    # Reset the index to start from 1 for each day
    day_df.index = range(1, len(day_df) + 1)
    
    # Display the DataFrame for the current day
    st.dataframe(day_df)

    # Generate passenger traffic data for that day
    passenger_traffic_df = passenger_distribution_df(df2[day])

    # Display Passenger Traffic Graph
    st.write("#### Passenger Traffic")
    st.altair_chart(plot_passenger_traffic(passenger_traffic_df), use_container_width=True)

    