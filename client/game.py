"""Entrypoint for the Game."""
import os
import time

from common import logic

from .level import Window

FPS = 15

segments = []  # list for the snakes segments

direction = (1, 0)  # start direction


def draw(win: Window):
    """Draw snake."""
    head = segments[0]
    for i in segments[::-1]:
        if i.id > 0:  # Check if not head
            print(win.term.home
                  + win.term.move_xy(i.x, i.y)
                  + win.term.green
                  + u'\u2588'
                  # + str(i.id)  # print segment id, for debug
                  + win.term.home)
    print(win.term.home
          + win.term.move_xy(head.x, head.y)
          + win.term.green
          + u'\u2588'
          # + str(i.id)
          + win.term.home)


def start_game(online: bool = False):
    """Start the game, itialize snake."""
    global direction
    global segments
    for i in range(0, logic.snek_segments):  # create initial segments of snake
        logic.add_segment(segments)

    window = Window(os.get_terminal_size())

    current_time = last_frame_time = time.time()
    while True:  # Game loop

        # Calculations needed for maintaining stable FPS
        sleep_time = 1. / FPS - (current_time - last_frame_time)
        if sleep_time > 0:
            time.sleep(sleep_time)

        # sTART GAME LOOP FOR MOVEMENT
        with window.term.cbreak(), window.term.hidden_cursor():  # input
            direction = logic.change_direction(
                str(
                    window.term.inkey(timeout=0).name
                )
                .replace("KEY_", "").lower(),
                direction
            )

        window.draw_border()
        draw(window)
        segments = logic.move(direction, segments)
