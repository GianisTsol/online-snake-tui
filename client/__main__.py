"""Entrypoint for the TUI client."""
import json
import os

from blessed import Terminal

from server import Server

from .game import OfflineGame, OnlineGame
from .level import Window


class InputManager:
    """Data to pass to online mode."""

    def __init__(self):
        """Initialize the class."""
        self.name = "Player69"
        self.window = Window(os.get_terminal_size())
        self.term = self.window.term
        self.savefile = "save.json"
        self.savefile = os.path.join(
            os.path.dirname(__file__), self.savefile
        )  # get the absolute path of our file
        self.nick_input = "Name (2-8 chars): "
        self.host = ""
        self.port = 0
        self.load_class()

    def load_class(self):
        """Load previously entered user data."""
        if not os.path.exists(self.savefile):
            self.save_class()

        with open(self.savefile, "r") as f:
            data = json.load(f)
            for key, value in data.items():
                # set every dict key to an atribute of the class
                setattr(self, key, value)  # self.key = value

    def save_class(self):
        """Save variables for future load."""
        with open(self.savefile, "w") as f:
            data = {"name": self.name, "host": self.host, "port": self.port}
            json.dump(data, f)

    def get_user_input(self, text: str, old_val: str = "") -> str:
        """Get user input text."""
        x = self.window.width // 2  # center of screen
        y = self.window.height // 2  # center of screen
        input = old_val
        print(end=self.term.home + self.term.clear)
        print(self.term.move_xy(x, y) + self.term.red_bold + text)
        while True:
            print(end=self.term.home + self.term.clear)
            print(
                self.term.move_xy(x - len(input + text) // 2, y)
                + self.term.red_bold
                + text
                + self.term.blue
                + self.term.underline
                + input
                + self.term.normal
            )
            val = self.term.inkey()
            if val.name == "KEY_ENTER":
                break
            elif val.name == "KEY_BACKSPACE":
                input = input[:-1]
            else:
                input += val
        return input

    def change_nickname(self):
        """Change player name."""
        x = self.window.width // 2  # center of screen
        y = self.window.height // 2  # center of screen
        """Prompt for player to change their name."""
        self.name = self.get_user_input(self.nick_input, self.name)
        if len(self.name) > 8 or len(self.name) < 2:
            print(end=self.term.home + self.term.clear)
            print(self.term.move_xy(x, y) + self.term.red_bold + "INVALID")
            self.name = ""
            self.term.inkey()
            self.change_nickname()
        print(self.term.normal)
        self.save_class()

    def connect_to_game(self):
        """Prompt server details."""
        if not self.host:
            self.host = self.get_user_input("Server ip: ")
            try:
                self.port = int(self.get_user_input("Port (65444): "))
            except ValueError:
                self.port = 65444
            self.save_class()
        OnlineGame(self.host, self.port, self.name)

    def reset_server(self):
        """Reset server details."""
        self.host = None
        self.port = None
        self.save_class()

    def start_server(self):
        """Input config params and start server."""
        name = self.get_user_input("Server Name: ", "SnekBox")
        server_port = int(self.get_user_input("Port (65444): ", str(65444)))
        server_y = self.get_user_input("Height: ", str(32))
        server_x = self.get_user_input("Width: ", str(128))
        tick = int(self.get_user_input("Tickrate: ", str(15)))
        max = int(self.get_user_input("Max Players: ", str(5)))

        print(end=self.term.home + self.term.clear)
        print("Starting server...")
        print("PRESS Q TO QUIT")
        config = {
            "SERVER_NAME": name,
            "GAME_VERSION": 0,
            "BOX_WIDTH": server_x,
            "BOX_HEIGHT": server_y,
            "TICKRATE": tick,
            "MAX_PLAYERS": max,
        }
        serv = Server(port=server_port, config=config)
        serv.start()

        while True:
            val = self.term.inkey()
            if val == "q":
                print("Exiting...")
                serv.stop()
                serv.join()
                break


inmger = InputManager()


class Menu:
    """The main menu."""

    OPTIONS = [
        ["Start Offline", OfflineGame],
        ["Connect to server", inmger.connect_to_game],
        ["Reset Server Details", inmger.reset_server],
        ["Change Nickname", inmger.change_nickname],
        ["Host A Server", inmger.start_server],
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
        print(
            self.term.move_xy(base_x - 2, base_y - 2)
            + self.term.green_bold
            + "SNEK"
            + self.term.normal
        )
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
