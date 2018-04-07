import datetime as dt
import requests

from dateutil.parser import parse as parse_date
from scipy.interpolate import interp1d

import noaablocks.error as err


def _get_json_value():
    pass


def _make_request(url, **kwargs):
    try:
        result = requests.get(url, **kwargs)
    except requests.exceptions.ConnectionError:
        raise err.NotConnectedError
    except requests.ConnectionError:
        raise err.ServiceUnavailable(url)

    if result.status_code != 200:
        raise err.ServiceError(result.status_code, url)

    return result


def get_location():
    """Returns the lat/lon of the current location reported by freegeoip"""
    result = _make_request('https://freegeoip.net/json/')

    data = result.json()

    return (data['latitude'], data['longitude'])


def get_hourly_forecast(lat, lon):
    """Returns json from noaa"""
    url = 'https://api.weather.gov/points/{lat},{lon}/forecast/hourly'.format(lat=lat, lon=lon)
    response = _make_request(url, headers={'Accept': 'application/vnd.noaa.dwml+json;version=1'})

    return response.json()


def _forecast_periods_to_datetime(periods):
    convert_keys = ['startTime', 'endTime']
    for period in periods:
        for convert_key in convert_keys:
            period[convert_key] = parse_date(period[convert_key])

    return periods


def get_current_temp(forecast):
    """Gets the n latest forecasts from the noaa forecast dictionary."""
    # periods is a list of dicts
    periods = forecast['properties']['periods']

    # Convert the forecast times into datetimes
    periods = _forecast_periods_to_datetime(periods)

    # TODO better error handling here.
    assert len(periods) > 0

    # Get the current datetime in the timezone used by the forecast.
    now = dt.datetime.now(tz=periods[0]['startTime'].tzinfo)

    datetimes = [p['startTime'].timestamp() for p in periods]
    temperatures = [p['temperature'] for p in periods]
    f = interp1d(datetimes, temperatures)

    current_temp = int(f(now.timestamp()))
    next_hour = now + dt.timedelta(hours=1)
    next_temp = int(f(next_hour.timestamp()))

    return current_temp, next_temp
