"""Models responsible for client side game run."""
import math
import random

from blessed import Terminal


class Window:
    """Class for rendering game on the screen."""

    # N[orth], S[outh], E[ast] and W[est] indicate that they have lines
    # joining up, down, right and left respectively.
    CHAR_ES = "┌"
    CHAR_EW = "─"
    CHAR_SW = "┐"
    CHAR_NS = "│"
    CHAR_NE = "└"
    CHAR_NW = "┘"

    def __init__(self, size: tuple[int, int]):
        """Set up the game renderer."""
        self.term = Terminal()
        self.size = size
        self.width, self.height = size
        self.BORDER_COLOR = self.term.bright_green

        self.SNAKE_COLORS = [
            self.term.red,
            self.term.green,
            self.term.yellow,
            self.term.blue,
            self.term.magenta,
            self.term.cyan,
        ]
        self.SNAKE_COLOR = random.choice(self.SNAKE_COLORS)

        self.player_colors = []

    def _draw_border_row(
        self, start: str, middle: str, end: str, width: int, x_offset: int = 0
    ):
        """Draw one line of the border around the screen."""
        print(
            self.term.move_right(x_offset)
            + self.BORDER_COLOR
            + start
            + middle * (width - 2)
            + end
            + self.term.normal
        )

    def player_color(self, player: int) -> str:
        """Get color for player id."""
        if len(self.player_colors) > player:
            self.player_colors.append(random.choice(self.SNAKE_COLORS))
            return self.player_colors[player]
        else:
            return self.SNAKE_COLORS[player]

    def draw_scoreboard(self, players: list):
        """Draw the scoreboard."""
        players = sorted(players, key=lambda x: x["score"])
        max_len = 1
        for i in players:
            i["name"] = str(i["score"]) + ": " + i["name"]
            if len(i["name"]) > max_len:
                max_len = len(i["name"])

        max_len += 2
        print(self.term.move_y(0))
        # Print the border header
        self._draw_border_row(
            self.CHAR_ES, self.CHAR_EW, self.CHAR_SW, max_len, self.width + 1
        )

        # Print border sides
        for _ in range(len(players)):
            self._draw_border_row(
                self.CHAR_NS + self.term.normal,
                " ",
                self.BORDER_COLOR + self.CHAR_NS,
                max_len,
                self.width + 1,
            )

        # Print the border footer
        self._draw_border_row(
            self.CHAR_NE, self.CHAR_EW, self.CHAR_NW, max_len, self.width + 1
        )

        for player in players:
            print(
                self.term.move_xy(
                    self.width + math.floor((max_len - len(player["name"])) / 2),
                    players.index(player) + 2,
                )
                + player["name"]
            )

    def draw_border(self):
        """Draw the border around the edge of the screen."""
        print(self.term.home + self.term.clear, end="")  # Clear the screen

        # Print the border header
        self._draw_border_row(
            self.CHAR_ES, self.CHAR_EW, self.CHAR_SW, self.width - 2
        )

        # Print border sides
        for _ in range(self.height - 3):
            self._draw_border_row(
                self.CHAR_NS + self.term.normal,
                " ",
                self.BORDER_COLOR + self.CHAR_NS,
                self.width - 2,
            )

        # Print the border footer
        self._draw_border_row(
            self.CHAR_NE, self.CHAR_EW, self.CHAR_NW, self.width - 2
        )
