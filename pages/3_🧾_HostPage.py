import streamlit as st
import json, os
import csv
from datetime import datetime
from typing import Callable, List

PERSIST_FILE = "counts.json"
ROLES = ["Bartender", "Waiter 1 ", "Waiter 2 ", "Waiter 3 ", "Waiter 4 "]


def log_timestamp(role: str, new_value: int, csv_path: str = "timestamps.csv"):
    file_exists = os.path.exists(csv_path)
    with open(csv_path, mode="a", newline="") as f:
        writer = csv.writer(f)
        # 1) Write header row the first time
        if not file_exists:
            writer.writerow(["role", "timestamp"])
        # 2) Always write your data row
        writer.writerow([role, datetime.now().isoformat()])
       

def reset_button():
    if st.button("🔄 Reset All Counters"):
        st.session_state.counts = { role: 0 for role in ROLES }
        save_counts(st.session_state.counts)
        st.rerun()

def load_counts():
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

      
def counter_button(
    label: str,
    role: str,
    delta: int,
    callbacks: List[Callable[[str,int], None]] = None,
    key: str = None
):
    """
    Renders a button that adds `delta` to st.session_state.counts[role].
    After updating & saving, it also runs each callback(role, new_value).
    """
    def _on_click(r: str):
        # 1) mutate
        new_val = max(0, st.session_state.counts[r] + delta)
        st.session_state.counts[r] = new_val
        # 2) persist
        save_counts(st.session_state.counts)
        # 3) extra side‐effects
        if callbacks:
            for cb in callbacks:
                cb(r, new_val)

    st.button(
        label,
        key=key or f"{label}_{role}",
        on_click=_on_click,
        args=(role,)
    )
    
# Example extra callback
def log_change(role:str, new_value:int):
    print(f">>> {role} is now {new_value}")
    
def host_login():
    st.title("🔒 Host Access Required")
    st.write("Enter your password to access the scheduling page.")
    true_password = "243"
    password = st.text_input("Password", type="password", key="host_pwd")

    if st.button("Login", key="host_login_btn"):
        if password == true_password:
            st.success("Access granted!")
            st.session_state.hostAccess = True
            st.rerun()
        else:
            st.error("Incorrect password. Please try again.")
            st.session_state.hostAccess = False

def host_page():
    # ——— Streamlit App ———
    st.title("Host — Customer Counters")

    # load once
    if "counts" not in st.session_state:
        st.session_state.counts = load_counts()

    reset_button()

    cols = st.columns(len(ROLES), gap="medium")

    for col, role in zip(cols, ROLES):
        with col:
            st.subheader(role)
            counter_button("➕ Add", role, delta=1, callbacks=[log_change, log_timestamp], key=f"inc_{role}")
            
            st.markdown(f"## {st.session_state.counts[role]}")

            counter_button("➖ Remove", role, delta=-1, callbacks=None, key=f"dec_{role}")

        
st.set_page_config(layout="wide")
    
        
        
# if 'hostAccess' not in st.session_state:
#     st.session_state.hostAccess = False
    
# if st.session_state.hostAccess == False:
#     host_login()
# else:
host_page()
    