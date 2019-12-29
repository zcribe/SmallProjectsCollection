from time import time, sleep
from math import floor

TIME_WORK = 25
TIME_REST = 5
TIME_REST_LONG = 30
ONE_MINUTE = 60
SESSIONS_WORK_MAX = 4


def run():
    target_minutes = TIME_WORK
    work_sessions = 0
    started = False

    while True:
        if target_minutes == TIME_WORK and work_sessions >= SESSIONS_WORK_MAX and started:
            target_minutes = TIME_REST_LONG
        elif target_minutes == TIME_WORK and started:
            target_minutes = TIME_REST
            work_sessions += 1
        elif not started:
            started = True
        else:
            target_minutes = TIME_WORK

        timer(target_minutes)


def timer(target_minutes):
    time_target = create_target_time(target_minutes)
    while time() < time_target:
        tick(time_target)
        sleep(1)
    return target_minutes


def tick(time_target):
    time_left = time_target - time()
    minutes = floor(time_left / ONE_MINUTE)
    seconds = round(time_left - minutes * ONE_MINUTE)
    print(f"{minutes}:{seconds}")


def create_target_time(target_minutes):
    return time() + target_minutes * ONE_MINUTE
