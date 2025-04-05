import streamlit as st
from services.db_services import username_password_match, get_user_info
from session_handling import save_current_user

st.set_page_config(layout="centered")    

st.session_state['current_user'] = None

st.title("🔐 Login")
        
def login_component():    
    with st.form(key='login_form'):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label='Login')

    if submit_button:
        if username_password_match(username, password):
            st.success("✅ Login successful!")
            st.write(f"Welcome, {username}!")
            save_current_user(username) 
            return {"success": True, "username": username}
        else:
            st.error("❌ Invalid username or password. Please try again.")
            return {"success": False, "username": None}
    
    return {"success": None, "username": None}

login_component()