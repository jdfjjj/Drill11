from pico2d import *

from grass import Grass # grass.py에서 정의한 Grass 클래스를 가져옴
from boy import Boy # boy.py에서 정의한 Boy 클래스를 가져옴


def a_down(event):
    return event.type == SDL_KEYDOWN and event.key == SDLK_a


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif (
            event.type == SDL_KEYDOWN
            and event.key == SDLK_SPACE
            and boy.state == 'SLEEP'
        ):
            boy.wake()
        elif a_down(event) and boy.state == 'IDLE':
            boy.start_auto_run()
        elif event.type == SDL_KEYDOWN and event.key in (SDLK_LEFT, SDLK_RIGHT):
            if event.key not in direction_keys:
                direction_keys.append(event.key)
            if boy.state in ('IDLE', 'RUN', 'SLEEP', 'AUTO_RUN'):
                direction = 1 if direction_keys[-1] == SDLK_RIGHT else -1
                boy.run_in_direction(direction)
        elif event.type == SDL_KEYUP and event.key in (SDLK_LEFT, SDLK_RIGHT):
            if event.key in direction_keys:
                direction_keys.remove(event.key)
            if boy.state == 'RUN':
                if direction_keys:
                    direction = 1 if direction_keys[-1] == SDLK_RIGHT else -1
                    boy.run_in_direction(direction)
                else:
                    boy.stop_running()


def reset_world():
    global world
    global boy

    world = []

    grass = Grass()
    world.append(grass)

    boy = Boy()
    world.append(boy)



def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


running = True
direction_keys = []

open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
