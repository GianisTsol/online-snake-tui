"""Models responsible for client side game run."""
from blessed import Terminal


class Window:
    """Class for rendering game on the screen."""

    CHARS = ['┌', '─', '┐', '│', '└', '┘']

    def __init__(self, size: tuple):
        """TODO: Docstring."""
        self.term = Terminal()
        self.width, self.height = size
        self.BORDER_COLOR = self.term.bright_green

    def draw_border(self):
        """TODO: Docstring."""
        print(self.term.home + self.term.clear, end='')  # Clear the screen

        # Print the border header
        print(self.BORDER_COLOR + self.CHARS[0] + self.CHARS[1]
              * (self.width - 2) + self.CHARS[2] + self.term.normal)

        # Print border sides
        for i in range(self.height - 3):
            print(self.BORDER_COLOR + self.CHARS[3] + self.term.normal + ' '
                  * (self.width - 2) + self.BORDER_COLOR
                  + self.CHARS[3] + self.term.normal)

        # Print the border footer
        print(self.BORDER_COLOR + self.CHARS[4] + self.CHARS[1]
              * (self.width - 2) + self.CHARS[5] + self.term.normal)
