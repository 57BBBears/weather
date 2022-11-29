import pytest
import json
import weather_api_service as was
from geolocation import Coordinates
from exceptions import WeatherApiServiceError


@pytest.fixture
def get_coordinates():
    return Coordinates(latitude=59.898617, longitude=30.26538)


@pytest.fixture
def get_api_response():
    return b"""{
    "latitude":59.898617,
    "longitude":30.26538,
    "generationtime_ms":0.26798248291015625,
    "utc_offset_seconds":0,
    "timezone":"GMT",
    "timezone_abbreviation":"GMT",
    "elevation":4.0,
    "current_weather":{
    "temperature":-1.8,
    "windspeed":10.8,
    "winddirection":111.0,
    "weathercode":3,
    "time":"2022-11-29T10:00"
    }
    }
    """


@pytest.fixture
def get_cur_weather():
    return was.Weather(
            temperature=-2,
            wind_speed=11,
            weather_type=was.WeatherType.CLOUDY,
            geolocation=Coordinates(latitude=59.898617,
                                    longitude=30.26538)
        )


@pytest.fixture
def mock_api_response(monkeypatch, get_api_response):
    def mock__get_weather_by_coordinates_response(latitude: float, longitude: float) -> bytes:
        return get_api_response

    monkeypatch.setattr(was,
                        '_get_weather_by_coordinates_response',
                        mock__get_weather_by_coordinates_response)


class TestWeatherApiService:
    def test_get_weather(self, get_coordinates):
        cur_weather = was.get_weather(get_coordinates)
        assert isinstance(cur_weather, was.Weather)
        assert cur_weather.geolocation == get_coordinates

    def test_mock_get_weather(self, mock_api_response, get_cur_weather, get_coordinates):
        cur_weather = was.get_weather(get_coordinates)
        assert was.get_weather(get_coordinates) == get_cur_weather

    def test_get_weather_by_coordinates(self, get_coordinates):
        coords = get_coordinates
        cur_weather = was.get_weather_by_coordinates(coords)
        assert isinstance(cur_weather, was.Weather)

    def test_mock_get_weather_by_coordinates(self, mock_api_response, get_cur_weather, get_coordinates):
        coords = get_coordinates
        assert was.get_weather_by_coordinates(coords) == get_cur_weather

    def test__get_weather_by_coordinates_response(self):
        weather_api_response = was._get_weather_by_coordinates_response(59.898617, 30.26538)
        weather_api_json = json.loads(weather_api_response)
        cur_weather = weather_api_json['current_weather']
        assert 'temperature' in cur_weather
        assert 'windspeed' in cur_weather
        assert 'weathercode' in cur_weather
        assert 'latitude' in weather_api_json
        assert 'longitude' in weather_api_json

    def test__parse_weather_by_coordinates_response(self, get_api_response, get_cur_weather):
        assert was._parse_weather_by_coordinates_response(get_api_response) == get_cur_weather

    def test_get_weather_interpretation_by_code(self):
        for code in range(-1, 101):
            if code == 0:
                weather_type = was.WeatherType.CLEAR
            elif code < 4:
                weather_type = was.WeatherType.CLOUDY
            elif code < 49:
                weather_type = was.WeatherType.FOG
            elif code < 58:
                weather_type = was.WeatherType.DRIZZLE
            elif code < 66:
                weather_type = was.WeatherType.RAIN
            elif code < 78:
                weather_type = was.WeatherType.SNOW
            elif code < 100:
                weather_type = was.WeatherType.THUNDERSTORM
            else:
                with pytest.raises(WeatherApiServiceError):
                    was.get_weather_interpretation_by_code(code)
                continue

            assert was.get_weather_interpretation_by_code(code) == weather_type
