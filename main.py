# openweathermap API call for historical data
# https://api.openweathermap.org/data/3.0/onecall/timemachine?
# lat={lat}&lon={lon}&dt={time}&appid={API key}

# Weather API:
# https://www.weatherapi.com/docs/
# 
# Historical data:
# https://api.weatherapi.com/v1/history.json?key=
# cb6a8215e8da403c86102517232503&q=<QUERYSTUFF>&dt=<OPTIONALDATENTIMESTUFF>&
# end_dt=<OPTIONALENDDATETIME>&unixend_dt=<OPTIONALUNIXDATETIMESTAMP>

# Opensky API:
# Installation: https://github.com/openskynetwork/opensky-api
# Docs: https://openskynetwork.github.io/opensky-api/python.html
'''
import opensky_api

apiObj = OpenSkyApi(username=<API username>, password=<API password>)
'''
from weather import *
from airports import *
import json
import datetime

def main():
    start = datetime.datetime(2022, 6, 1)
    end = datetime.datetime(2022, 6, 2)
    print(json.dumps(getHistoricalWeatherData(start, end, "ABI"), indent=4))

if __name__ == "__main__":
    main()


