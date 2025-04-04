import streamlit as st
import pandas as pd
from services.analytics_services import  analytics
from services.df_service import *
import altair as alt
from scripts.script import extract_flight_data_excel

st.set_page_config(layout="wide")

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

def show_analytics(df):
    fl, delayed_flights, top_dest, total, pre_close, close = analytics(df)
    
    st.metric("Total Flights", total)
    st.metric("Flights Left", fl)
    st.metric("Delayed flights", delayed_flights)
    
    # st.subheader("Peak Operational Hours")
    # st.bar_chart(rh.set_index('time_window'), horizontal=True)
    
    st.subheader("Top 3 Destinations")
    st.dataframe(top_dest, use_container_width=True, hide_index=True)
    
    st.metric("Prep Closing", pre_close)
    st.metric("Final Closing", close)
    

def international_page():
    st.title("International Flights")
    raw_data = international_flights()
    data = raw_data[['AirlineName', 'time', 'updatedTime', 'AirportName', 'Status', 'Flight number', 'Passengers']]
    passenger_distribution = passenger_distribution_df(data.copy())
    flight_counts = flights_per_hour_distribution_df(data.copy())   
    
    hide_departed = st.checkbox("Hide Departed Flights", value=False)

    if hide_departed:
        data = data[data["Status"] != "Departed"]  # Filter out "Departed" rows
    
    if isinstance(data, pd.DataFrame):

        data = data.reset_index(drop=True)  # Reset index to remove default numbering
        data.index = data.index + 1  # Start index from 1 instead of 0

        col1, col2 = st.columns([3, 2])  
        with col1:
            st.subheader("Flight Data")
            st.dataframe(data.style.apply(highlight_delayed, axis=1), 
                        use_container_width=True,
                        height=600)

            p_chart = alt.Chart(passenger_distribution).mark_bar().encode(
                x=alt.X('time:N', title="Time Slots", sort=list(passenger_distribution['time'])),  
                y=alt.Y('passengers:Q', title="Number of Passengers", scale=alt.Scale(domain=[0, 1000])),
                color=alt.value("#3498db"), 
                tooltip=[
                    alt.Tooltip('time:N', title="Time "),
                    alt.Tooltip('passengers:Q', title="Total Passengers", format=',d')  # Comma format for numbers
                ]
            ).properties(
                width=700,
                height=400
            )

            f_chart = alt.Chart(flight_counts).mark_bar().encode(
                x=alt.X('rounded_hour:N', title="Time Slots", sort=list(flight_counts['rounded_hour']), axis=alt.Axis(labelAngle=0)),
                y=alt.Y('flight_counts:Q', title="Number of Flights"),
                color=alt.value("#3498db"), 
                tooltip=[
                    alt.Tooltip('rounded_hour:N', title="Hour"),
                    alt.Tooltip('flight_counts:Q', title="Flights Count", format=',d')  # Ensures readable number format
                ]
            ).properties(
                width=700,
                height=400
            )

            st.title("Passengers Traffic")
            st.altair_chart(p_chart, use_container_width=True)
            
            st.subheader("Flights per Hour")
            st.altair_chart(f_chart, use_container_width=True)
            
        with col2:
            show_analytics(data)     
    else:
        st.error(data)

def log_in():
    if "scheduling_password_validated" not in st.session_state:
        st.session_state["scheduling_password_validated"] = False

    if not st.session_state["scheduling_password_validated"]:
        password = st.text_input("Enter Password to Access Scheduling", type="password")
        if st.button("Login"):
            if password == "0412":
                st.session_state["scheduling_password_validated"] = True
                st.success("Access granted!")
                return True
            else:
                st.error("Incorrect password. Please try again.")
                return False
        return
     


def scheduling_page():
    st.title("Scheduling")
    # Extract flight data and add footprint
    df = extract_flight_data_excel()
    df = add_footprint(df)
    
    st.write("### Complete Flight Data")
    st.dataframe(df)
    
    # Organize flights by day and display for the first 14 days
    df2 = organized_flights_by_day(df)
    first_14_days = list(df2.keys())[:14]
    
    for day in first_14_days:
        col1, col2 = st.columns([1, 2])  

        with col1:
            st.write(f"### Flights for {day}")
            day_df = df2[day]
            day_df.index = range(1, len(day_df) + 1)  # reset index for readability
            st.dataframe(day_df)

        with col2:
            st.write("#### Passenger Traffic")
            passenger_traffic_df = passenger_distribution_monthly_df(day_df)
            st.altair_chart(plot_passenger_traffic(passenger_traffic_df), use_container_width=True)

# ----------------- Sidebar Navigation ----------------- #

with st.sidebar:
    st.header("Navigation")
    if st.button("🏢 Home"):
        st.session_state.current_page = "home"
    if st.button("🥃 Int Analysis"):
        st.session_state.current_page = "int"
    if st.button("📅 Scheduling"):
        st.session_state.current_page = "scheduling"
    
    st.divider()
    st.caption(f"Data last refreshed: {pd.Timestamp.now(tz='US/Eastern').strftime('%Y-%m-%d %H:%M')}")

# ----------------- Main Content Router ----------------- #

if st.session_state.current_page == "home":
    home_page()
elif st.session_state.current_page == "int":
    international_page()
elif st.session_state.current_page == "scheduling":
    access = log_in()
    if access: 
        scheduling_page()

