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
import json
import pandas as pd
from airports import *

PARAMS = [
    "temperature_2m",
    "relativehumidity_2m",
    "dewpoint_2m",
    "apparent_temperature",
    "pressure_msl",
    "surface_pressure",
    "precipitation",
    "rain",
    "snowfall",
    "cloudcover",
    "cloudcover_low",
    "cloudcover_mid",
    "cloudcover_high",
    "shortwave_radiation",
    "direct_radiation",
    "direct_normal_irradiance",
    "diffuse_radiation",
    "windspeed_10m",
    "windspeed_100m",
    "winddirection_10m",
    "winddirection_100m",
    "windgusts_10m",
    "et0_fao_evapotranspiration",
    "weathercode",
    "vapor_pressure_deficit"
]

def getHistoricalWeatherData(start_dt : datetime.datetime, end_dt : datetime.datetime, airport_code : str) -> pd.DataFrame:
    formatted_start = start_dt.strftime("%Y-%m-%d")
    formatted_end = end_dt.strftime("%Y-%m-%d")
    airportData = getAirportInfo()
    lat = airportData[airportData['IATA'] == airport_code]['LATITUDE'].values[0]
    lon = airportData[airportData['IATA'] == airport_code]['LONGITUDE'].values[0]

    r = requests.get(f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={formatted_start}&end_date={formatted_end}&hourly={','.join(PARAMS)}")
    data = r.json()

    data = pd.json_normalize(data)
    return data


def getWeatherForecast(start_dt: datetime.datetime, end_dt: datetime.datetime, airport_code : str) -> pd.DataFrame:
    formatted_start = start_dt.strftime("%Y-%m-%d")
    formatted_end = end_dt.strftime("%Y-%m-%d")
    airportData = getAirportInfo()
    lat = airportData[airportData['IATA'] == airport_code]['LATITUDE'].values[0]
    lon = airportData[airportData['IATA'] == airport_code]['LONGITUDE'].values[0]

    r = requests.get(f"https://archive-api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&start_date={formatted_start}&end_date={formatted_end}&hourly={','.join(PARAMS)}")
    data = r.json()

    data = pd.json_normalize(data)
    return data


def writeDataToFile(data : dict) -> None:
    jsonObj = json.dumps(data)
    with open("data.json", "w") as handle:
        handle.write(jsonObj)


def main():
    pass

if __name__ == "__main__":
    main()