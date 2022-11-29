from weather_api_service import Weather, WeatherType
from geolocation import Geolocation, Coordinates
import formatter


class TestFormatter:
    def test_format_weather(self):
        weather = Weather(
            temperature=-2,
            wind_speed=11,
            weather_type=WeatherType.CLOUDY,
            geolocation=Coordinates(latitude=59.898617,
                                    longitude=30.26538)
        )

        geo = Geolocation(
            Coordinates(latitude=39.03, longitude=-77.5),
            country='США',
            region='Вирджиния',
            city='Ашберн',
            zip='20149'
        )

        assert formatter.format_weather(weather, geo) == """Место: Ашберн, Вирджиния, США, 20149
Температура: -2 °С
Ветер: 11 м/с
Погода: Облачно"""