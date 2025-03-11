import streamlit as st
import pandas as pd
from services.analytics_services import  analytics
from services.df_service import *
from services.chartPlot_service import *
import altair as alt

df = flight_gate_df(62,68)

df = flight_count_hour(df)

st.dataframe(df)

chart = plot_flights_by_hour_altair(df)

# chart2 = alt.Chart(df).mark_bar(
#         color='#89CFF0',  # Light blue for consistency
#         opacity=0.85,
#         size=30  # Increase bar width
#     ).encode(
#         x=alt.X('rounded_hour:O', title="Hour of Day", sort=list(map(str, df['rounded_hour']))),
#         y=alt.Y('flight_counts:Q', title="Number of Flights"),
#         tooltip=[alt.Tooltip('rounded_hour:O', title="Hour"), 
#                  alt.Tooltip('flight_counts:Q', title="Flights")]
#     ).properties(
#         width=750,
#         height=400
#     ).configure_axis(
#         labelFontSize=12,
#         titleFontSize=14
#     )

st.altair_chart(chart, use_container_width=True)




