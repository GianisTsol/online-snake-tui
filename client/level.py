"""Models responsible for client side game run."""
import random

from blessed import Terminal


class Window:
    """Class for rendering game on the screen."""

    # N[orth], S[outh], E[ast] and W[est] indicate that they have lines
    # joining up, down, right and left respectively.
    CHAR_ES = '┌'
    CHAR_EW = '─'
    CHAR_SW = '┐'
    CHAR_NS = '│'
    CHAR_NE = '└'
    CHAR_NW = '┘'

    def __init__(self, size: tuple[int, int]):
        """Set up the game renderer."""
        self.term = Terminal()
        self.width, self.height = size
        self.BORDER_COLOR = self.term.bright_green

        self.SNAKE_COLORS = [self.term.red, self.term.green, self.term.yellow,
                             self.term.blue, self.term.magenta, self.term.cyan]
        self.SNAKE_COLOR = random.choice(self.SNAKE_COLORS)

    def _draw_border_row(self, start: str, middle: str, end: str):
        """Draw one line of the border around the screen."""
        print(
            self.BORDER_COLOR + start + middle * (self.width - 2) + end,
            end=self.term.normal
        )

    def draw_border(self):
        """Draw the border around the edge of the screen."""
        print(self.term.home + self.term.clear, end='')  # Clear the screen

        # Print the border header
        self._draw_border_row(self.CHAR_ES, self.CHAR_EW, self.CHAR_SW)

        # Print border sides
        for _ in range(self.height - 3):
            self._draw_border_row(
                self.CHAR_NS + self.term.normal,
                ' ',
                self.BORDER_COLOR + self.CHAR_NS
            )

        # Print the border footer
        self._draw_border_row(self.CHAR_NE, self.CHAR_EW, self.CHAR_NW)
