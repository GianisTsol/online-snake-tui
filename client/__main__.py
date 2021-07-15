"""Entrypoint for the TUI client."""
import os

from blessed import Terminal

from .game import GameController
from .level import Window


class PlayerData:
    """Data to pass to online mode."""

    def __init__(self):
        """Initialize the class."""
        self.name = "Player69"
        self.window = Window(os.get_terminal_size())
        self.term = self.window.term
        self.nick_input = "Name (8 chars max): "

    def change_nickname(self):
        """Prompt for player to change their name."""
        print(end=self.term.home + self.term.clear)
        x = self.window.width // 2
        y = self.window.height // 2
        print(self.term.move_xy(x, y) + self.term.red_bold + self.nick_input)
        while True:
            print(end=self.term.home + self.term.clear)
            print(
                self.term.move_xy(x - len(self.name + self.nick_input) // 2, y)
                + self.term.red_bold
                + self.nick_input
                + self.term.blue
                + self.name
            )
            val = self.term.inkey()
            if val.name == "KEY_ENTER":
                break
            elif val.name == "KEY_BACKSPACE":
                self.name = self.name[:-1]
            else:
                self.name += val
        if len(self.name) > 8:
            print(end=self.term.home + self.term.clear)
            print(self.term.move_xy(x, y) + self.term.red_bold + "INVALID")
            self.name = ""
            self.term.inkey()
            self.change_nickname()
        print(self.term.normal)


player = PlayerData()


class Menu:
    """The main menu."""

    OPTIONS = [
        ["Start Offline", GameController],
        ["Online Lobby", lambda: GameController(online=True, name=player.name)],
        ["Change Nickname", player.change_nickname],
        ["Custom", GameController],
        ["Exit", exit],
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
        if key == "down":
            self.selection_index += 1
            self.selection_index %= len(self.OPTIONS)
            self.draw()
        elif key == "up":
            self.selection_index -= 1
            self.selection_index %= len(self.OPTIONS)
            self.draw()
        elif key == "enter":
            self.OPTIONS[self.selection_index][1]()
            self.draw()

    def event_loop(self):
        """Wait for keypresses."""
        while True:
            with self.term.cbreak(), self.term.hidden_cursor():
                key = window.term.inkey(timeout=1).name
                if key:
                    self.on_key_press(key.removeprefix("KEY_").lower())


if __name__ == "__main__":
    window = Window(os.get_terminal_size())
    Menu(window.term)
