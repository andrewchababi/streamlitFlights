import streamlit as st
import pandas as pd
from services import flight_gate_df, analytics, plot_flights_by_hour, highlight_delayed, add_footprint, plot_flights_by_hour, plot_passengers_by_hour

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
    fl, delayed_flights, top_dest, total, pre_close, close, rh = analytics(df)
    
    st.metric("Total Flights", total)
    st.metric("Flights Left", fl)
    st.metric("Delayed flights", delayed_flights)
    
    # st.subheader("Peak Operational Hours")
    # st.bar_chart(rh.set_index('time_window'), horizontal=True)
    
    st.subheader("Top 3 Destinations")
    st.dataframe(top_dest, use_container_width=True, hide_index=True)
    
    st.metric("Prep Closing", pre_close)
    st.metric("Final Closing", close)
    

def cp_page():
    st.title("Carlos and Pepes Flights (62-68)")
    data = flight_gate_df(62, 68)
    data = add_footprint(data)
    
    hide_departed = st.checkbox("Hide Departed Flights", value=False)

    if hide_departed:
        data = data[data["Status"] != "Departed"]  # Filter out "Departed" rows
    
    plot_df = data.copy()
    flights_fig, flights_ax = plot_flights_by_hour(plot_df)
    passengers_fig, passengers_ax = plot_passengers_by_hour(plot_df)
    
    if isinstance(data, pd.DataFrame):
        col1, col2 = st.columns([3, 2])  
        with col1:
            st.subheader("Flight Data")
            st.dataframe(data.style.format({'Gate': '{:.0f}'})
                         .apply(highlight_delayed, axis=1), 
                        use_container_width=True,
                        height=600)
        
            st.subheader("Flights per Hour")
            st.pyplot(flights_fig)
            
            st.subheader("Passengers per Hour")
            st.pyplot(passengers_fig)

        with col2:
            show_analytics(data)     
    else:
        st.error(data)

def ubar_page():
    st.title("Ubar Flights (52-68)")
    data = flight_gate_df(52, 68)
    data = add_footprint(data)
    
    hide_departed = st.checkbox("Hide Departed Flights", value=False)

    if hide_departed:
        data = data[data["Status"] != "Departed"]  # Filter out "Departed" rows
    
    plot_df = data.copy()
    fig, ax = plot_flights_by_hour(plot_df)
    passengers_fig, passengers_ax = plot_passengers_by_hour(plot_df)
    
    if isinstance(data, pd.DataFrame):
        col1, col2 = st.columns([3, 2])
        with col1:
            st.subheader("Flight Data")
            st.dataframe(data.style.format({'Gate': '{:.0f}'})
                         .apply(highlight_delayed, axis=1),
                        use_container_width=True,
                        height=600)
            
            st.subheader("Flights per Hour")
            st.pyplot(fig)
            st.subheader("Passengers per Hour")
            st.pyplot(passengers_fig)
        with col2:
            show_analytics(data)  
    else:
        st.error(data)


def custom_page():
    st.title("Custom Gate Flights Analysis")
    with st.expander("Gate Selection", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            g1 = st.number_input("Starting Gate", min_value=1, max_value=100, value=62)
        with col2:
            g2 = st.number_input("Ending Gate", min_value=1, max_value=100, value=68)
    
    if st.button("Analyze Custom Range"):
        data = flight_gate_df(g1, g2)
        if isinstance(data, pd.DataFrame):
            left, right = st.columns([3, 2])
            with left:
                st.subheader("Flight Data")
                st.dataframe(data.style.format({'Gate': '{:.0f}'}),
                            use_container_width=True,
                            height=600,
                            hide_index=True)
            
            with right:
                show_analytics(data)  # Pass the data directly
        else:
            st.error(data)

# Sidebar Navigation
with st.sidebar:
    st.header("Navigation")
    if st.button("🏢 Home"):
        st.session_state.current_page = "home"
    if st.button("🥃 C&P Analysis"):
        st.session_state.current_page = "cp"
    if st.button("🍷 UBar Analysis"):
        st.session_state.current_page = "ubar"

    st.divider()
    st.caption(f"Data last refreshed: {pd.Timestamp.now(tz='US/Eastern').strftime('%Y-%m-%d %H:%M')}")

# Main content router
if st.session_state.current_page == "home":
    home_page()
elif st.session_state.current_page == "cp":
    cp_page()
elif st.session_state.current_page == "ubar":
    ubar_page()