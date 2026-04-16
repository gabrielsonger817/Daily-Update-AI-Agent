import requests
from typing import Dict

from config import OPENWEATHER_API_KEY, MY_CITY, MY_COUNTRY_CODE


def get_weather() -> Dict:
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": f"{MY_CITY},{MY_COUNTRY_CODE}",
        "appid": OPENWEATHER_API_KEY,
        "units": "imperial",
        "cnt": 8,  # 24-hour window in 3-hour slots
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    slots = data["list"]
    current = slots[0]
    temps = [s["main"]["temp"] for s in slots]
    max_precip = round(max(s.get("pop", 0) for s in slots) * 100)

    return {
        "city": MY_CITY,
        "current_temp": round(current["main"]["temp"]),
        "feels_like": round(current["main"]["feels_like"]),
        "high": round(max(temps)),
        "low": round(min(temps)),
        "description": current["weather"][0]["description"].capitalize(),
        "humidity": current["main"]["humidity"],
        "wind_speed": round(current["wind"]["speed"]),
        "precipitation_chance": max_precip,
    }
