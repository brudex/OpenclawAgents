#!/usr/bin/env python3
"""Get current weather in Accra, Ghana using wttr.in (no API key needed)."""

import json
import urllib.request


def get_weather(city="Accra"):
    url = f"https://wttr.in/{city}?format=j1"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    current = data["current_condition"][0]
    area = data["nearest_area"][0]

    location = area["areaName"][0]["value"]
    country = area["country"][0]["value"]

    temp_c = current["temp_C"]
    temp_f = current["temp_F"]
    feels_like_c = current["FeelsLikeC"]
    humidity = current["humidity"]
    wind_speed_kmph = current["windspeedKmph"]
    wind_dir = current["winddir16Point"]
    description = current["weatherDesc"][0]["value"]
    visibility = current["visibility"]
    uv_index = current["uvIndex"]

    print(f"Weather in {location}, {country}")
    print("=" * 40)
    print(f"  Condition   : {description}")
    print(f"  Temperature : {temp_c}°C / {temp_f}°F")
    print(f"  Feels Like  : {feels_like_c}°C")
    print(f"  Humidity    : {humidity}%")
    print(f"  Wind        : {wind_speed_kmph} km/h {wind_dir}")
    print(f"  Visibility  : {visibility} km")
    print(f"  UV Index    : {uv_index}")


if __name__ == "__main__":
    get_weather("Accra")
