import requests
import datetime
import joblib
from weather import getWeatherForecast


def loadParams():
    airports = joblib.load('trainingData/airports.pkl')
    carriers = joblib.load('trainingData/carriers.pkl')

    return airports, carriers


def convertAirportToInt(name, map):
    conversion = map[map['DEPARTING_AIRPORT'] == name]
    return conversion['DEPARTING_AIRPORT_int_label'] if conversion.size > 0 else 0


def convertCarrierToInt(name, map):
    conversion = map[map['CARRIER_NAME'] == name]
    return conversion['CARRIER_NAME_int_label'] if conversion.size > 0 else 0


def getFlightInfo(flight_no : str) -> list:
    url = f"https://aerodatabox.p.rapidapi.com/flights/number/{flight_no}"

    querystring = {"withAircraftImage":"false","withLocation":"true"}

    headers = {
        "X-RapidAPI-Key": "Insert key here",
        "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    # input has [MONTH, DAY OF WEEK, PRCP, SNOW, TMAX, AWND, CARRIER_NAME_int_label, DEPARTING_AIRPORT_int_label]
    response = response.json()[0]

    airports, carriers = loadParams()

    departing = response['departure']

    dName = departing['airport']['name']
    dDate = datetime.datetime.strptime(departing['scheduledTimeLocal'], "%Y-%m-%d %H:%M%z")

    output = [0 for i in range(8)]
    output[0] = dDate.month
    output[1] = int(dDate.strftime('%w')) + 1

    weather = getWeatherForecast(dDate, departing['airport']['iata'])
    weather = weather['daily']

    output[2] = weather['precipitation_sum'][0]
    output[3] = weather['snowfall_sum'][0]
    output[4] = weather['temperature_2m_max'][0]
    output[5] = weather['windspeed_10m_max'][0]

    output[6] = convertCarrierToInt(response['airline']['name'], carriers)  # convert to int label
    output[7] = convertAirportToInt(dName, airports)                        # convert to int label

    return [output]


if __name__ == '__main__':
    flight_no = 'DL56'
    date = datetime.datetime(year=2023, month=3, day=26)
    print(getFlightInfo(flight_no, date))
