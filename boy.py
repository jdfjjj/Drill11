import math
import time

from pico2d import load_image
from transitions import Machine


class AutoRun:
    SCREEN_WIDTH = 800

    def __init__(self, boy):
        self.boy = boy

    def enter(self):
        pass

    def exit(self):
        pass

    def do(self):
        next_x = self.boy.x + self.boy.face_dir * 5
        if next_x <= 50:
            self.boy.x = 50
            self.boy.face_dir = 1
        elif next_x >= self.SCREEN_WIDTH - 50:
            self.boy.x = self.SCREEN_WIDTH - 50
            self.boy.face_dir = -1
        else:
            self.boy.x = next_x
        self.boy.frame = (self.boy.frame + 1) % 8

    def draw(self):
        pass


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')
        self.auto_run = AutoRun(self)
        self.machine = Machine(
            model=self,
            states=['IDLE', 'RUN', 'SLEEP', 'AUTO_RUN'],
            initial='IDLE',
            auto_transitions=False,
            transitions=[
                {
                    'trigger': 'timeout',
                    'source': 'IDLE',
                    'dest': 'SLEEP',
                    'after': 'enter_sleep',
                },
                {
                    'trigger': 'start_run',
                    'source': ['IDLE', 'SLEEP'],
                    'dest': 'RUN',
                    'after': 'enter_run',
                },
                {
                    'trigger': 'start_auto_run',
                    'source': 'IDLE',
                    'dest': 'AUTO_RUN',
                    'after': 'enter_auto_run',
                },
                {
                    'trigger': 'stop_run',
                    'source': 'RUN',
                    'dest': 'IDLE',
                    'after': 'enter_idle',
                },
                {
                    'trigger': 'wake',
                    'source': 'SLEEP',
                    'dest': 'IDLE',
                    'after': 'enter_idle',
                },
            ],
        )
        self.idle_started_at = time.monotonic()

    def update(self):
        if self.state == 'IDLE':
            if time.monotonic() - self.idle_started_at >= 5:
                self.timeout()
                return
            self.frame = (self.frame + 1) % 8
        elif self.state == 'RUN':
            self.x = min(max(self.x + self.face_dir * 5, 50), 750)
            self.frame = (self.frame + 1) % 8
        elif self.state == 'AUTO_RUN':
            self.auto_run.do()

    def run_in_direction(self, direction):
        self.face_dir = direction
        if self.state in ('IDLE', 'SLEEP'):
            self.start_run()

    def stop_running(self):
        if self.state == 'RUN':
            self.stop_run()

    def enter_sleep(self):
        self.frame = 0

    def enter_run(self):
        self.frame = 0

    def enter_auto_run(self):
        self.auto_run.enter()

    def exit_auto_run(self):
        self.auto_run.exit()

    def enter_idle(self):
        self.frame = 0
        self.idle_started_at = time.monotonic()

    def draw(self):
        if self.state == 'AUTO_RUN':
            self.auto_run.draw()
        elif self.state == 'SLEEP':
            direction = 1 if self.face_dir == 1 else -1
            self.image.clip_composite_draw(
                0,
                300 if self.face_dir == 1 else 200,
                100,
                100,
                direction * math.pi / 2,
                '',
                self.x,
                self.y - 30,
                100,
                100,
            )
        elif self.state == 'RUN':
            if self.face_dir == 1:
                self.image.clip_draw(self.frame * 100, 100, 100, 100, self.x, self.y)
            else:
                self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
        elif self.state == 'IDLE':
            if self.face_dir == 1:
                self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
            else:
                self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)