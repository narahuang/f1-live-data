import requests
import time

while True:
    try:
        weather = requests.get(
            'https://api.openf1.org/v1/weather?session_key=latest',
            timeout=30)
    except Exception:
        continue

    weather_data = weather.json()
    weather_now = weather_data[-1]
    print(f"{weather_now['air_temperature']}\t{weather_now['track_temperature']}")
    time.sleep(120)
