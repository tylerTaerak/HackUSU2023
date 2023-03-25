# Historical data:
# https://api.weatherapi.com/v1/history.json?key=
# cb6a8215e8da403c86102517232503&q=<QUERYSTUFF>&dt=<OPTIONALDATENTIMESTUFF>&
# end_dt=<OPTIONALENDDATETIME>&unixend_dt=<OPTIONALUNIXDATETIMESTAMP>

# flight data api key: xIgsAA2Q1iJN38QCVQ566DJTGA0CahxO
# flight data secret key: osbBEgBxrDlNACqA
# base url: [ Base URL: test.api.amadeus.com/v1 ]

# flights.csv documentation: https://www.openintro.org/data/index.php?data=airline_delay

import requests
import datetime
import pandas as pd


def getAirportInfo():
    with open("airports.csv", "r") as handle:
        df = pd.read_csv(handle)
    return df


def getWeatherForecast(start_dt: datetime.datetime, airport_code : str) -> pd.DataFrame:
    formatted_start = start_dt.strftime("%Y-%m-%d")
    airportData = getAirportInfo()
    lat = airportData[airportData['IATA'] == airport_code]['LATITUDE'].values[0]
    lon = airportData[airportData['IATA'] == airport_code]['LONGITUDE'].values[0]

    # r = requests.get(f"https://archive-api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&start_date={formatted_start}&temperature_unit=fahrenheit&windspeed_units=mph&precipitation_units=inch&daily={','.join(PARAMS)}")
    # https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&daily=temperature_2m_max,precipitation_sum,snowfall_sum,windspeed_10m_max&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&forecast_days=1&start_date=2023-03-26&end_date=2023-03-26&timezone=America%2FDenver
    r = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&daily=temperature_2m_max,precipitation_sum,snowfall_sum,windspeed_10m_max&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&forecast_days=1&start_date={formatted_start}&end_date={formatted_start}&timezone=auto")
    data = r.json()

    return data
