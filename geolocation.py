from dataclasses import dataclass
import json
from json.decoder import JSONDecodeError
import urllib.request
import urllib.parse
from urllib.error import URLError

from config import IP_API_URL, IP_API_LANG
from exceptions import GeolocationApiServiceError


@dataclass(frozen=True)
class Coordinates:
    """Coordinates data class with latitude and longitude"""
    latitude: float
    longitude: float


@dataclass(frozen=True)
class Geolocation:
    """Geolocation data class with coordinates and address"""
    coordinates: Coordinates
    country: str
    region: str
    city: str
    zip: str


def get_geolocation() -> Geolocation:
    """
    Return coordinates and geolocation info
    :return: Geolocation
    :rtype: Geolocation
    """
    return get_geolocation_by_ip()


def get_geolocation_by_ip(ip: str = '') -> Geolocation:
    """
    Get geolocation by geo api.
    :param str ip: ip address for check, default is empty (current ip).
    :return: Geolocation of ip
    :rtype: Geolocation
    """
    response = _get_coordinates_by_ip_response(ip)

    return _parse_coordinates_by_ip_response(response)


def _get_coordinates_by_ip_response(ip: str = '') -> str:
    url = _get_geolocation_api_url(ip)

    try:
        return urllib.request.urlopen(url).read()
    except URLError as exp:
        raise GeolocationApiServiceError from exp


def _get_geolocation_api_url(ip: str = '') -> str:
    ip = urllib.parse.quote_plus(str(ip)) if ip else ''
    params = {}
    if IP_API_LANG:
        params['lang'] = IP_API_LANG

    get_params = urllib.parse.urlencode(params) if params else ''

    return IP_API_URL + ip + '?' + get_params


def _parse_coordinates_by_ip_response(json_response: str) -> Geolocation:
    try:
        dict_response = json.loads(json_response)

        return Geolocation(
            coordinates=Coordinates(latitude=dict_response['lat'], longitude=dict_response['lon']),
            country=dict_response['country'],
            region=dict_response['regionName'],
            city=dict_response['city'],
            zip=dict_response['zip']
        )
    except (JSONDecodeError, KeyError) as exp:
        raise GeolocationApiServiceError from exp
