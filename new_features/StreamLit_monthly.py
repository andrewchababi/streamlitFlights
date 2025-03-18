import streamlit as st
import pandas as pd
from monthly_flight_scripts import extract_flight_data_excel
from process_data_frame import *

# Apply dark mode styling
st.markdown(
    """
    <style>
        .reportview-container {
            background-color: #2f2f2f;
            color: white;
        }
        .sidebar .sidebar-content {
            background-color: #2f2f2f;
            color: white;
        }
        .widget-label {
            color: white;
        }
        .streamlit-expanderHeader {
            color: white;
        }
        .css-ffhzg2 {
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"

# Page rendering functions
def home_page():
    st.title("Airport Flight Analytics Dashboard ✈️")
    st.write("""
    Welcome to the Montreal Airport Flight Analytics Dashboard!
    
    **Features:**
    - Real-time flight data analysis
    - Gate-specific performance metrics
    - Operational insights and forecasting
    - Custom gate range analysis
    
    Use the sidebar to navigate between different analytical views.
    """)


df = extract_flight_data_excel()

df = add_footprint(df)

# Display the complete dataframe
st.write("### Complete Flight Data")
st.dataframe(df)

# Organize flights by day
df2 = organized_flights_by_day(df)

# Get the first 14 days (two weeks)
first_14_days = list(df2.keys())[:14]

st.write("## Flights for the First Two Weeks")

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