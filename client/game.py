"""Entrypoint for the Game."""
import time

from common import models

from .level import Window

FPS = 15

direction = (1, 0)  # start direction

snek_segments = 10  # Starting segments
segments = []  # list for the snakes segments

# directions #

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)


def add_segment():
    """Add segments to the snek."""
    # Function to add segments to the snake, TODO: make apple
    curr_index = len(segments)
    segments.append(
        models.SnakeSegment(id=curr_index,
                            x=1 + curr_index,
                            y=5,
                            type='snake_segment',
                            player=0,
                            before=curr_index - 1,
                            after=curr_index + 1
                            ))


def on_key_press(key: str):
    """Handle directions from key presses."""
    global direction
    key = str(key).replace("KEY_", "").lower()  # get keys at more usable format
    if key == "up" and direction != down:
        direction = up
    if key == "down" and direction != up:
        direction = down
    if key == "right" and direction != left:
        direction = right
    if key == "left" and direction != right:
        direction = left


def draw(win: Window):
    """Draw snake."""
    global segments
    global direction
    head = segments[0]
    for i in segments[::-1]:
        if i.id > 0:  # Check if not head
            print(win.term.home
                  + win.term.move_xy(i.x, i.y)
                  + win.term.green
                  + u'\u2588'
                  # + str(i.id)  # print segment id, for debug
                  + win.term.home)
    print(win.term.home
          + win.term.move_xy(head.x, head.y)
          + win.term.green
          + u'\u2588'
          # + str(i.id)
          + win.term.home)


def move():
    """Move the snake. Needs to be called each frame."""
    global segments
    global direction
    head = segments[0]
    for i in segments[::-1]:
        if i.id > 0:  # Check if not head
            i.x = segments[i.before].x
            i.y = segments[i.before].y

    head.x += direction[0]
    head.y += direction[1]


def has_collided_with_self() -> bool:
    """Return True if the snake has collided with itself."""
    global segments
    for i in segments[1:]:
        if (segments[0].x, segments[0].y) == (i.x, i.y):
            return True
    return False


def has_collided_with_wall(win: Window) -> bool:
    """Return True if the snake has collided with a wall."""
    global segments
    head = segments[0]
    return (
        head.x <= 0
        or head.x >= win.width - 1
        or head.y <= 0
        or head.y >= win.height - 1
    )


def start_game():
    """Start the game, itialize snake."""
    for i in range(0, snek_segments):  # create initial segments of snake
        add_segment()

    window = Window()

    current_time = last_frame_time = time.time()
    while True:  # Game loop

        # Calculations needed for maintaining stable FPS
        sleep_time = 1. / FPS - (current_time - last_frame_time)
        if sleep_time > 0:
            time.sleep(sleep_time)

        # sTART GAME LOOP FOR MOVEMENT
        with window.term.cbreak(), window.term.hidden_cursor():  # input
            on_key_press(window.term.inkey(timeout=0).name)

        window.draw_border()
        draw(window)
        move()
