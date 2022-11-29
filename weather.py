import sys
from geolocation import get_geolocation, Coordinates
from weather_api_service import get_weather
from formatter import format_weather
from exceptions import GeolocationApiServiceError, WeatherApiServiceError


def main():
    try:
        geo = get_geolocation()
    except GeolocationApiServiceError:
        print("Can't get geolocation.")
        sys.exit(1)

    try:
        weather = get_weather(geo.coordinates)
    except WeatherApiServiceError:
        print("Can't get weather.")
        sys.exit(1)

    print(format_weather(weather, geo))


if __name__ == '__main__':
    main()
