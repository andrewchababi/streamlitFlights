import pandas as pd
from monthly_flight_scripts import extract_flight_data_excel

flight_aircraft_mapping = {
    "Boeing 787-9 Dreamliner": [
        "TK36", "RJ272", "AC1884", "AC812", "AT209", "AC844", "AC975", "AC50",
        "AC870", "AC884", "AC96", "AC959", "AC876", "AC878"
    ],
    "Airbus A320": [
        "TS738", "AC995", "WG7292", "TS384", "TS328", "TS938", "AC866", "TS152",
        "TS196", "TS572", "AF347", "AC832", "TS890", "TS198", "TS102", "WG6544",
        "TS484", "WG2548", "TS204", "TS498", "TS394", "TS106", "AF345", "TS680",
        "TS760", "AC50", "OS74", "WG2876", "WG4534", "AC876", "TS340", "WG7590",
        "AC944", "TS758", "AC1321", "AC894", "WG268", "WG6828", "WG5263",
        "AC1874", "AC938", "TS712", "AC414", "TS974", "TS284", "TS814", "TS856",
        "AC999", "WG774", "WG2881", "TS218", "TS452", "TS250", "TS356", "WG5619",
        "TS434", "WG6204", "TS604", "AC848", "AC920", "TS110"
    ],
    "Airbus A321": [
        "TS328", "TS938", "AC866", "TS934", "TS572", "TS600", "TS198", "TS102",
        "AC922", "TS484", "TS498", "AC1884", "TS106", "TS680", "TS760", "TS538",
        "TS340", "TS684", "TS110", "AC915", "TS894", "AC1331", "TS150", "TS852",
        "TS284", "AC940", "TS856", "TS814", "TS218", "TS356", "TS434", "TS480",
        "TS398", "TS320", "TS372", "TS890"
    ],
    "Boeing 737-800": [
        "BA94", "TS184", "WG519", "AC1792", "WG4428", "CM484", "WG2876", "AC876",
        "AC944", "AC844", "QR764", "WG4426", "WG5477", "WG764", "WG5463", "TS402",
        "TS398", "WG6404", "TS890"
    ],
    "Embraer E190": [
        "AM681", "AC50"
    ],
    "Airbus A380": [
        "EK244"
    ],
    "Boeing 737 MAX 8": [
        "WG2548", "WG6552", "WG5357", "WG4534", "WG7590", "WG6544", "WG774", "TS890"
    ],
    "Boeing 747-8": [
        "AC1800"
    ],
    "Boeing 747-400": [
        "QR764"
    ],
    "Airbus A350-900": [
        "LH475"
    ],
    "Airbus A350-1000": [
        "BA94"
    ],
    "Boeing 777-300ER": [
        "QR764"
    ],
    "Airbus A330-300": [
        "AC832", "AC822", "AC834"
    ]
}

