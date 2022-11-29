import json
from pytest import fixture

import geolocation
from config import IP_API_URL, IP_API_LANG


@fixture
def get_ip():
    return '8.8.8.8'


@fixture
def get_response():
    return """{
  "query": "8.8.8.8",
  "status": "success",
  "country": "США",
  "countryCode": "US",
  "region": "VA",
  "regionName": "Вирджиния",
  "city": "Ашберн",
  "zip": "20149",
  "lat": 39.03,
  "lon": -77.5,
  "timezone": "America/New_York",
  "isp": "Google LLC",
  "org": "Google Public DNS",
  "as": "AS15169 Google LLC"
}"""


@fixture
def get_geolocation():
    return geolocation.Geolocation(
            geolocation.Coordinates(latitude=39.03, longitude=-77.5),
            country='США',
            region='Вирджиния',
            city='Ашберн',
            zip='20149'
        )


@fixture
def mock_response(monkeypatch, get_response):
    """ _get_coordinates_by_ip_response mocked to return certain response by fixture get_response """
    def mock__get_coordinates_by_ip_response(ip: str = ''):
        return get_response

    monkeypatch.setattr(geolocation,
                        '_get_coordinates_by_ip_response',
                        mock__get_coordinates_by_ip_response)


class TestGeolocationAPI:
    def test__get_geolocation_api_url(self, get_ip):
        ip = get_ip

        assert geolocation._get_geolocation_api_url(ip) == IP_API_URL + ip + '?lang=' + IP_API_LANG
        assert geolocation._get_geolocation_api_url() == IP_API_URL + '?lang=' + IP_API_LANG

    def test__get_coordinates_by_ip_response(self):
        response = geolocation._get_coordinates_by_ip_response()
        assert len(response) > 0

    def test_mock__get_coordinates_by_ip_response(self, mock_response, get_response):
        assert geolocation._get_coordinates_by_ip_response() == get_response

    def test__parse_coordinates_by_ip_response(self):
        response = geolocation._get_coordinates_by_ip_response()
        json_response = json.loads(response)

        assert 'country' in json_response
        assert 'regionName' in json_response
        assert 'city' in json_response
        assert 'zip' in json_response
        assert 'lat' in json_response
        assert 'lon' in json_response
        assert isinstance(geolocation._parse_coordinates_by_ip_response(response),
                          geolocation.Geolocation)

    def test_get_geolocation_by_ip(self, get_ip, get_geolocation):
        api_geo = geolocation.get_geolocation_by_ip(get_ip)

        assert isinstance(api_geo, geolocation.Geolocation)
        assert api_geo == get_geolocation

    def test_get_geolocation(self, mock_response, get_geolocation):
        api_geo = geolocation.get_geolocation()

        assert isinstance(api_geo, geolocation.Geolocation)
        assert api_geo == geolocation.get_geolocation_by_ip()
        assert api_geo == get_geolocation
