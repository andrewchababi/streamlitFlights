import json
import pandas as pd
import cloudscraper
import streamlit as st

# Define the URL and payload for fetching flight data
url = "https://www.admtl.com/en-CA/webruntime/api/apex/execute?language=en-CA&asGuest=true&htmlEncode=false"

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
    response = cloudscraper.create_scraper().post(url, json=payload)
    response.raise_for_status()
    return response

def parse_json_content(response_content):
    return json.loads(response_content)

def format_json_data(json_data):
    return json.dumps(json_data, indent=4)

def convert_to_dataframe(json_data, key='returnValue', section='flightsForToday'):
    df = pd.json_normalize(json_data[key][section])
    return df 


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
    new_df['Gate'] = new_df['Gate'].str.extract('(\d+)')  # Extract digits
    new_df = new_df.dropna()
    new_df['Gate'] = new_df['Gate'].astype(int)
    return new_df
