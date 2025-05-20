import streamlit as st
from components.login import login_component, navigation_component
from components.signIn import new_customer_display
# Configure the page
st.set_page_config(page_title="Flight Dashboard", layout="centered")

# Initialize current_user only once
if "current_user" not in st.session_state:
    st.session_state['current_user'] = None

st.title("Welcome to Restoport!")
st.markdown("Your hub for flight analytics and scheduling.")
st.markdown("---")  

if st.session_state.get("current_user") is None:
    login_component()
    st.markdown("---")
    new_customer_display()
else: 
    login_component()
    # TODO: make a welcome component to signal what user is signed in
    navigation_component()