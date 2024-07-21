import pytest
import main


def test_get_laptime():
    session = "9161"
    driver = "16"
    lap_num = "7"
    lap = main.Lap(session, driver)
    lap.lap_num = lap_num
    lap.get_lap()
    lap_time = float(lap.lap_time)
    assert lap_time == 255.224
    assert lap.lap_num == 7
    assert lap.lap_time_s1 == 149.986
    assert lap.lap_time_s2 == 49.206
    assert lap.lap_time_s3 == 56.032
    assert lap.outlap is True
