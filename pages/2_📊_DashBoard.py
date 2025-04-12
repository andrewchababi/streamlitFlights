import streamlit as st 
from services.df_service import *
from components.dashboard import *
from components.signIn import *
from session_handling import set_flights, get_session_flights

st.set_page_config(layout="wide")

def dashboard():
    st.title(f"Flight Analytics")
    flights = get_session_flights()
    passenger_dist = passenger_distribution_df(flights.copy())
    flight_count = flights_per_hour_distribution_df(flights.copy())

    hide_departed = st.checkbox("Hide Departed Flights", value=False)

    if hide_departed:
        flights = flights[flights["Status"] != "Departed"] 
    
    if isinstance(flights, pd.DataFrame):
        flights = reset_data_index(flights)

        col1, col2 = st.columns([3,2])
        with col1:
            display_flights_df(flights)
            display_passenger_chart(passenger_dist)
            display_flights_chart(flight_count)
           
        with col2:
            refresh_button()
            show_analytics(flights)
    
    else:
        st.error(flights)


if st.session_state.get('current_user') is None:
    sign_in_display()
else:
    current = st.session_state['current_user']
    set_flights()
    dashboard()
    
    
    
