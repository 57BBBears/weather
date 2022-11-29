import json
from json.decoder import JSONDecodeError
from typing import Union
from dataclasses import dataclass
from enum import Enum
import urllib.parse
import urllib.request
from urllib.error import URLError

from geolocation import Coordinates
from config import WEATHER_API_URL
from exceptions import WeatherApiServiceError


class WeatherType(str, Enum):
    CLEAR = 'Ясно'
    CLOUDY = 'Облачно'
    DRIZZLE = 'Изморось'
    FOG = 'Туман'
    RAIN = 'Дождь'
    SNOW = 'Снег'
    THUNDERSTORM = 'Гроза'


@dataclass(frozen=True)
class Weather:
    temperature: int
    wind_speed: int
    weather_type: WeatherType
    geolocation: Coordinates


def get_weather(place: Union[str, Coordinates]) -> Weather:
    """ Get weather by coordinates, address (in future)"""
    return get_weather_by_coordinates(place)


def get_weather_by_coordinates(coordinates: Coordinates) -> Weather:
    """ Get weather by coordinates in open meteo """
    response = _get_weather_by_coordinates_response(coordinates.latitude, coordinates.longitude)
    return _parse_weather_by_coordinates_response(response)


def _get_weather_by_coordinates_response(latitude: float, longitude: float) -> bytes:
    url = _get_weather_api_url(latitude, longitude)
    try:
        return urllib.request.urlopen(url).read()
    except URLError as exp:
        raise WeatherApiServiceError from exp


def _get_weather_api_url(latitude: float, longitude: float) -> str:
    url = WEATHER_API_URL
    get_params = urllib.parse.urlencode({'latitude': latitude,
                                         'longitude': longitude,
                                         'current_weather': True,
                                         'windspeed_unit': 'ms'})
    url += '?' + get_params

    return url


def _parse_weather_by_coordinates_response(json_response: str) -> Weather:
    try:
        dict_response = json.loads(json_response)
        current_weather = dict_response['current_weather']

        return Weather(
            temperature=round(current_weather['temperature']),
            wind_speed=round(current_weather['windspeed']),
            weather_type=get_weather_interpretation_by_code(current_weather['weathercode']),
            geolocation=Coordinates(latitude=dict_response['latitude'],
                                    longitude=dict_response['longitude'])
        )
    except (JSONDecodeError, KeyError) as exc:
        raise WeatherApiServiceError from exc


def get_weather_interpretation_by_code(code: int) -> WeatherType:
    if code == 0:
        weather_type = WeatherType.CLEAR
    elif code < 4:
        weather_type = WeatherType.CLOUDY
    elif code < 49:
        weather_type = WeatherType.FOG
    elif code < 58:
        weather_type = WeatherType.DRIZZLE
    elif code < 66:
        weather_type = WeatherType.RAIN
    elif code < 78:
        weather_type = WeatherType.SNOW
    elif code < 100:
        weather_type = WeatherType.THUNDERSTORM
    else:
        raise WeatherApiServiceError

    return weather_type
