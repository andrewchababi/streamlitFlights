import pandas as pd
from datetime import datetime

def extract_flight_data_excel(file_path="monthly_flights.xlsx"):

    df = pd.read_excel(file_path, skiprows=5)
    
    df.columns = df.columns.str.strip()
    
    # Ensure the Date column is in datetime format
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce').dt.strftime("%Y-%m-%d")

    df["time"] = pd.to_datetime(df["Heure plan. / Sched. Time"], format="%H:%M:%S", errors="coerce").dt.strftime("%H:%M:%S")

    df.rename(columns={
        "Compagnie aérienne/ Airline": "Airline",
        "No. Vol / Flight no.": "Flight Number",
        "Terminal": "Terminal"
    }, inplace = True)

    df["Flight number"] = df["Airline"].astype(str) + df["Flight Number"].astype(str)
    
    international_df = df[df["Terminal"] == "I"].reset_index(drop=True)

    international_df.index = international_df.index + 1
    
    extracted_df = international_df[["Date", "time", "Flight number"]]
    
    return extracted_df




