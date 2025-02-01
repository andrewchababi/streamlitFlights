import streamlit as st
import pandas as pd
from services import flight_gate_df, analytics  # Replace with actual module name

st.set_page_config(layout="wide")

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"
if 'custom_gates' not in st.session_state:
    st.session_state.custom_gates = [None, None]

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

# Modified show_analytics function and page layouts
def show_analytics(df, col):
    top_dest, total, pre_close, close, rh = analytics(df)
    
    with col:
        # Key Metrics
        col.subheader("Key Performance Indicators")
        cols = col.columns(3)
        with cols[0]:
            col.metric("Total Flights", total)
        with cols[1]:
            col.metric("Prep Closing", pre_close)
        with cols[2]:
            col.metric("Final Closing", close)
        
        # Top Destinations
        col.subheader("Top 3 Destinations")
        col.dataframe(top_dest, use_container_width=True)
        
        # Rush Hours
        col.subheader("Peak Operational Hours")
        col.bar_chart(rh.set_index('time_window'))

def cp_page():
    st.title("Cost & Performance Analysis (Gates 62-69)")
    data = flight_gate_df(62, 69)
    
    if isinstance(data, pd.DataFrame):
        col1, col2 = st.columns([3, 2])  # Wider left column for data
        with col1:
            st.subheader("Flight Data")
            st.dataframe(data.style.format({'gate': '{:.0f}'}), 
                        use_container_width=True,
                        height=600)
        
        with col2:
            show_analytics(data, col2)
    else:
        st.error(data)

def ubar_page():
    st.title("Utility Bar Analysis (Gates 52-69)")
    data = flight_gate_df(52, 69)
    
    if isinstance(data, pd.DataFrame):
        col1, col2 = st.columns([3, 2])
        with col1:
            st.subheader("Flight Data")
            st.dataframe(data.style.format({'gate': '{:.0f}'}),
                        use_container_width=True,
                        height=600)
        
        with col2:
            show_analytics(data, col2)
    else:
        st.error(data)

def custom_page():
    st.title("Custom Gate Analysis")
    with st.expander("Gate Selection", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            g1 = st.number_input("Starting Gate", min_value=1, max_value=100, value=62)
        with col2:
            g2 = st.number_input("Ending Gate", min_value=1, max_value=100, value=69)
    
    if st.button("Analyze Custom Range"):
        data = flight_gate_df(g1, g2)
        if isinstance(data, pd.DataFrame):
            left, right = st.columns([3, 2])
            with left:
                st.subheader("Flight Data")
                st.dataframe(data.style.format({'gate': '{:.0f}'}),
                            use_container_width=True,
                            height=600)
            
            with right:
                show_analytics(data, right)
        else:
            st.error(data)
# Sidebar Navigation
with st.sidebar:
    st.header("Navigation")
    if st.button("🏠 Home"):
        st.session_state.current_page = "home"
    if st.button("💰 C&P Analysis"):
        st.session_state.current_page = "cp"
    if st.button("📊 UBar Analysis"):
        st.session_state.current_page = "ubar"
    if st.button("⚙️ Custom Analysis"):
        st.session_state.current_page = "custom"

# Main content router
if st.session_state.current_page == "home":
    home_page()
elif st.session_state.current_page == "cp":
    cp_page()
elif st.session_state.current_page == "ubar":
    ubar_page()
elif st.session_state.current_page == "custom":
    custom_page()

# Database status in sidebar
with st.sidebar:
    st.divider()
    st.caption(f"Database last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")