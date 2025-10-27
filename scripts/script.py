import json
import pandas as pd
import cloudscraper
import streamlit as st

# Define the URL and payload for fetching flight data
url = "https://www.admtl.com/en-CA/webruntime/api/apex/execute?language=en-CA&asGuest=true&htmlEncode=false"

headers = {
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://www.admtl.com/en-CA/flights/departures",
    "Origin": "https://www.admtl.com",
    "Accept": "*/*",
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
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
    scraper.get("https://www.admtl.com/en-CA/flights/departures")

    # response = cloudscraper.create_scraper().post(url,headers=headers, json=payload)
    response = scraper.post(url, json=json.dumps(payload), headers=headers)
    response.raise_for_status()
    return response

def parse_json_content(response_content):
    return json.loads(response_content)

def format_json_data(json_data):
    return json.dumps(json_data, indent=4)

def convert_to_dataframe(json_data, key='returnValue', section='flightsForToday'):
    return pd.json_normalize(json_data[key][section])

@st.cache_data(ttl=3600)
def process_flights_to_df(url):
    response = fetch_flight_data(url)
    print(f"HTTP Status Code: {response.status_code}")

    raw_data = response.content
    structured_data = parse_json_content(raw_data)

    flights_df = convert_to_dataframe(structured_data)

    flights_df.rename(columns={
        'TerminalGate': 'Gate',
        'FormattedScheduledTime': 'time',
        'FormattedUpdatedTime': 'updatedTime',
        'OperationalStatusDescription': 'Status',
        'PublicDisplayFlightNumber' : 'Flight number',
    }, inplace=True)

    new_columns_of_interest = ['AirlineName', 'Gate', 'time', 'updatedTime', 'AirportName', 'Status', 'Flight number']
    new_df = flights_df[new_columns_of_interest]

    new_df = new_df.copy()
    new_df['Gate'] = new_df['Gate'].str.extract('(\\d+)')  # Extract digits
    new_df = new_df.dropna()
    new_df['Gate'] = new_df['Gate'].astype(int)

    return new_df

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
    
    extracted_df = international_df[["Date", "time", "Flight number", "Destination"]]
    
    return extracted_df

def unique_international_dest(df):

    data = df['Destination']

    unique_destinations = set(data)

    return unique_destinations