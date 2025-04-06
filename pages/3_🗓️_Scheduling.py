import streamlit as st 
from services.df_service import *
from scripts.script import extract_flight_data_excel
from components.dashboard import *
from components.signIn import *
from session_handling import set_flights, get_session_flights

st.set_page_config(layout="wide")

def dashboard():
    st.title(f"Scheduling Analytics")
    all_flights = extract_flight_data_excel()
    add_footprint_to_flights = add_footprint(all_flights)

    st.write("### Complete Flight Data")
    st.dataframe(all_flights)

    daily_flights = organized_flights_by_day(add_footprint_to_flights)

    for day in daily_flights.keys():
        col1, col2 = st.columns([1, 2])  

        with col1:
            st.write(f"### Flights for {day}")
            day_df = daily_flights[day]
            day_df.index = range(1, len(day_df) + 1)  # reset index for readability
            st.dataframe(day_df)

        with col2:
            st.write("## Passenger Traffic")
            passenger_traffic_df = passenger_distribution_monthly_df(day_df)
            st.altair_chart(create_passenger_dist_chart(passenger_traffic_df), use_container_width=True)

if st.session_state.get('current_user') is None:
    sign_in_display()
else:
    current = st.session_state['current_user']
    set_flights()
    dashboard()
    
    
    
