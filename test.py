import streamlit as st
import pandas as pd
from services.analytics_services import  analytics
from services.df_service import *
from services.chartPlot_service import plot_flights_by_hour, plot_passengers_by_hour
import altair as alt

df = flight_gate_df(62,68)

df = flights_per_halfHour_df(df)

df = round_time_to_halfhour(df)

# Generate distributed passengers DataFrame
# df_output = distribute_passengers_df(df)
df_output = passenger_distribution_df(df)

st.title("Passenger Traffic")

chart = alt.Chart(df_output).mark_bar().encode(
    x=alt.X('time:N', title="Time Slots", sort=list(df_output['time'])),  # Ensure time is sorted
    y=alt.Y('passengers:Q', title="Number of Passengers"),
    tooltip=['time', 'passengers']
).properties(
    width=700,
    height=400
)

st.altair_chart(chart, use_container_width=True)


st.dataframe(df)


