import streamlit as st
from services.df_service import flight_gate_df
from services.db_services import get_user_info


def save_current_user(username):
    user_info = get_user_info(username)
    st.session_state['current_user'] = user_info

def set_flights():
    g1 = st.session_state['current_user'].get("lowerGate")
    g2 = st.session_state['current_user'].get("upperGate")
    flights_df = flight_gate_df(g1, g2)

    st.session_state.flights = flights_df
    
def get_session_flights():
    return st.session_state.flights