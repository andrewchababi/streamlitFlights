import streamlit as st
import pandas as pd
from services.analytics_services import analytics
from services.df_service import highlight_delayed
from services.chartPlot_service import create_flights_chart, create_passenger_dist_chart

current = st.session_state['current_user']

def show_analytics(df):
    fl, delayed_flights, top_dest, total, pre_close, close = analytics(df)
    
    st.metric("Total Flights", total)
    st.metric("Flights Left", fl)
    st.metric("Delayed flights", delayed_flights)
    
    st.subheader("Top 3 Destinations")
    st.dataframe(top_dest, use_container_width=True, hide_index=True)
    
    st.metric("Prep Closing", pre_close)
    st.metric("Final Closing", close)
    

def reset_data_index(df: pd.DataFrame):
    data = df.reset_index(drop=True)
    data.index += 1
    return data

def display_flights_df(flights_df): 
    st.subheader("Flight Data")
    st.dataframe(flights_df.style.format({'Gate': '{:.0f}'})
                         .apply(highlight_delayed, axis=1), 
                        use_container_width=True,
                        height=600)

    st.write('')
    
def display_passenger_chart(passenger_distribution: pd.DataFrame):
    p_chart = create_passenger_dist_chart(passenger_distribution)

    st.title("Passengers Traffic")
    st.altair_chart(p_chart, use_container_width=True)

    st.write('')
 
def display_flights_chart(flight_count: pd.DataFrame):
    f_chart = create_flights_chart(flight_count)

    st.subheader("Flights per Hour")
    st.altair_chart(f_chart, use_container_width=True)
    st.write('')
            
def refresh_button():
    refresh = st.button('Update Data')
    if  refresh: 
        st.rerun()