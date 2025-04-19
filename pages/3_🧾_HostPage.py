import streamlit as st
import json, os

PERSIST_FILE = "counts.json"
ROLES = ["Bartender", "Waiter 1 ", "Waiter 2 ", "Waiter 3 ", "Waiter 4 "]



def load_count():
    counts = {}
    if os.path.exists(PERSIST_FILE):
        with open(PERSIST_FILE, "r") as f:
            counts = json.load(f)
    for role in ROLES:
        counts.setdefault(role, 0)
    return counts

def save_counts(counts):
    with open(PERSIST_FILE, "w") as f:
        json.dump(counts, f)



def increment_button(role): 
    if st.button("➕ Add Customer", key=f"inc_{role}"):
        st.session_state.counts[role] += 1
        save_counts(st.session_state.counts)
        # add timestamp to csv
        
def decrement_button(role):
    if st.button("➖ Remove Customer", key=f"dec_{role}"):
        if st.session_state.counts[role] > 0:
            st.session_state.counts[role] -= 1
            save_counts(st.session_state.counts)
            # need to decide if this removes timestamp from csv or not 
 

# --- App Startup --- 
st.set_page_config(layout='wide')
st.title('Host - Customer Counters')


# 1. Initialize session state from disk on first load
if "counts" not in st.session_state:
    st.session_state.counts = load_count()
    
cols = st.columns(len(ROLES), gap='medium')





for col, role in zip(cols, ROLES):
    with col:
        st.subheader(role)
        
        st.markdown(f"## {st.session_state.counts[role]}")
        # Increment button
        increment_button(role)

        # Display current count


        # Decrement button
        decrement_button(role)
        
        
        