aircraft_capacity = {
    "Boeing 787-9 Dreamliner": 296,  # Typical capacity
    "Airbus A320": 180,  # Typical capacity
    "Airbus A321": 220,  # Typical capacity
    "Boeing 737-800": 189,  # Typical capacity
    "Embraer E190": 114,  # Typical capacity
    "Airbus A380": 853,  # Maximum capacity
    "Boeing 737 MAX 8": 178,  # Typical capacity
    "Boeing 747-8": 524,  # Maximum capacity
    "Boeing 747-400": 416,  # Maximum capacity
    "Airbus A319": 140,  # Smaller version of the A320, used for short-haul
    "Airbus A330": 300,  # Wide-body aircraft for long-haul flights
    "Airbus A340": 250,  # Wide-body, long-range airliner
    "Airbus A350": 300,  # Newer, long-range wide-body aircraft
    "Boeing 737-700": 140,  # Smaller version of the 737
    "Boeing 757-200": 200,  # Narrow-body, medium- to long-haul
    "Boeing 767-300": 240,  # Wide-body, medium- to long-haul
    "Boeing 777-200": 314,  # Wide-body, long-range aircraft
    "Boeing 777-300": 396,  # Larger version of the 777
    "Boeing 787-8": 242,  # Dreamliner, known for fuel efficiency, long-haul
    "Boeing 787-10": 330,  # Longest version of the Dreamliner series
    "Boeing 717": 100,  # Smaller, regional aircraft
    "Embraer E175": 88,  # Regional jet for short flights
    "Embraer E195": 124,  # Larger version of the E190
    "Bombardier CRJ200": 50,  # Regional aircraft
    "Bombardier CRJ700": 70,  # Larger regional aircraft
    "Bombardier CRJ900": 90,  # Bigger version of the CRJ700
    "Bombardier Q400": 78,  # Turboprop regional aircraft
    "ATR 72": 70,  # Small turboprop for regional flights
    "Mitsubishi MRJ90": 92,  # New regional jet from Mitsubishi
    "Sukhoi Superjet 100": 108,  # Russian regional jet
    "Antonov An-124": 650,  # Huge cargo aircraft, can carry passengers too
    "Lockheed L-1011 TriStar": 250,  # Older wide-body, used for medium- and long-haul
    "McDonnell Douglas MD-80": 160,  # Narrow-body, medium-haul aircraft
    "McDonnell Douglas MD-90": 160,  # Slightly newer version of the MD-80
    "Convair 880": 110,  # Older narrow-body aircraft
    "Douglas DC-9": 100,  # Older narrow-body aircraft, now retired
    "Douglas DC-10": 250,  # Wide-body, used for medium- and long-haul
    "Lockheed Constellation": 65,  # Vintage wide-body aircraft
}

load_factors_by_airline = {
    # Major North American Airlines
    "AC": 0.85,     # Air Canada
    "AA": 0.85,     # American Airlines
    "DL": 0.85,     # Delta Air Lines
    "UA": 0.85,     # United Airlines
    "WN": 0.90,     # Southwest Airlines
    "B6": 0.85,     # JetBlue Airways
    "AS": 0.85,     # Alaska Airlines
    "NK": 0.90,     # Spirit Airlines

    # European Airlines
    "BA": 0.85,     # British Airways
    "LH": 0.90,     # Lufthansa
    "AF": 0.85,     # Air France
    "KL": 0.85,     # KLM
    "FR": 0.90,     # Ryanair
    "U2": 0.85,     # EasyJet
    "IB": 0.85,     # Iberia
    "SK": 0.80,     # SAS (Scandinavian Airlines)
    "AY": 0.85,     # Finnair

    # Middle Eastern Airlines
    "EK": 0.40,     # Emirates (Updated to 40%)
    "QR": 0.40,     # Qatar Airways (Updated to 40%)
    "EY": 0.85,     # Etihad Airways
    "WY": 0.85,     # Oman Air

    # Asian Airlines
    "SQ": 0.85,     # Singapore Airlines
    "CX": 0.85,     # Cathay Pacific
    "TG": 0.80,     # Thai Airways
    "NH": 0.85,     # ANA (All Nippon Airways)
    "JL": 0.85,     # Japan Airlines
    "CZ": 0.75,     # China Southern Airlines
    "MU": 0.75,     # China Eastern Airlines
    "HU": 0.80,     # Hainan Airlines

    # Australian Airlines
    "QF": 0.85,     # Qantas
    "VA": 0.80,     # Virgin Australia

    # South American Airlines
    "LA": 0.80,     # LATAM Airlines
    "AV": 0.80,     # Avianca
    "G3": 0.85,     # Gol Linhas Aéreas

    # African Airlines
    "SA": 0.75,     # South African Airways
    "MS": 0.75,     # EgyptAir
    "ET": 0.80,     # Ethiopian Airlines

    # Low-Cost Carriers Worldwide
    "W6": 0.90,     # Wizz Air
    "DY": 0.85,     # Norwegian Air
    "AK": 0.85,     # AirAsia
    "6E": 0.85,     # IndiGo
    "JQ": 0.85,     # Jetstar Airways
    "TR": 0.80,     # Scoot
    "NK": 0.90,     # Spirit Airlines

    # Airlines with 40% load factor due to frequent no-shows
    "ALG": 0.40,    # Algerian Airlines
    "MA": 0.40,     # Moroccan Airlines
    "JO": 0.60      # Jordanian Airlines
}


