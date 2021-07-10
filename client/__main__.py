"""Entrypoint for the TUI client."""

import time

from .models import Window

FPS = 60

if __name__ == '__main__':
    window = Window()

    current_time = last_frame_time = time.time()
    while True:  # Game loop
        # Calculations needed for maintaining stable FPS
        sleep_time = 1. / FPS - (current_time - last_frame_time)
        if sleep_time > 0:
            time.sleep(sleep_time)

        window.redraw()
