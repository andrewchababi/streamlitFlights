import streamlit as st
from datetime import datetime
from monthly_flight_scripts import extract_flight_data_excel
from process_data_frame import add_footprint, organized_flights_by_day, passenger_distribution_df, plot_passenger_traffic

today = datetime.today()
today_str = today.strftime("%Y-%m-%d")
data = extract_flight_data_excel()
data = add_footprint(data)
data = organized_flights_by_day(data)

today_data = data[today_str]
print(today_data)

today_passenger_distribution = passenger_distribution_df(today_data)
print(today_passenger_distribution)

chart = plot_passenger_traffic(today_passenger_distribution)

def temp():
    st.set_page_config(page_title="Temporary Dashboard - Restoport", layout="wide")

    with st.container():
        st.markdown("## ⚠️ Temporary Dashboard")
        st.markdown(
            """
            *Our main website is currently down for maintenance.**  
            In the meantime, we're providing this **alternative dashboard** with high-level insights to help you stay on top of passenger flow.

            ---
            """
        )

    with st.container():
        st.markdown("### 🛫 Passenger Traffic Overview")
        st.markdown(
            f""" 
            ### **Date:** `{today_str}`  
            This chart summarizes the estimated passenger flow across the **entire international gate area** for the day.
            """
        )
        
        st.altair_chart(chart, use_container_width=True)

    with st.container():
        st.markdown("---")
        st.markdown(
            """
            *Thank you for your understanding.  
            We'll be back with full insights soon!*  
            Please make sure to refer to management explicitly for any decisions
            """
        )
       
    
temp()
   