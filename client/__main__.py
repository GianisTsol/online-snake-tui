"""Entrypoint for the TUI client."""
import os

from blessed import Terminal

from .game import start_game
from .level import Window

sel = 1


def display_menu(term: Terminal, menu: list, sel: int):
    """Display the menu."""
    print(term.home + term.clear, end='')
    print(term.move_xy(round(term.width / 2), round(term.height / 2)))
    for i in menu:
        if menu.index(i) == sel - 1:
            print(term.bold_red_reverse + i[0] + term.normal)
        else:
            print(term.red + i[0] + term.normal)


def on_key_press(key: str, term: Terminal, menu: list):
    """Handle key presses."""
    global sel
    key = str(key).replace("KEY_", "").lower()  # get keys at more usable format
    if key == "down":
        if sel < len(menu):
            sel += 1
    elif key == "up":
        if sel > 1:
            sel -= 1
    elif key == "enter":
        menu[sel][1]()
    if key != "":
        display_menu(term, menu, sel)


# Menu options
menu = [
    ["Start Offline", start_game],
    ["Online Lobby", start_game],
    ["Custom", start_game],
    ["Exit", exit],
]

if __name__ == '__main__':
    window = Window(os.get_terminal_size())
    print(window.term.home + window.term.clear, end='')
    while True:
        with window.term.cbreak(), window.term.hidden_cursor():  # input
            on_key_press(
                window.term.inkey(timeout=1).name,
                window.term,
                menu)
