from time import time, sleep
from math import floor

TIME_WORK = 25
TIME_REST = 5
TIME_REST_LONG = 30
ONE_MINUTE = 60
SESSIONS_WORK_MAX = 4


class Pomodoro():
    def __init__(self):
        self.state = 'work'
        self.work_sessions = 0
        self.goal = time() + TIME_WORK * ONE_MINUTE

    def run(self):
        self.timer()

    def timer(self, testing=False):
        time_target = self.goal
        while time() < time_target:
            self._tick()
            if not testing:
                sleep(1)
        self._state_manager()

    def _tick(self):
        time_left = self.goal - time()
        minutes = floor(time_left / ONE_MINUTE)
        seconds = round(time_left - minutes * ONE_MINUTE)
        print(f"{self.state.capitalize()} - {minutes}:{seconds}")

    def _set_goal(self, target):
        self.goal = time() + target * ONE_MINUTE

    def _state_manager(self):
        if self.work_sessions >= SESSIONS_WORK_MAX:
            self.state = 'rest_long'
            self._set_goal(TIME_REST_LONG)
        elif self.state == 'work':
            self.state = 'rest'
            self._set_goal(TIME_REST)
        else:
            self.state = 'work'
            self._set_goal(TIME_WORK)

        self.run()

Pomodoro().run()