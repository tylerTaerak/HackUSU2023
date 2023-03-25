import requests
import datetime
import pandas as pd


def getAirportInfo():
    with open("airports.csv", "r") as handle:
        df = pd.read_csv(handle, index_col='IATA')
    return df


FLIGHT_COLS = [
        'DEP_DEL15',
        'DEPARTING_AIRPORT',
        'LATITUDE',
        'LONGITUDE',
        'PRCP',
        'SNOW',
        'SNWD',
        'TMAX',
        'AWND'
        ]


def getHistoricFlightData():
    with open("full_data_flightdelay.csv", "r") as handle:
        df = pd.read_csv(handle, usecols=FLIGHT_COLS)

    df['DEPARTING_AIRPORT'] = df['DEPARTING_AIRPORT'].str.replace(' Airport', '')
    return df


def getFlightInfo(flight_no : str, target_date : datetime.datetime) -> dict:
    date_formatted = target_date.strftime("%Y-%m-%d")
    url = f"https://aerodatabox.p.rapidapi.com/flights/number/{flight_no}/{date_formatted}"

    querystring = {"withAircraftImage":"false","withLocation":"false"}

    headers = {
        "X-RapidAPI-Key": "3e0d295e86msh9de57d9cb1d10d6p10295cjsn454e1f232977",
        "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()
