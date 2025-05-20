import streamlit as st 
from services.df_service import *
from scripts.script import extract_flight_data_excel
from components.scheduling import *
from components.signIn import *

st.set_page_config(layout="wide")


def scheduling_log_in():
    true_password = st.session_state["current_user"].get('scheduling_code')
    
    st.title("Scheduling")

    with st.form("scheduling_form"):
        password = st.text_input("Enter Password to Access Scheduling", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if int(password) == true_password:
                st.success("Access granted!")
                st.session_state.access = True
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")
                st.session_state.access = False
         

def scheduling():
    st.title(f"Scheduling Analytics")
    all_flights = extract_flight_data_excel()
    footprint_flights = add_footprint(all_flights)

    st.write("### Complete Flight Data")
    st.dataframe(all_flights)

    daily_flights = organized_flights_by_day(footprint_flights)

    display_flights_day(daily_flights)

if 'access' not in st.session_state:
    st.session_state.access = False

if st.session_state.get('current_user') is None:
    sign_in_display()

else:
    if st.session_state.access == True:
        scheduling() 
    else:
        scheduling_log_in()
