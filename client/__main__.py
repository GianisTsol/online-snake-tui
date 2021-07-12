"""Entrypoint for the TUI client."""
import os

from blessed import Terminal

from .game import GameController
from .level import Window


class Menu:
    """The main menu."""

    OPTIONS = [
        ['Start Offline', GameController],
        ['Online Lobby', lambda: GameController(online=True)],
        ['Custom', GameController],
        ['Exit', exit],
    ]

    def __init__(self, term: Terminal):
        """Set up the menu."""
        self.term = term
        self.selection_index = 0
        self.draw()
        self.event_loop()

    def draw(self):
        """Render the menu to the terminal."""
        base_x = self.term.width // 2
        base_y = (self.term.height - len(self.OPTIONS)) // 2
        print(end=self.term.home + self.term.clear)
        self.term.move_xy
        for index, (label, _action) in enumerate(self.OPTIONS):
            x = base_x - len(label) // 2
            y = base_y + index
            if index == self.selection_index:
                style = self.term.bold_red_reverse
            else:
                style = self.term.red
            print(self.term.move_xy(x, y) + style + label + self.term.normal)

    def on_key_press(self, key: str):
        """Handle a key being pressed."""
        if key == 'down':
            self.selection_index += 1
            self.selection_index %= len(self.OPTIONS)
            self.draw()
        elif key == 'up':
            self.selection_index -= 1
            self.selection_index %= len(self.OPTIONS)
            self.draw()
        elif key == 'enter':
            self.OPTIONS[self.selection_index][1]()

    def event_loop(self):
        """Wait for keypresses."""
        while True:
            with self.term.cbreak(), self.term.hidden_cursor():
                key = window.term.inkey(timeout=1).name
                if key:
                    self.on_key_press(key.removeprefix('KEY_').lower())


if __name__ == '__main__':
    window = Window(os.get_terminal_size())
    Menu(window.term)
