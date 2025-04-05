import streamlit as st 

def sign_in_display():
    st.subheader("🔐 Please Sign In")
    st.write(
        "To access your **flight analytics** and **scheduling** features, "
        "please sign in using your credentials."
    )
    
def new_customer_display():
    st.subheader("🏬 New Customer?")
    st.write(
        "Are you a store manager interested in our services? "
        "Contact our team at [sales@restoport.xyz](mailto:sales@restoport.xyz) "
        "for more information."
    )