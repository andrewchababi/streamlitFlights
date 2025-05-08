
import streamlit as st
from services.db_services import username_password_match
from session_handling import save_current_user

def login_component():
    st.subheader("🔐 Login")
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label='Login')
    
    if submit_button:
        if username_password_match(username, password):
            st.success("✅ Login successful!")
            st.write(f"Welcome, {username}!")
            save_current_user(username)  
            st.rerun()
        else:
            st.error("❌ Invalid username or password. Please try again.")
    return False
    
def navigation_component():
    st.write("### Navigation")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Analytics 📊"):
            st.switch_page('pages/2_📊_DashBoard.py')
        # if st.button("Tasks 📝 (Coming soon)"):
        #     print("Todo")
        if st.button("Scheduling 🗓️"):
            st.switch_page("pages/4_🗓️_Scheduling.py")
    with col2:
        if st.button("Host"):
            st.switch_page('pages/3_🧾_HostPage.py')
        if st.button("Log Out"):
            st.session_state["current_user"] = None
            st.session_state.access = False
            st.rerun()

