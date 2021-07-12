"""Entrypoint for the Game."""
import os
import time

from common import logic

from .level import Window

BLOCK_CHAR = '█'
FPS = 15


class GameController:
    """The game mainloop."""

    def __init__(
            self,
            online: bool = False,
            direction: tuple[int, int] = (1, 0)):
        """Set up the game."""
        self.online = online
        self.window = Window(os.get_terminal_size())
        self.term = self.window.term
        self.direction = direction
        self.segments = []
        # Create the initial snake segments.
        for _ in range(logic.STARTING_SNAKE_SEGMENTS):
            logic.add_segment(self.segments)
        with self.term.hidden_cursor():
            self.run_game_loop()

    def draw(self):
        """Draw the snake on the window."""
        for i in self.segments:
            print(
                self.term.home
                + self.term.move_xy(i.x, i.y)
                + self.window.SNAKE_COLOR
                + BLOCK_CHAR
                + self.term.normal
                + self.term.home
            )

    def run_game_loop(self):
        """Run the game update loop."""
        last_frame_time = current_time = time.time()
        while True:
            # Calculations needed for maintaining stable FPS
            sleep_time = 1 / FPS - (current_time - last_frame_time)
            if sleep_time > 0:
                time.sleep(sleep_time)

            # Change direction if there is input.
            with self.term.cbreak():
                if key := self.term.inkey(timeout=0).name:
                    self.direction = logic.change_direction(
                        key.removeprefix('KEY_').lower(),
                        self.direction
                    )

            # Render the screen.
            self.window.draw_border()
            self.draw()
            # Move the snake.
            logic.move(self.direction, self.segments)
