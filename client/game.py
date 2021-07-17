"""Entrypoint for the Game."""
import os
import time

from common import logic

from .level import Window
from .networking import Connection

BLOCK_CHAR = "█"
FPS = 15

# The numbers are lower score boundaries for each verdicts.
DEATH_VERDICTS = [
    (0, "Pathetic."),
    (1, "Try harder next time?"),
    (5, "Almost good."),
    (10, "Not bad..."),
    (15, "Decent."),
    (20, "Well done."),
    (25, "Nice!"),
    (30, "Sweet!"),
    (45, "Amazing!!"),
    (50, "Wow!!! What a game!"),
    (69, "Nice. Maybe not so pathetic after all."),
    (100, "The bestest of the best!!!"),
    (120, "Still pathetic lmao."),
]

# N[orth]/E[ast]/S[outh]/[W]est indicates direction of segment to join on to.
SNAKE_HEAD_CHARS = {
    "n": "╹",
    "e": "╺",
    "s": "╻",
    "w": "╸",
}

SNAKE_BODY_CHARS = {
    "ew": "═",
    "ns": "║",
    "es": "╔",
    "sw": "╗",
    "ne": "╚",
    "nw": "╝",
    "ww": "═",
}

SNAKE_TAIL_CHARS = {
    "n": "╿",
    "e": "╼",
    "s": "╽",
    "w": "╾",
}


class Game:
    """The game mainloop."""

    def __init__(self, win: Window):
        """Game class base."""
        self.window = win
        self.term = Window.term

    def get_death_message(self) -> str:
        """Get the message to show when the player dies."""
        for score, possible_verdict in DEATH_VERDICTS:
            if score <= self.score:
                verdict = possible_verdict
        return f"You died with: {self.score} score. {verdict}"

    def show_death_screen(self):
        """Show when player dies."""
        message = self.get_death_message()
        # Calculate center.
        x = self.term.width // 2 - len(message) // 2
        y = self.term.height // 2
        print(end=self.term.home + self.term.clear)
        print(
            self.term.move_xy(x, y) + self.term.red + message + self.term.normal
        )


class OfflineGame(Game):
    """docstring for OfflineGame."""

    def __init__(self):
        """Set up the game."""
        self.window = Window(os.get_terminal_size())
        self.term = self.window.term
        self.direction = (1, 0)
        self.segments = []
        self.score = 0
        self.apple = None

        # Create the initial snake segments.
        for _ in range(logic.STARTING_SNAKE_SEGMENTS):
            logic.add_segment(self.segments)
        with self.term.hidden_cursor():
            self.run_game_loop()

    def direction_from_segment(
        self, from_segment_index: int, to_segment_index: int
    ) -> str:
        """Find the direction from one segment to another.

        Assumes these segments are connected.
        """
        s_from = self.segments[from_segment_index]
        s_to = self.segments[to_segment_index]
        if s_from.x == s_to.x:
            return "n" if s_to.y < s_from.y else "s"
        else:
            return "e" if s_to.x > s_from.x else "w"

    def draw(self):
        """Draw the snake on the window."""
        snake_chars = []
        snake_chars.append(SNAKE_HEAD_CHARS[self.direction_from_segment(0, 1)])
        for body_index in range(1, len(self.segments) - 1):
            before_dir = self.direction_from_segment(body_index, body_index - 1)
            after_dir = self.direction_from_segment(body_index, body_index + 1)
            if before_dir + after_dir in SNAKE_BODY_CHARS:
                snake_chars.append(SNAKE_BODY_CHARS[before_dir + after_dir])
            else:
                snake_chars.append(SNAKE_BODY_CHARS[after_dir + before_dir])
        snake_chars.append(SNAKE_TAIL_CHARS[self.direction_from_segment(-1, -2)])
        for segment, char in zip(self.segments, snake_chars):
            print(
                self.term.home
                + self.term.move_xy(segment.x, segment.y)
                + self.window.SNAKE_COLOR
                + char
                + self.term.normal
                + self.term.home
            )

        print(
            self.term.home
            + self.term.move_xy(self.apple.x, self.apple.y)
            + self.term.red
            + BLOCK_CHAR
            + self.term.normal
            + self.term.home
        )

    def run_game_loop(self):
        """Run the game update loop."""
        last_frame_time = current_time = time.time()
        self.apple = logic.create_apple(self.window.size, self.segments)
        while True:
            # Calculations needed for maintaining stable FPS
            sleep_time = 1 / FPS - (current_time - last_frame_time)
            if sleep_time > 0:
                time.sleep(sleep_time)

            # Change direction if there is input.
            with self.term.cbreak():
                if key := self.term.inkey(timeout=0).name:
                    self.direction = logic.change_direction(
                        key.removeprefix("KEY_").lower(), self.direction
                    )

            # Render the screen.
            self.window.draw_border()
            self.draw()
            # Move the snake.
            logic.move(self.direction, self.segments)

            # check for apple
            if logic.check_apple(self.segments, self.apple):
                self.apple = logic.create_apple(self.window.size, self.segments)
                logic.add_segment(self.segments)
                self.score += 1

            # check for collisions
            if logic.has_collided_with_self(
                self.segments
            ) or logic.has_collided_with_wall(
                self.window.width, self.window.height, self.segments
            ):
                self.show_death_screen()
                with self.term.cbreak():
                    self.term.inkey()
                    return


