import streamlit as st
import json, os

PERSIST_FILE = "counts.json"
ROLES = ["Bartender", "Waiter 1", "Waiter 2", "Waiter 3", "Waiter 4"]


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



def increment_button(variable): 
    clicked = st.button("➕ Add Customer")
    if clicked:
        variable += 1
        # add timestamp to csv
        
def decrement_button(role):
    if st.button("➖ Remove Customer", key=f"inc_{role}"):
        if st.session_state.counts[role] > 0:
            st.session_state.counts[role] -= 1
            save_counts(st.session_state[role])
            # need to decide if this removes timestamp from csv or not 
 