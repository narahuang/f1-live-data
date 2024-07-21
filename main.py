import requests
import argparse
import time

API_URL = "https://api.openf1.org/v1/laps"


# Get lap time and stores to a object
class Lap:

    def __init__(self, session, driver):
        self.session = session
        self.driver = driver
        self.lap = None
        self.lap_num = None
        self.lap_time = None
        self.lap_time_s1 = None
        self.lap_time_s2 = None
        self.lap_time_s3 = None
        self.outlap = False

    def get_lap(self):
        payload = {'session_key': str(self.session),
                   'driver_number': self.driver,
                   'lap_number': str(self.lap_num)}
        r = requests.get(url=API_URL, params=payload)
        rdata = r.json()
        self.lap = rdata[0]
        self.lap_num = self.lap['lap_number']
        self.lap_time = self.lap['lap_duration']
        self.lap_time_s1 = self.lap['duration_sector_1']
        self.lap_time_s2 = self.lap['duration_sector_2']
        self.lap_time_s3 = self.lap['duration_sector_3']
        self.outlap = self.lap['is_pit_out_lap']

    def get_current_lap_num(self):
        payload = {'session_key': 'latest', 'driver_number': self.driver}
        req = requests.get(url=API_URL, params=payload)
        reqdata = req.json()
        self.session = reqdata[0]['session_key']
        self.current_lap = reqdata[-1]
        self.current_lap_num = self.current_lap['lap_number']
        return int(self.current_lap_num)

    def get_laptime(self):
        if float(self.lap_time) > 60:
            minutes, seconds = divmod(self.lap_time, 60)
        return f"{int(minutes)}:{seconds:.3f}"


# Update every 1 minutes, and only show latest-1 lap
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--session', help="Session key \
                        (default: latest)", default='latest')
    parser.add_argument('-d', '--driver', help="Driver number", required=True)
    args = parser.parse_args()
    session = args.session
    driver = args.driver
    lap = Lap(session, driver)
    current_lap = lap.get_current_lap_num()
    if current_lap > 3:
        lap.lap_num = current_lap - 1
    else:
        return 0
    lap.get_lap()
    print(f"Driver {driver}\tLap {lap.lap_num}\tLapTime: {lap.get_laptime()}\t{lap.lap_time_s1}  {lap.lap_time_s2}  {lap.lap_time_s3}")
    printed_lap = lap.lap_num

    while True:
        time.sleep(60)
        current_lap = lap.get_current_lap_num()
        if current_lap < 3:
            continue
        if printed_lap >= current_lap - 1:
            continue
        else:
            lap.lap_num = current_lap - 1
            lap.get_lap()
            printed_lap = lap.lap_num           
            print(f"Driver {driver}\tLap {lap.lap_num}\tLapTime: {lap.get_laptime()}\t{lap.lap_time_s1}  {lap.lap_time_s2}  {lap.lap_time_s3}")


if __name__ == "__main__":
    main()
