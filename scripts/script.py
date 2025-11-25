# import json
# import pandas as pd
# import cloudscraper
# import streamlit as st

# # Define the URL and payload for fetching flight data
# url = "https://www.admtl.com/en-CA/webruntime/api/apex/execute?language=en-CA&asGuest=true&htmlEncode=false"

# headers = {
#     "Content-Type": "application/json; charset=utf-8",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
#     "Referer": "https://www.admtl.com/en-CA/flights/departures",
#     "Origin": "https://www.admtl.com",
#     "Accept": "*/*",
# }



# payload = {
#     "namespace": "",
#     "classname": "@udd/01pMm00000AWKuH",
#     "method": "getFlights",
#     "isContinuation": False,
#     "params": {
#         "language": "en-CA",
#         "page": "departures"
#     },
#     "cacheable": False
# }


# def fetch_flight_data(url):
#     scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
#     scraper.get("https://www.admtl.com/en-CA/flights/departures")

#     # response = cloudscraper.create_scraper().post(url,headers=headers, json=payload)
#     response = scraper.post(url, json=payload, headers=headers)
#     response.raise_for_status()
#     return response

# def parse_json_content(response_content):
#     return json.loads(response_content)

# def format_json_data(json_data):
#     return json.dumps(json_data, indent=4)

# def convert_to_dataframe(json_data, key='returnValue', section='flightsForToday'):
#     return pd.json_normalize(json_data[key][section])

# @st.cache_data(ttl=3600)
# def process_flights_to_df(url):
#     response = fetch_flight_data(url)
#     print(f"HTTP Status Code: {response.status_code}")

#     raw_data = response.content
#     structured_data = parse_json_content(raw_data)

#     flights_df = convert_to_dataframe(structured_data)

#     flights_df.rename(columns={
#         'TerminalGate': 'Gate',
#         'FormattedScheduledTime': 'time',
#         'FormattedUpdatedTime': 'updatedTime',
#         'OperationalStatusDescription': 'Status',
#         'PublicDisplayFlightNumber' : 'Flight number',
#     }, inplace=True)

#     new_columns_of_interest = ['AirlineName', 'Gate', 'time', 'updatedTime', 'AirportName', 'Status', 'Flight number']
#     new_df = flights_df[new_columns_of_interest]

#     new_df = new_df.copy()
#     new_df['Gate'] = new_df['Gate'].str.extract('(\\d+)')  # Extract digits
#     new_df = new_df.dropna()
#     new_df['Gate'] = new_df['Gate'].astype(int)

#     return new_df

# def extract_flight_data_excel(file_path="monthly_flights.xlsx"):

#     df = pd.read_excel(file_path, skiprows=5)
    
#     df.columns = df.columns.str.strip()
    
#     # Ensure the Date column is in datetime format
#     df["Date"] = pd.to_datetime(df["Date"], errors='coerce').dt.strftime("%Y-%m-%d")

#     df["time"] = pd.to_datetime(df["Heure plan. / Sched. Time"], format="%H:%M:%S", errors="coerce").dt.strftime("%H:%M:%S")

#     df.rename(columns={
#         "Compagnie aérienne/ Airline": "Airline",
#         "No. Vol / Flight no.": "Flight Number",
#         "Terminal": "Terminal"
#     }, inplace = True)

#     df["Flight number"] = df["Airline"].astype(str) + df["Flight Number"].astype(str)
    
#     international_df = df[df["Terminal"] == "I"].reset_index(drop=True)

#     international_df.index = international_df.index + 1
    
#     extracted_df = international_df[["Date", "time", "Flight number", "Destination"]]
    
#     return extracted_df

# def unique_international_dest(df):

#     data = df['Destination']

#     unique_destinations = set(data)

#     return unique_destinations
import json
import pandas as pd
import cloudscraper

# Define the URL and payload for fetching flight data
url = "https://www.admtl.com/en-CA/webruntime/api/apex/execute?language=en-CA&asGuest=true&htmlEncode=false"

headers = {
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://www.admtl.com/en-CA/flights/departures",
    "Origin": "https://www.admtl.com",
    "Accept": "/",
}



payload = {
    "namespace": "",
    "classname": "@udd/01pMm00000AWKuH",
    "method": "getFlights",
    "isContinuation": False,
    "params": {
        "language": "en-CA",
        "page": "departures"
    },
    "cacheable": False
}


def fetch_flight_data(url):
    print("[flight_analytics] Starting flight data fetch...")
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
    print("[flight_analytics] Initial GET to departures page...")
    scraper.get("https://www.admtl.com/en-CA/flights/departures")

    print("[flight_analytics] Sending POST request for flights...")
    # IMPORTANT: send the payload as JSON, do NOT pre-dump it (browser sends a JSON object, not a JSON string)
    response = scraper.post(url, json=payload, headers=headers)
    print(f"[flight_analytics] Response received with status code: {response.status_code}")
    if response.status_code != 200:
        print("[flight_analytics] Non-200 response body (truncated):")
        try:
            print(response.text[:1000])
        except Exception:
            print("[flight_analytics] Unable to print response text.")
    response.raise_for_status()
    print("[flight_analytics] Flight data fetch successful.")
    return response

def parse_json_content(response_content):
    print("[flight_analytics] Parsing JSON content...")
    return json.loads(response_content)

def format_json_data(json_data):
    print("[flight_analytics] Formatting JSON data...")
    return json.dumps(json_data, indent=4)

def convert_to_dataframe(json_data, key='returnValue', section='flightsForToday'):
    print(f"[flight_analytics] Converting JSON to DataFrame (key='{key}', section='{section}')...")
    df = pd.json_normalize(json_data[key][section])
    print(f"[flight_analytics] DataFrame created with {len(df)} rows.")
    return df


def extract_flight_data_excel(file_path="monthly_flights.xlsx"):
    print(f"[flight_analytics] Reading Excel file: {file_path}")
    df = pd.read_excel(file_path, skiprows=5)
    print(f"[flight_analytics] Raw rows loaded from Excel: {len(df)}")
    
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
    print("[flight_analytics] Created combined 'Flight number' column.")
    
    international_df = df[df["Terminal"] == "I"].reset_index(drop=True)
    print(f"[flight_analytics] Filtered international flights: {len(international_df)} rows.")

    international_df.index = international_df.index + 1
    
    extracted_df = international_df[["Date", "time", "Flight number", "Destination"]]
    print(f"[flight_analytics] Final extracted DataFrame shape: {extracted_df.shape}")
    
    return extracted_df

def unique_international_dest(df):
    print("[flight_analytics] Calculating unique international destinations...")
    data = df['Destination']
    unique_destinations = set(data)
    print(f"[flight_analytics] Found {len(unique_destinations)} unique destinations.")
    return unique_destinations


if _name_ == "_main_":
    """
    Simple sanity check when running this script directly.
    It will try to fetch today's flights, print basic info,
    and save the results to an Excel file.
    """
    print("[flight_analytics] Script started as _main_.")
    try:
        response = fetch_flight_data(url)
        json_data = parse_json_content(response.content)
        df = convert_to_dataframe(json_data)
        print(f"[flight_analytics] Sanity check: fetched {len(df)} flights for today.")

        # Save to Excel so you can inspect the data easily
        output_file = "flights_today.xlsx"
        df.to_excel(output_file, index=False)
        print(f"[flight_analytics] Saved flights to Excel file: {output_file}")
    except Exception as e:
        print(f"[flight_analytics] ERROR while running sanity check: {e}")