flight_mappings_excel = {}

for aircraft, flights_list in flight_aircraft_mapping.items():
    for flight in flights_list:
        airline_code = flight[:2]  # The first two characters of the flight number
        load_factor = load_factors_by_airline.get(airline_code, 0.80)  # Default load factor if not found
        max_capacity = aircraft_capacity.get(aircraft, "Unknown Capacity")  # Max capacity for the aircraft

        # Ensure that max_capacity is a number and calculate the passengers
        if isinstance(max_capacity, int):
            passengers = round(max_capacity * load_factor)
        else:
            passengers = 188  # If the capacity is not found, mark as 188

        # Populate the dictionary with just flight number and estimated passengers
        flight_mappings_excel[flight] = passengers 

# flight_mappings_excel = {
#     "TS284": 166, "WG6146": 157, "TS890": 166, "F82100": 157, "WG378": 160,
#     "TS398": 169, "TS538": 174, "WG7188": 154, "CM484": 114, "WG4126": 154,
#     "AC944": 117, "AC1748": 149, "TS198": 166, "TS760": 164, "AC938": 123,
#     "AC954": 117, "EK244": 319, "AC962": 120, "AC948": 115, "AC1838": 139,
#     "WG5163": 154, "WG4134": 152, "WG7134": 154, "WG2189": 160, "AM681": 136,
#     "AC999": 149, "TS106": 169, "AC1004": 117, "TS938": 169, "TS498": 166,
#     "TS974": 164, "TS814": 164, "AC1884": 125, "LX87": 225, "AF345": 231,
#     "AC959": 125, "WG517": 157, "WG3106": 154, "AC844": 123, "AC874": 120,
#     "AC1792": 123, "OS74": 169, "AC995": 117, "AC832": 123, "TS196": 169,
#     "AC1275": 125, "AF347": 231, "KL672": 262, "AC866": 117, "TS110": 172,
#     "LH475": 261, "TS680": 166, "AC822": 125, "AC878": 115, "AC894": 141,
#     "AT209": 233, "BA94": 260, "QR764": 319, "AF4083": 120, "AC870": 115,
#     "S4328": 157, "AC876": 262, "TP254": 123, "AV201": 115, "RJ272": 233,
#     "WG604": 141, "WG525": 133, "WG2743": 141, "TS738": 166, "TS894": 164,
#     "TS356": 172, "AC922": 117, "WG434": 131, "AC1874": 120, "AC1450": 115,
#     "WG792": 131, "AC1325": 115, "AC920": 125, "WG537": 133, "WG428": 133,
#     "TS600": 172, "WG2789": 131, "AC1362": 117, "TS340": 169, "AF625": 231,
#     "AC5": 125, "AC1750": 125, "TS716": 164, "WG652": 136, "TS856": 164,
#     "AC781": 115, "TS602": 174, "AC892": 126, "TS252": 174, "AC50": 117,
#     "TK36": 260, "AC834": 125, "AC2076": 121, "AC96": 127, "AC2176": 110,
#     "WG6204": 133, "TS868": 172, "WG277": 133, "TS216": 172, "WG5237": 133,
#     "WG4228": 141, "AC1800": 123, "WG5219": 133, "AC1822": 115, "WG7292": 131,
#     "AC2196": 115, "WG5263": 133, "DM5961": 140, "WG6828": 136, "AH2701": 242,
#     "AC72": 115, "AC884": 120, "AC98": 120, "AC812": 117, "TS150": 172
# }
