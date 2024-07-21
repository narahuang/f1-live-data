import requests
import time

all_messages = []

while True:
    time.sleep(10)
    try:
        response = requests.get(
            'https://api.openf1.org/v1/race_control?session_key=latest',
            timeout=30)
        race_control_data = response.json()
    except Exception:
        continue

    for item in race_control_data:
        if item['message'] not in all_messages:
            print(f"{item['date']}\t{item['message']}")
            all_messages.append(item['message'])
