import streamlit as st
import pandas as pd
from services.chartPlot_service import create_passenger_dist_monthly_chart
from services.df_service import passenger_distribution_monthly_df

current = st.session_state['current_user']

def reset_data_index(df: pd.DataFrame):
    data = df.reset_index(drop=True)
    data.index += 1
    return data
    
def display_passenger_monthly_chart(passenger_distribution: pd.DataFrame):
    p_chart = create_passenger_dist_monthly_chart(passenger_distribution)

    st.title("Passengers Traffic")
    st.altair_chart(p_chart, use_container_width=True)

    st.write('')

def display_flights_day(daily_flights):

    for day in daily_flights.keys():
        col1, col2 = st.columns([1, 2])
    
        with col1:
            st.title(f"Flights for {day}")
            day_df = daily_flights[day]
            day_df.index = range(1, len(day_df) + 1)
            st.dataframe(day_df)

        with col2:
            passenger_distribution = passenger_distribution_monthly_df(day_df)
            p_chart = create_passenger_dist_monthly_chart(passenger_distribution)

            st.title("Passengers Traffic")
            st.altair_chart(p_chart, use_container_width=True)

            st.write('')

                    