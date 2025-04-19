import streamlit as st
import json, os
from typing import Callable, List

PERSIST_FILE = "counts.json"
ROLES = ["Bartender", "Waiter 1 ", "Waiter 2 ", "Waiter 3 ", "Waiter 4 "]



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



# def inc_role(role): 
#     st.session_state.counts[role] += 1
#     save_counts(st.session_state.counts)
#     # add timestamp to csv
        
# def dec_role(role):
#     print('decrement ----------------------' ,st.session_state.counts[role])
#     if st.session_state.counts[role] > 0:
#         st.session_state.counts[role] -= 1
#         save_counts(st.session_state.counts)
#         # need to decide if this removes timestamp from csv or not 
 
 
# def increment_button(role, on_clicked):
#     print('increment ', st.session_state.counts[role])
#     st.button(
#             "➕ Add Customer",
#             key=f"inc_{role}",
#             on_click=on_clicked,
#         )

# def decrement_button(role, on_clicked):
#     print('increment ', st.session_state.counts[role])
#     st.button(
#             "➖ Remove Customer",
#             key=f"dec_{role}",
#             on_click=on_clicked,
#         )

# # --- App Startup --- 
# st.set_page_config(layout='wide')
# st.title('Host - Customer Counters')


# # 1. Initialize session state from disk on first load
# if "counts" not in st.session_state:
#     st.session_state.counts = load_count()
    
# cols = st.columns(len(ROLES), gap='medium')





# for col, role in zip(cols, ROLES):
#     with col:
#         st.subheader(role)
        
#         st.markdown(f"## {st.session_state.counts[role]}")
#         # Increment button
#         increment_button(role, inc_role(role))

#         # Decrement button
#         decrement_button(role, dec_role(role))
        
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

# ——— Streamlit App ———
st.set_page_config(layout="wide")
st.title("Host — Customer Counters")

# load once
if "counts" not in st.session_state:
    st.session_state.counts = load_counts()

cols = st.columns(len(ROLES), gap="medium")

# Example extra callback
def log_change(role:str, new_value:int):
    print(f">>> {role} is now {new_value}")

for col, role in zip(cols, ROLES):
    with col:
        st.subheader(role)
        # +1 button, also logs changes
        counter_button("➕ Add", role, delta=1, callbacks=[log_change], key=f"inc_{role}")
        # display
        st.markdown(f"## {st.session_state.counts[role]}")
        # –1 button, no extra callbacks
        counter_button("➖ Remove", role, delta=-1, callbacks=None, key=f"dec_{role}")
        
        