class OnlineGame(Game):
    """Online Game Mode controller."""

    def __init__(self, host: str, port: int, name: str):
        """Online Game class."""
        self.con = Connection()
        self.name = name
        self.score = 0
        self.alive = True
        self.direction = (1, 0)
        self.con.connect(host, port)
        self.con.start()  # After connecting, start recieving

        while not self.con.ready:
            pass  # Wait until we start getting data

        self.start_online()

    def draw(self, entities: dict):
        """Draw all etities given."""
        for i in entities:
            type = i["type"]
            if type == "snake_segment":
                # TODO: add artemis' beautiful snake
                print(
                    self.term.home
                    + self.term.move_xy(i["x"], i["y"])
                    + self.window.player_color(i["player"])
                    + BLOCK_CHAR
                    + self.term.normal
                    + self.term.home
                )
            if type == "apple":
                print(
                    self.term.home
                    + self.term.move_xy(i["x"], i["y"])
                    + self.term.red
                    + BLOCK_CHAR
                    + self.term.normal
                    + self.term.home
                )

    def end_game(self):
        """End game session."""
        self.show_death_screen()
        # stop the con thread
        self.con.stop()
        self.con.join()
        self.alive = False

    def event_handler(self, type: str, data: any):
        """Server event handler."""
        if type == "dead":
            self.score = int(data)
            self.end_game()

    def start_online(self):
        """Start the game in online mode."""
        self.window = Window(
            (self.con.serverinfo.width, self.con.serverinfo.height)
        )
        self.term = self.window.term

        last_frame_time = current_time = time.time()

        self.con.send_event("nick", self.name)  # send our name to server

        while self.alive:
            # Calculations needed for maintaining stable FPS
            sleep_time = 1 / FPS - (current_time - last_frame_time)
            if sleep_time > 0:
                time.sleep(sleep_time)

            self.window.draw_border(name=self.con.serverinfo.name)
            # Get key presses and send them as change direction events
            with self.term.cbreak():
                if key := self.term.inkey(timeout=0).name:
                    self.direction = logic.change_direction(
                        key.removeprefix("KEY_").lower(), self.direction
                    )  # do key loic
                    self.con.send_event(
                        "dir", self.direction
                    )  # send the direction

            data = self.con.get_newest()
            if data:
                # get players and draw scoreboard
                if "players" in data:
                    self.window.draw_scoreboard(data["players"])

                # check fore server events
                if "event" in data:
                    self.event_handler(
                        data["event"]["type"], data["event"]["data"]
                    )

                if "entities" in data:
                    # Draw each entity sent to us
                    self.draw(data["entities"])

        # wait for key press to return to main menu
        with self.term.cbreak():
            self.term.inkey()
