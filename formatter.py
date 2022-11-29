from weather_api_service import Weather
from geolocation import Geolocation


def format_weather(weather: Weather, geo: Geolocation) -> str:
    geolocation = ', '.join([geo.city, geo.region, geo.country, geo.zip])
    return format_console(weather, geolocation)


def format_console(weather: Weather, geo: str) -> str:
    return f"""Место: {geo}
Температура: {weather.temperature} °С
Ветер: {weather.wind_speed} м/с
Погода: {weather.weather_type}"""
