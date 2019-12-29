from time import time, sleep
from math import floor
import argparse
import csv
import datetime

# Constants
TIME_WORK = 25
TIME_REST = 5
TIME_REST_LONG = 30
ONE_MINUTE = 60
SESSIONS_WORK_MAX = 4
LOOP_LIMIT = 9999

# Console
parser = argparse.ArgumentParser(description='===== Pomodoro timer CLI =====')
parser.add_argument('-wt', '-worktime', type=int, help=f'Minutes of work in a work sessions (default {TIME_WORK})',
                    default=TIME_WORK, nargs='?')
parser.add_argument('-rt', '-resttime', type=int, help=f'Minutes of rest in a rest sessions (default {TIME_REST})',
                    default=TIME_REST, nargs='?')
parser.add_argument('-rtl', '-resttimelong', type=int,
                    help=f'Minutes of rest in a long rest sessions (default {TIME_REST_LONG})',
                    default=TIME_REST_LONG, nargs='?')
parser.add_argument('-mws', '-maxworksessions', type=int,
                    help=f'Number of work sessions cycles before long rest session (default {SESSIONS_WORK_MAX})',
                    default=SESSIONS_WORK_MAX, nargs='?')
parser.add_argument('-ll', '-looplimit', type=int,
                    help=f'Maximum number of total sessions (default 9999)', default=LOOP_LIMIT, nargs='?')
parser.add_argument('-log', '-logsessions', type=bool,
                    help='Should sessions be logged (False)', default=False, nargs='?')

arguments = vars(parser.parse_args())
time_work = arguments['wt']
time_rest = arguments['rt']
time_rest_long = arguments['rtl']
sessions_work_max = arguments['mws']
loop_lim = arguments['ll']


# Core
def run():
    target_minutes = time_work
    work_sessions = 0
    started = False

    for _ in range(0, loop_lim):
        if target_minutes == time_work and work_sessions >= sessions_work_max and started:
            target_minutes = time_rest_long
        elif target_minutes == time_work and started:
            target_minutes = time_rest
            work_sessions += 1
        elif not started:
            started = True
        else:
            target_minutes = time_work

        timer(target_minutes)
        write_log(target_minutes)


def timer(target_minutes: int) -> int:
    time_target = create_target_time(target_minutes, time())
    while time() < time_target:
        tick(time_target)
        sleep(1)
    return target_minutes


def write_log(minutes: int, testing=False):
    with open('session_log.csv', 'w', newline='') as csvfile:
        log_writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        today = datetime.datetime.now(datetime.timezone.utc)
        log_writer.writerow([today, minutes])


def tick(time_target: float, broadcast=True):
    if broadcast:
        print(create_message(time_target))


def create_message(time_target: float) -> str:
    time_left = time_target - time()
    print(time())
    minutes = floor(time_left / ONE_MINUTE)
    seconds = round(time_left - minutes * ONE_MINUTE)
    message = f"{minutes}:{seconds}"
    return message


def create_target_time(target_minutes: int, current_time: float) -> float:
    return current_time + target_minutes * ONE_MINUTE


if __name__ == "__main__":
    run()
